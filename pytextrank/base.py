#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Implements the base class for TextRank, with placeholder methods for
use by subclasses for algorithm extensions.
"""

from .util import groupby_apply, default_scrubber

from collections import Counter, defaultdict, OrderedDict
from dataclasses import dataclass
from icecream import ic  # type: ignore
from spacy.tokens import Doc, Span, Token  # type: ignore
import graphviz  # type: ignore
import json
import math
import networkx as nx  # type: ignore
import pathlib
import time
import typing


@dataclass
class Phrase:
    """
Represents one extracted phrase.
    """
    text: str
    rank: float
    count: int
    chunks: typing.List[Span]


Node = typing.Tuple[str, str]  # (lemma, pos)
PhraseLike = typing.List[typing.Tuple[str, typing.List[typing.Tuple[float, Span]]]]


class BaseTextRank:
    """
Implements TextRank by Mihalcea, et al., as a spaCy pipeline component.
    """

    _EDGE_WEIGHT = 1.0
    _POS_KEPT = ["ADJ", "NOUN", "PROPN", "VERB"]
    _TOKEN_LOOKBACK = 3


    def __init__ (
        self,
        edge_weight: float = _EDGE_WEIGHT,
        pos_kept: typing.List[str] = _POS_KEPT,
        token_lookback: int = _TOKEN_LOOKBACK,
        scrubber: typing.Optional[typing.Callable] = None,
        ) -> None:
        """
Constructor for a `TextRank` object

    edge_weight:
default weight for an edge

    pos_kept:
parts of speech tags to be kept; adjust this if strings representing
the POS tags change

    token_lookback:
the window for neighboring tokens (similar to a skip gram)

    scrubber:
optional "scrubber" function to clean up punctuation from a token; if `None` then defaults to `pytextrank.default_scrubber`
        """
        self.edge_weight = edge_weight
        self.pos_kept = pos_kept
        self.token_lookback = token_lookback

        if not scrubber:
            self.scrubber = default_scrubber
        else:
            self.scrubber = scrubber


        self.doc: Doc = None
        self.stopwords: dict = defaultdict(list)
        self.reset()


    def __call__ (
        self,
        doc: Doc,
        ) -> Doc:
        """
