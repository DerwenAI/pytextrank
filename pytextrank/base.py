#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/pytextrank#license-and-copyright

"""
Implements the base class for `TextRank` –
with placeholder methods to be used by the subclasses for algorithm extensions.
"""

from collections import Counter, defaultdict, OrderedDict
from dataclasses import dataclass
import json
import math
import pathlib
import time
import typing

from icecream import ic  # type: ignore # pylint: disable=E0401,W0611 # lgtm[py/unused-import]
from spacy.tokens import Doc, Span, Token  # type: ignore # pylint: disable=E0401
import graphviz  # type: ignore # pylint: disable=E0401
import networkx as nx  # type: ignore # pylint: disable=E0401

from .util import groupby_apply, default_scrubber

try:
    import altair as alt  # type: ignore # pylint: disable=E0401
    import pandas as pd  # type: ignore # pylint: disable=E0401
except ImportError:
    _has_altair_and_pandas = False
else:
    _has_altair_and_pandas = True

# parameter type annotation for a *stop words* source
StopWordsLike = typing.Union[ str, pathlib.Path, typing.Dict[str, typing.List[str]] ]


@dataclass(order=True, frozen=True)
class Lemma:
    """
A data class representing one node in the *lemma graph*.
    """
    lemma: str
    pos: str


    def label (
        self
        ) -> str:
        """
Generates a more simplified string representation than `repr()`
provides.

    returns:
string representation
        """
        return str((self.lemma, self.pos,))


@dataclass
class Phrase:
    """
A data class representing one ranked phrase.
    """
    text: str
    chunks: typing.List[Span]
    count: int
    rank: float


@dataclass
class Sentence:
    """
A data class representing the distance measure for one sentence.
    """
    start: int
    end: int
    sent_id: int
    phrases: typing.Set[int]
    distance: float


    def empty (
        self
        ) -> bool:
        """
Test whether this sentence includes any ranked phrases.

    returns:
`True` if the `phrases` is not empty.
        """
        return len(self.phrases) == 0


    def text (
        self,
        doc: Doc,
        ) -> str:
        """
Accessor for the text slice of the `spaCy` [`Doc`](https://spacy.io/api/doc)
document represented by this sentence.

    doc:
source document

    returns:
the sentence text
        """
        return doc[self.start:self.end]


@dataclass
class VectorElem:
    """
A data class representing one element in the *unit vector* of the document.
    """
    phrase: Phrase
    phrase_id: int
    coord: float


@dataclass
class Paragraph:
    """
A data class representing the distance measure for one paragraph.
    """
    start: int
    end: int
    para_id: int
    distance: float


class BaseTextRankFactory:
    """
A factory class that provides the document with its instance of
`BaseTextRank`
    """

    _EDGE_WEIGHT: float = 1.0
    _POS_KEPT: typing.List[str] = ["ADJ", "NOUN", "PROPN", "VERB"]
    _TOKEN_LOOKBACK: int = 3


    def __init__ (
        self,
        *,
        edge_weight: float = _EDGE_WEIGHT,
        pos_kept: typing.List[str] = None,
        token_lookback: int = _TOKEN_LOOKBACK,
        scrubber: typing.Optional[typing.Callable] = None,
        stopwords: typing.Optional[StopWordsLike] = None,
        ) -> None:
        """
Constructor for a factory used to instantiate the PyTextRank pipeline components.

    edge_weight:
default weight for an edge

    pos_kept:
parts of speech tags to be kept; adjust this if strings representing the POS tags change

    token_lookback:
the window for neighboring tokens – similar to a *skip gram*

    scrubber:
optional "scrubber" function to clean up punctuation from a token; if `None` then defaults to `pytextrank.default_scrubber`; when running, PyTextRank will throw a `FutureWarning` warning if the configuration uses a deprecated approach for a scrubber function

    stopwords:
optional dictionary of `lemma: [pos]` items to define the *stop words*, where each item has a key as a lemmatized token and a value as a list of POS tags; may be a file name (string) or a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html) for a JSON file; otherwise throws a `TypeError` exception
        """
        self.edge_weight: float = edge_weight
        self.token_lookback: int = token_lookback

        if pos_kept:
            self.pos_kept: typing.List[str] = pos_kept
        else:
            self.pos_kept = self._POS_KEPT

        if scrubber:
            self.scrubber: typing.Callable = scrubber
        else:
            self.scrubber = default_scrubber

        if stopwords:
            self.stopwords: typing.Dict[str, typing.List[str]] = self._load_stopwords(stopwords)
        else:
            self.stopwords = defaultdict(list)


    @classmethod
    def _load_stopwords (
        cls,
        stopwords: typing.Optional[StopWordsLike] = None,
        ) -> typing.Dict[str, typing.List[str]]:
        """
Load a dictionary of
[*stop words*](https://derwen.ai/docs/ptr/glossary/#stop-words)
– i.e., tokens to be ignored when constructing the
[*lemma graph*](https://derwen.ai/docs/ptr/glossary/#lemma-graph).

Note: be cautious about the use of this feature, since it can get
"greedy" and bias or otherwise distort the results.

    stopwords:
optional dictionary of `lemma: [pos]` items to define the *stop words*, where each item has a key as a lemmatized token and a value as a list of POS tags; may be a file name (string) or a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html) for a JSON file; otherwise throws a `TypeError` exception

    returns:
the *stop words* dictionary
        """
        if isinstance(stopwords, dict):
            return stopwords

        if isinstance(stopwords, pathlib.Path):
            path: pathlib.Path = stopwords
        else:
            path = pathlib.Path(str)  # type: ignore

        if path.exists():
            with open(path, "r") as f:
                data = json.load(f)

                if data:
                    return data.items()

        raise TypeError("cannot parse the stopwords source as a dictionary")


    def __call__ (
        self,
        doc: Doc,
        ) -> Doc:
        """
Set the extension attributes on a `spaCy` [`Doc`](https://spacy.io/api/doc)
document to create a *pipeline component* for `BaseTextRank` as
a stateful component, invoked when the document gets processed.

See: <https://spacy.io/usage/processing-pipelines#pipelines>

    doc:
a document container, providing the annotations produced by earlier stages of the `spaCy` pipeline
        """
        Doc.set_extension("textrank", force=True, default=None)
        Doc.set_extension("phrases", force=True, default=[])

        doc._.textrank = BaseTextRank(
            doc,
            edge_weight = self.edge_weight,
            pos_kept = self.pos_kept,
            token_lookback = self.token_lookback,
            scrubber = self.scrubber,
            stopwords = self.stopwords,
            )

        doc._.phrases = doc._.textrank.calc_textrank()
        return doc