Set the extension attributes on a spaCy[`Doc`](https://spacy.io/api/doc) 
document to create a *pipeline component factory* for `TextRank` as 
a stateful component, when the document gets processed.
See: <https://spacy.io/usage/processing-pipelines#pipelines>

    doc:
the document container for accessing linguistic annotations
        """
        self.doc = doc

        Doc.set_extension("phrases", force=True, default=[])
        Doc.set_extension("textrank", force=True, default=self)
        doc._.phrases = self.calc_textrank()

        return doc


    def reset (
        self
        ) -> None:
        """
Initialize the data structures needed for extracting phrases, removing
any pre-existing state.
        """
        self.elapsed_time = 0.0
        self.lemma_graph = nx.DiGraph()
        self.phrases: dict = defaultdict(list)
        self.ranks: typing.Dict[Node, float] = {}
        self.seen_lemma: typing.Dict[Node, typing.Set[int]] = OrderedDict()


    def load_stopwords (
        self,
        data: typing.Optional[typing.Dict[str, typing.List[str]]] = None,
        path: typing.Optional[pathlib.Path] = None,
        ) -> None:
        """
Load a dictionary of *stop words* for tokens to be ignored when
constructing the lemma graph.

Note: be cautious when using this feature, it can get "greedy" and
bias/distort the results.

    data:
dictionary of `lemma: [pos]` items to define the stop words, where
each item has a key as a lemmatized token and a value as a list of POS
tags

    path:
optional [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html) 
of a JSON file – in lieu of providing a `data` parameter
        """
        if data:
            self.stopwords = data
        elif path and path.exists():
            with open(path, "r") as f:
                data = json.load(f)

                if data:
                    for lemma, pos_list in data.items():
                        self.stopwords[lemma] = pos_list


    def calc_textrank (
        self
        ) -> typing.List[Phrase]:
        """
Iterate through each sentence in the doc, constructing a lemma graph
then returning the top-ranked phrases.

This method represents the heart of the algorithm implementation.

    returns:
list of ranked phrases, in descending order
        """
        self.reset()
        t0 = time.time()

        self.lemma_graph = self._construct_graph()

        # to run the algorithm, we use the NetworkX implementation
        # of PageRank (i.e., approximating eigenvalue centrality)
        # to calculate a rank for each node in the lemma graph

        self.ranks = nx.pagerank(
            self.lemma_graph,
            personalization=self.get_personalization(),
        )

        # collect the top-ranked phrases based on both the noun chunks
        # and the named entities

        nc_phrases = self._collect_phrases(self.doc.noun_chunks, self.ranks)
        ent_phrases = self._collect_phrases(self.doc.ents, self.ranks)
        all_phrases = { **nc_phrases, **ent_phrases }

        # since noun chunks can be expressed in different ways (e.g., may
        # have articles or prepositions), we need to find a minimum span
        # for each phrase based on combinations of lemmas

        raw_phrase_list: typing.List[Phrase] = self._get_min_phrases(all_phrases)
        phrase_list = sorted(raw_phrase_list, key=lambda p: p.rank, reverse=True)

        t1 = time.time()
        self.elapsed_time = (t1 - t0) * 1000.0

        return phrase_list


    def get_personalization (
        self
        ) -> typing.Optional[typing.Dict[Node, float]]:
        """
Get the node weights for use in Personalized PageRank.
Defaults to no-op.

    returns:
`None`
        """
        return None


    def _construct_graph (
        self
        ) -> nx.DiGraph:
        """
Construct the lemma graph.

    returns:
a directed graph representing the lemma graph
        """
        g = nx.DiGraph()

        # add nodes made of (lemma, pos)
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
a parsed spaCy [`Token`](https://spacy.io/api/token) to be evaluated

    returns:
boolean value for whether to keep this token as a node in the lemma
graph
        """
        lemma = token.lemma_.lower().strip()

        if lemma in self.stopwords and token.pos_ in self.stopwords[lemma]:
            return False
        elif token.pos_ not in self.pos_kept:
            return False
        else:
            # also track occurrence of this token's lemma, for later use
            key = (lemma, token.pos_,)

            if key not in self.seen_lemma:
                self.seen_lemma[key] = set([token.i])
            else:
                self.seen_lemma[key].add(token.i)

            return True


    @property
    def node_list (
        self
        ) -> typing.List[typing.Tuple[str, str]]:
        """
Build a list of vertices for the lemma graph.

    returns:
list of nodes
        """
        nodes = [
            (token.lemma_, token.pos_)
            for token in self.doc
            if self._keep_token(token)
        ]

        return nodes


    @property
    def edge_list (
        self
        ) -> typing.List[typing.Tuple[Node, Node, typing.Dict[str, float]]]:
        """
Build a list of weighted edges for the lemma graph.

    returns:
list of weighted edges
        """
        edges: typing.List[typing.Tuple[Node, Node]] = []

        for sent in self.doc.sents:
            h = [
                (token.lemma_, token.pos_)
                for token in sent
                if self._keep_token(token)
            ]

            for hop in range(self.token_lookback):
                for idx, node in enumerate(h[: -1 - hop]):
                    nbor = h[hop + idx + 1]
                    edges.append((node, nbor))

        # include weight on the edge: (2, 3, {'weight': 3.1415})
        weighted_edges = [
            (*n, {"weight": w * self.edge_weight}) for n, w in Counter(edges).items()
        ]

        return weighted_edges


    def _collect_phrases (
        self,
        spans: typing.Iterable[Span],
        ranks: typing.Dict[Node, float]
        ) -> typing.Dict[Span, float]:
        """
Aggregate the rank metrics of the individual nodes (tokens) within
each phrase.

    spans:
spans of noun chuncks

    ranks:
rank metrics corresponding to each node

    returns:
phrases extracted from the lemma graph, each with an aggregate rank
metric
        """
        phrases = {
            span: sum(
                ranks[(token.lemma_, token.pos_)]
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
span representing one phrase

    sum_rank:
sum of the ranks for each token within this span

    returns:
normalized rank metric
        """
        non_lemma = len([tok for tok in span if tok.pos_ not in self.pos_kept])
        non_lemma_discount = len(span) / (len(span) + (2.0 * non_lemma) + 1.0)

        # use a root mean square (RMS) to normalize the contributions
        # of all the tokens
        phrase_rank = math.sqrt(sum_rank / (len(span) + non_lemma))

        return phrase_rank * non_lemma_discount


    def _get_min_phrases (
        self,
        all_phrases: typing.Dict[Span, float]
        ) -> typing.List[Phrase]:
        """
Group the phrases by their text content, select the span with the
maximum rank within each group, then collect the ranked phrases into
an ordered list.

    all_phrases:
raw phrase list

    returns:
ordered list of ranked phrases
        """
        data = [
            (self.scrubber(span.text), rank, span) for span, rank in all_phrases.items()
        ]

        keyfunc = lambda x: x[0]
        applyfunc = lambda g: list((rank, spans) for text, rank, spans in g)

        phrases: PhraseLike = groupby_apply(
            data,
            keyfunc,
            applyfunc,
        )

        phrase_list = [
            Phrase(
                text=p[0],
                rank=max(rank for rank, span in p[1]),
                count=len(p[1]),
                chunks=list(span for rank, span in p[1]),
            )
            for p in phrases
        ]

        return phrase_list


    def summary (
        self,
        limit_phrases=10,
        limit_sentences=4,
        preserve_order=False
        ):
        """
Run extractive summarization, based on the vector distance (per
sentence) for each of the top-ranked phrases.

    limit_phrases:
maximum number of top-ranked phrases to use in the distance vectors

    limit_sentences:
total number of sentences to yield for the extractive summary

    preserve_order:
flag to preserve the order of sentences as they originally occurred in
the source text; defaults to `False`

    yields:
texts for sentences, in order
        """
        unit_vector = []

        # construct a list of sentence boundaries with a phrase set
        # for each (initialized to empty)

        sent_bounds = [ [s.start, s.end, set([])] for s in self.doc.sents ]

        # iterate through the top-ranked phrases, adding them to the
        # phrase vector for each sentence

        phrase_id = 0

        for p in self.doc._.phrases:
            unit_vector.append(p.rank)

            for chunk in p.chunks:
                for sent_start, sent_end, sent_vector in sent_bounds:
                    if chunk.start >= sent_start and chunk.start <= sent_end:
                        sent_vector.add(phrase_id)
                        break

            phrase_id += 1

            if phrase_id == limit_phrases:
                break

        # construct a unit_vector for the top-ranked phrases, up to
        # the requested limit

        sum_ranks = sum(unit_vector)

        try:
            unit_vector = [ rank/sum_ranks for rank in unit_vector ]
        except ZeroDivisionError:
            unit_vector = (0.0,) * len(unit_vector)

        # iterate through each sentence, calculating its euclidean
        # distance from the unit vector

        sent_rank = {}
        sent_id = 0

        for sent_start, sent_end, sent_vector in sent_bounds:
            sum_sq = 0.0
    
            for phrase_id in range(len(unit_vector)):
                if phrase_id not in sent_vector:
                    sum_sq += unit_vector[phrase_id]**2.0

            sent_rank[sent_id] = math.sqrt(sum_sq)
            sent_id += 1

        # extract the sentences with the lowest distance

        sent_text = {}
        sent_id = 0

        for sent in self.doc.sents:
            sent_text[sent_id] = sent
            sent_id += 1

        # build a list of sentence indices, sorted according to their
        # corresponding rank

        top_sent_ids = list(range(len(sent_rank)))
        top_sent_ids.sort(key=lambda sent_id: sent_rank[sent_id])

        # truncate to the given limit

        top_sent_ids = top_sent_ids[:limit_sentences]

        # sort in ascending order of index to preserve the order in
        # which the sentences appear in the original text

        if preserve_order:
            top_sent_ids.sort()

        # yield results, up to the limit requested

        for sent_id in top_sent_ids:
            yield sent_text[sent_id]


    def write_dot (
        self,
        path="graph.dot"
        ) -> None:
        """
Serialize the lemma graph in the `Dot` file format.

    path:
path for the output file; defaults to `"graph.dot"`
        """
        dot = graphviz.Digraph()

        for lemma, pos in self.lemma_graph.nodes():
            node_key = (lemma, pos,)
            rank = self.ranks[node_key]

            label = "{} ({:.4f})".format(lemma, rank)
            dot.node(str(node_key), label)

        for edge in self.lemma_graph.edges():
            dot.edge(str(edge[0]), str(edge[1]), constraint="false")

        with open(path, "w") as f:
            f.write(dot.source)