class BaseTextRank:
    """
Implements the *TextRank* algorithm defined by
[[mihalcea04textrank]](https://derwen.ai/docs/ptr/biblio/#mihalcea04textrank),
deployed as a `spaCy` pipeline component.

This class does not get called directly; instantiate its factory
instead.
    """

    def __init__ (
        self,
        doc: Doc,
        edge_weight: float,
        pos_kept: typing.List[str],
        token_lookback: int,
        scrubber: typing.Callable,
        stopwords: typing.Dict[str, typing.List[str]],
        ) -> None:
        """
Constructor for a `TextRank` object.

    doc:
a document container, providing the annotations produced by earlier stages of the `spaCy` pipeline

    edge_weight:
default weight for an edge

    pos_kept:
parts of speech tags to be kept; adjust this if strings representing the POS tags change

    token_lookback:
the window for neighboring tokens – similar to a *skip gram*

    scrubber:
optional "scrubber" function to clean up punctuation from a token

    stopwords:
optional dictionary of `lemma: [pos]` items to define the *stop words*, where each item has a key as a lemmatized token and a value as a list of POS tags
        """
        self.doc: Doc = doc
        self.edge_weight: float = edge_weight
        self.token_lookback: int = token_lookback
        self.pos_kept: typing.List[str] = pos_kept
        self.scrubber: typing.Callable = scrubber
        self.stopwords: typing.Dict[str, typing.List[str]] = stopwords

        # internal data for BiasedTextRank
        self.focus_tokens: typing.Set[str] = set()
        self.node_bias = 1.0
        self.default_bias = 1.0

        # effectively, performs the same work as the `reset()` method;
        # called explicitly here for the sake of type annotations
        self.elapsed_time: float = 0.0
        self.lemma_graph: nx.Graph = nx.Graph()
        self.phrases: typing.List[Phrase] = []
        self.ranks: typing.Dict[Lemma, float] = {}
        self.seen_lemma: typing.Dict[Lemma, typing.Set[int]] = OrderedDict()


    def reset (
        self
        ) -> None:
        """
Reinitialize the data structures needed for extracting phrases,
removing any pre-existing state.
        """
        self.elapsed_time = 0.0
        self.lemma_graph = nx.Graph()
        self.phrases = []
        self.ranks = {}
        self.seen_lemma = OrderedDict()


    def calc_textrank (
        self
        ) -> typing.List[Phrase]:
        """
Iterate through each sentence in the doc, constructing a
[*lemma graph*](https://derwen.ai/docs/ptr/glossary/#lemma-graph)
then returning the top-ranked phrases.

This method represents the heart of the *TextRank* algorithm.

    returns:
list of ranked phrases, in descending order
        """
        t0 = time.time()
        self.reset()
        self.lemma_graph = self._construct_graph()

        # to run the algorithm, we use the NetworkX implementation
        # for PageRank (i.e., based on eigenvector centrality)
        # to calculate a rank for each node in the lemma graph
        self.ranks = nx.pagerank(
            self.lemma_graph,
            personalization = self.get_personalization(),
            )

        # agglomerate the lemmas ranked in the lemma graph into ranked
        # phrases, leveraging information from earlier stages of the
        # pipeline: noun chunks and named entities
        nc_phrases: typing.Dict[Span, float] = {}

        try:
            nc_phrases = self._collect_phrases(self.doc.noun_chunks, self.ranks)
        except NotImplementedError as ex:
            # some languages don't have `noun_chunks` support in spaCy models, e.g. "ru"
            ic.disable()
            ic(ex)
            ic.enable()

        ent_phrases: typing.Dict[Span, float] = self._collect_phrases(self.doc.ents, self.ranks)
        all_phrases: typing.Dict[Span, float] = { **nc_phrases, **ent_phrases }

        # since noun chunks can be expressed in different ways (e.g., may
        # have articles or prepositions), we need to find a minimum span
        # for each phrase based on combinations of lemmas
        raw_phrase_list: typing.List[Phrase] = self._get_min_phrases(all_phrases)
        phrase_list: typing.List[Phrase] = sorted(raw_phrase_list, key=lambda p: p.rank, reverse=True)

        t1 = time.time()
        self.elapsed_time = (t1 - t0) * 1000.0

        return phrase_list


    def get_personalization (  # pylint: disable=R0201
        self
        ) -> typing.Optional[typing.Dict[Lemma, float]]:
        """
Get the *node weights* for initializing the use of the
[*Personalized PageRank*](https://derwen.ai/docs/ptr/glossary/#personalized-pagerank)
algorithm.

Defaults to a no-op for the base *TextRank* algorithm.

    returns:
`None`
        """
        return None


    def _construct_graph (
        self
        ) -> nx.Graph:
        """
Construct the
[*lemma graph*](https://derwen.ai/docs/ptr/glossary/#lemma-graph).

    returns:
a directed graph representing the lemma graph
        """
        g = nx.Graph()

        # add nodes made of Lemma(lemma, pos)
        g.add_nodes_from(self.node_list)

        # add edges between nodes that co-occur within a window,
        # weighted by the count
        g.add_edges_from(self.edge_list)

        return g


    def _keep_token (
        self,
        token: Token,
        ) -> bool:
        """
Skip tokens that are either in the stop word list or don't have a part
of speech tag suitable for vertices in the lemma graph.
Otherwise, track this token in the `seen_lemma` dictionary.

    token:
a parsed `spaCy` [`Token`](https://spacy.io/api/token) to be evaluated

    returns:
boolean value for whether to keep this token as a node in the lemma graph
        """
        lemma = token.lemma_.lower().strip()

        if self._is_stopword(lemma, token):
            return False

        if token.pos_ not in self.pos_kept:
            return False

        # also track occurrence of this token's lemma, for later use
        key = Lemma(lemma, token.pos_,)

        if key not in self.seen_lemma:
            self.seen_lemma[key] = set([token.i])
        else:
            self.seen_lemma[key].add(token.i)

        return True


    def _is_stopword (
        self,
        lemma: str,
        token: Token,
        ) -> bool:
        """
Determine whether the given (lemma, pos) pair was identified with in
the *stop words* list.

    returns:
boolean result of the test
        """
        return lemma in self.stopwords and token.pos_ in self.stopwords[lemma]


    @property
    def node_list (
        self
        ) -> typing.List[Lemma]:
        """
Build a list of vertices for the lemma graph.

    returns:
list of nodes
        """
        nodes: typing.List[Lemma] = [
            Lemma(token.lemma_, token.pos_)
            for token in self.doc
            if self._keep_token(token)
        ]

        return nodes


    @property
    def edge_list (
        self
        ) -> typing.List[typing.Tuple[Lemma, Lemma, typing.Dict[str, float]]]:
        """
Build a list of weighted edges for the lemma graph.

    returns:
list of weighted edges
        """
        edges: typing.List[typing.Tuple[Lemma, Lemma]] = []

        for sent in self.doc.sents:
            h = [
                Lemma(token.lemma_, token.pos_)
                for token in sent
                if self._keep_token(token)
            ]

            for hop in range(self.token_lookback):
                for idx, node in enumerate(h[: -1 - hop]):
                    nbor = h[hop + idx + 1]
                    edges.append((node, nbor))

        # include weight on the edge: (2, 3, {'weight': 3.1415})
        weighted_edges: typing.List[typing.Tuple[Lemma, Lemma, typing.Dict[str, float]]] = [
            (*n, {"weight": w * self.edge_weight}) for n, w in Counter(edges).items()
        ]

        return weighted_edges


    def _collect_phrases (
        self,
        spans: typing.Iterable[Span],
        ranks: typing.Dict[Lemma, float]
        ) -> typing.Dict[Span, float]:
        """
Aggregate the rank metrics of the individual nodes (tokens) within
each phrase.

    spans:
spans of noun chunks

    ranks:
rank metrics corresponding to each node

    returns:
phrases extracted from the lemma graph, each with an aggregate rank metric
        """
        phrases: typing.Dict[Span, float] = {
            span: sum(
                ranks[Lemma(token.lemma_, token.pos_)]
                for token in span
                if self._keep_token(token)
            )
            for span in spans
        }

        return {
            span: self._calc_discounted_normalised_rank(span, sum_rank)
            for span, sum_rank in phrases.items()
        }


    def _calc_discounted_normalised_rank (
        self,
        span: Span,
        sum_rank: float
        ) -> float:
        """
Since the noun chunking is greedy, we discount the ranks using a point
estimate based on the number of non-lemma tokens within a phrase.

    span:
a span representing one phrase

    sum_rank:
sum of the ranks for each token within this span

    returns:
normalized rank metric
        """
        if len(span) < 1 :
            return 0.0
        non_lemma = len([tok for tok in span if tok.pos_ not in self.pos_kept])
        non_lemma_discount = len(span) / (len(span) + (2.0 * non_lemma) + 1.0)

        # NB:
        # This implements a *point estimate* for the ratio of the span
        # of an extracted phrase divided by the number of non-lemma
        # tokens within that span.
        #
        # The algorithm defined as in the original paper
        # [[mihalcea04textrank]](https://derwen.ai/docs/ptr/biblio/#mihalcea04textrank)
        # only considered multi-word phrases which had adjacent lemmas.
        # Early use cases in industry (circa 2009) required better recall
        # of phrases so this approach of using a point estimate here to
        # "normalize" the rank metric causes the longer phrases to get
        # discounted when they included too many non-lemma tokens.
        # In other words, we allow some non-lemmas, but avoid having
        # the algorithm become too "greedy" as it builds phrases.
        #
        # Kudos to @debraj135 who asked for an explanation about this
        # section of the code.
        phrase_rank = math.sqrt(sum_rank / (len(span) + non_lemma))

        return phrase_rank * non_lemma_discount


    def _get_min_phrases (
        self,
        all_phrases: typing.Dict[Span, float]
        ) -> typing.List[Phrase]:
        """
Group the phrases by their text content, selecting the span with the
maximum rank within each group, then collect the ranked phrases into
an ordered list.

Throws a `FutureWarning` warning if the configuration uses a
deprecated approach for a scrubber function

    all_phrases:
the raw phrase list

    returns:
an ordered list of ranked phrases

        """
        try:
            data: typing.List[typing.Tuple[Span, float, Span]] = [
                (self.scrubber(span), rank, span) for span, rank in all_phrases.items()
            ]
        except AttributeError:
            raise FutureWarning("Text-based scrubbers are deprecated. Use a `Span` instead.")

        keyfunc = lambda x: x[0]
        applyfunc = lambda g: list((rank, spans) for text, rank, spans in g)

        phrases: typing.List[typing.Tuple[str, typing.List[typing.Tuple[float, Span]]]] = groupby_apply(
            data,
            keyfunc,
            applyfunc,
        )

        phrase_list: typing.List[Phrase] = [
            Phrase(
                text = p[0],
                rank = max(rank for rank, span in p[1]),
                count = len(p[1]),
                chunks = list(span for rank, span in p[1]),
            )
            for p in phrases
        ]

        return phrase_list


    def get_unit_vector (
        self,
        limit_phrases: int,
        ) -> typing.List[VectorElem]:
        """
Construct a *unit vector* representing the top-ranked phrases in a
`spaCy` [`Doc`](https://spacy.io/api/doc) document.
This provides a *characteristic* for comparing each sentence to the
entire document.
Taking the ranked phrases in descending order, the unit vector is a
normalized list of their calculated ranks, up to the specified limit.

    limit_phrases:
maximum number of top-ranked phrases to use in the *unit vector*

    returns:
the unit vector, as a list of `VectorElem` objects
        """
        unit_vector: typing.List[VectorElem] = [
            VectorElem(
                phrase = p,
                phrase_id = phrase_id,
                coord = p.rank,
                )
            for phrase_id, p in enumerate(self.doc._.phrases)
            ]

        # truncate to the specified limit
        limit = min(limit_phrases, len(unit_vector))
        unit_vector = unit_vector[:limit]

        # normalize the phrase coordinates, such that the unit vector
        # has length = 1.0
        sum_length = sum([ elem.coord for elem in unit_vector ])

        for elem in unit_vector:
            if sum_length > 0.0:
                elem.coord = elem.coord / sum_length
            else:
                elem.coord = 0.0

        return unit_vector


    def calc_sent_dist (
        self,
        limit_phrases: int,
        ) -> typing.List[Sentence]:
        """
For each sentence in the document, calculate its distance from a *unit
vector* of top-ranked phrases.

    limit_phrases:
maximum number of top-ranked phrases to use in the *unit vector*

    returns:
a list of sentence distance measures
        """
        unit_vector = self.get_unit_vector(limit_phrases)

        sent_dist: typing.List[Sentence] = [
            Sentence(
                start = s.start,
                end = s.end,
                sent_id = sent_id,
                phrases = set(),
                distance = 0.0,
                )
            for sent_id, s in enumerate(self.doc.sents)
            ]

        # identify the top-ranked phrases in each sentence
        for elem in unit_vector:
            for chunk in elem.phrase.chunks:
                for sent in sent_dist:
                    if chunk.start >= sent.start and chunk.end <= sent.end:
                        sent.phrases.add(elem.phrase_id)
                        break

        # calculate a euclidean distance for each sentence; in other
        # words, test for inclusion of each phrase in the unit vector
        for sent in sent_dist:
            sum_sq = 0.0

            for elem in unit_vector:
                if elem.phrase_id not in sent.phrases:
                    sum_sq += elem.coord**2.0

            sent.distance = math.sqrt(sum_sq)

        return sent_dist


    def segment_paragraphs (
        self,
        sent_dist: typing.List[Sentence],
        ) -> typing.List[Paragraph]:
        """
Segment a ranked document into paragraphs.

    sent_dist:
a list of ranked Sentence data objects

    returns:
a list of Paragraph data objects
        """
        para_elem: typing.List[int] = []
        para_bounds: typing.List[typing.List[int]] = []

        # first, determine the paragraph boundaries
        for sent_id, s in enumerate(self.doc.sents):
            toke_0 = str(s.__getitem__(0))
            ret_count = sum(map(lambda c: 1 if c == "\n" else 0, toke_0))

            # test for a paragraph boundary
            if ret_count > 1:
                if len(para_elem) > 0:
                    para_bounds.append(para_elem)

                para_elem = []

            # include this sentence
            para_elem.append(sent_id)

        # then finalize
        if len(para_elem) > 0:
            para_bounds.append(para_elem)

        # second, aggregate the distance measures and construct the
        # Paragraph data objects
        para_list: typing.List[Paragraph] = []

        for para_id, para_elem in enumerate(para_bounds):
            sum_dist = [
                sent_dist[sent_id].distance
                for sent_id in para_elem
                ]

            para_list.append(Paragraph(
                para_id = para_id,
                start = para_elem[0],
                end = para_elem[-1],
                distance = sum(sum_dist) / float(len(sum_dist)),
                ))

        return para_list


    def summary (
        self,
        *,
        limit_phrases: int = 10,
        limit_sentences: int = 4,
        preserve_order: bool = False,
        level: str="sentence",
        ) -> typing.Iterator[str]:
        """
Run an
[*extractive summarization*](https://derwen.ai/docs/ptr/glossary/#extractive-summarization),
based on the vector distance (per sentence) for each of the top-ranked phrases.

    limit_phrases:
maximum number of top-ranked phrases to use in the distance vectors

    limit_sentences:
total number of sentences to yield for the extractive summarization

    preserve_order:
flag to preserve the order of sentences as they originally occurred in the source text; defaults to `False`

    level:
default extractive summarization with `"sentence"` value; when set as `"paragraph`" get the average score per paragraph then sort the paragraphs to produce the summary

    yields:
texts for sentences, in order
        """
        # build a list of sentence indices sorted by distance
        sent_dist: typing.List[Sentence] = self.calc_sent_dist(limit_phrases)

        if level == "sentence":
            top_sent_ids: typing.List[int] = [
                sent.sent_id
                for sent in sorted(sent_dist, key=lambda sent: sent.distance)
                ]

            # truncated to the specified limit
            limit = min(limit_sentences, len(top_sent_ids))
            top_sent_ids = top_sent_ids[:limit]

            # optional: sort in ascending order of index to preserve
            # the order in which sentences appear in the original text
            if preserve_order:
                top_sent_ids.sort()

            # extract sentences with the least distance, up to the limit
            # requested
            for sent_id in top_sent_ids:
                yield sent_dist[sent_id].text(self.doc)

        if level == "paragraph":
            top_sent_ids = [
                sent_id
                for p in sorted(self.segment_paragraphs(sent_dist), key=lambda x: x.distance)
                for sent_id in range(p.start, p.end + 1)
            ]

            # truncate to the specified limit
            limit_para = min(limit_sentences, len(top_sent_ids))
            top_sent_ids = top_sent_ids[:limit_para]

            # optional: sort in ascending order of index to preserve
            # the order in which the sentences appear in the original
            # text
            if preserve_order:
                top_sent_ids.sort()

            # extract sentences with the least distance, up to the limit
            # requested
            for sent_id in top_sent_ids:
                yield sent_dist[sent_id].text(self.doc)


    def write_dot (
        self,
        *,
        path: typing.Optional[typing.Union[ str, pathlib.Path ]] = "graph.dot",
        ) -> None:
        """
Serialize the lemma graph in the `Dot` file format.

    path:
path for the output file; defaults to `"graph.dot"`
        """
        dot = graphviz.Graph()

        for lemma in self.lemma_graph.nodes():
            rank = self.ranks[lemma]
            key = lemma.label()

            label = "{} ({:.4f})".format(key, rank)
            dot.node(key, label)

        for edge in self.lemma_graph.edges():
            dot.edge(edge[0].label(), edge[1].label(), constraint="false")

        if isinstance(path, str):
            path = pathlib.Path(path)

        with open(path, "w") as f:  # type: ignore
            f.write(dot.source)


    def plot_keyphrases (
        self
        ) -> typing.Any:
        """
Plot a document's keyphrases rank profile using
[`altair.Chart`](https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html)

Throws an `ImportError` if the `altair` and `pandas` libraries are not installed.

    returns:
the `altair` chart being rendered
        """
        if not _has_altair_and_pandas:
            raise ImportError("altair and pandas are required to use this method. Install them with `pip install 'pytextrank[viz]'`")

        source = pd.DataFrame([p.__dict__ for p in self.doc._.phrases]).drop("chunks", axis=1).reset_index()

        c = (
            alt.Chart(source)
            .mark_bar()
            .encode(x="index", y="rank", color="count", tooltip=["text", "rank", "count"])
            .properties(title="Keyphrase profile of the document")
        )

        return c
