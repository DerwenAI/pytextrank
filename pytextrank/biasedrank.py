"""
Implements the *BiasedTextrank* algorithm.
"""
import time

from spacy.tokens import Doc, Span, Token  # type: ignore
import typing
import networkx as nx  # type: ignore

from .base import BaseTextRankFactory, BaseTextRank, Lemma, Phrase, Sentence
from .util import groupby_apply


class BiasedTextRankFactory (BaseTextRankFactory):
    """
A factory class that provides the document with its instance of
`PositionRank`
    """


    def __call__ (
        self,
        doc: Doc,
        ) -> Doc:
        """
Set the extension attributes on a `spaCy` [`Doc`](https://spacy.io/api/doc)
document to create a *pipeline component* for `PositionRank` as
a stateful component, invoked when the document gets processed.

See: <https://spacy.io/usage/processing-pipelines#pipelines>

    doc:
a document container, providing the annotations produced by earlier stages of the `spaCy` pipeline
        """
        Doc.set_extension("textrank", force=True, default=None)
        Doc.set_extension("phrases", force=True, default=[])

        doc._.textrank = BiasedTextRank(
            doc,
            edge_weight = self.edge_weight,
            pos_kept = self.pos_kept,
            token_lookback = self.token_lookback,
            scrubber = self.scrubber,
            stopwords = self.stopwords,
            )

        return doc


class BiasedTextRank(BaseTextRank):
    """
Implements the *PositionRank* algorithm described by
[[florescuc17]](https://derwen.ai/docs/ptr/biblio/#florescuc17),
deployed as a `spaCy` pipeline component.

This class does not get called directly; instantiate its factory
instead.
    """


    def get_personalization (
        self, focus=None, bias=1
        ) -> typing.Optional[typing.Dict[Lemma, float]]:
        """
        Get the *node weights* for initializing the use of the
        [*Personalized PageRank*](https://derwen.ai/docs/ptr/glossary/#personalized-pagerank)
        algorithm.

            returns:
        Biased restart probabilities to use in the *PageRank* algorithm.
        """
        focus_tokens = focus.lower().split(" ")
        # assign bias to focus nodes while 1 to other nodes
        weighted_nodes = {
            Lemma(token.lemma_, token.pos_): bias if token.text in focus_tokens or token.lemma_ in focus_tokens else 1
            for token in self.doc
            if token.pos_ in self.pos_kept
        }

        # normalize weights
        total_weight = sum([weight for weight in weighted_nodes.values()])
        if total_weight ==0:
            return None
        normalized_weighted_nodes = {lemma : weight/total_weight for lemma, weight in weighted_nodes.items()}

        # print(f"normalized_weighted_nodes: {normalized_weighted_nodes}")
        return normalized_weighted_nodes

    def calc_textrank(
                self,
            focus="",
            bias=1
        ):
            """
    Iterate through each sentence in the doc, constructing a
    [*lemma graph*](https://derwen.ai/docs/ptr/glossary/#lemma-graph)

    This method represents the heart of the *TextRank* algorithm.

        returns: None
            """
            t0 = time.time()
            self.reset()
            self.lemma_graph = self._construct_graph()

            # to run the algorithm, we use the NetworkX implementation
            # of PageRank (i.e., approximating eigenvalue centrality)
            # to calculate a rank for each node in the lemma graph
            personalization = self.get_personalization(focus, bias)
            self.ranks = nx.pagerank(
                self.lemma_graph,
                personalization=personalization,
            )

            # agglomerate the lemmas ranked in the lemma graph into ranked
            # phrases, leveraging information from earlier stages of the
            # pipeline: noun chunks and named entities

            nc_phrases: typing.Dict[Span, float] = self._collect_phrases(self.doc.noun_chunks, self.ranks)
            ent_phrases: typing.Dict[Span, float] = self._collect_phrases(self.doc.ents, self.ranks)
            all_phrases: typing.Dict[Span, float] = {**nc_phrases, **ent_phrases}

            # since noun chunks can be expressed in different ways (e.g., may
            # have articles or prepositions), we need to find a minimum span
            # for each phrase based on combinations of lemmas
            raw_phrase_list: typing.List[Phrase] = self._get_min_phrases(all_phrases)
            phrase_list: typing.List[Phrase] = sorted(raw_phrase_list, key=lambda p: p.rank, reverse=True)

            t1 = time.time()
            self.elapsed_time = (t1 - t0) * 1000.0
            self.phrases = phrase_list

    def get_phrases(self, focus="", bias=1) -> typing.List[Phrase]:
        """
        returns:
        list of ranked phrases, in descending order
        """
        t0 = time.time()
        # calculate textrank
        self.calc_textrank(focus, bias)
        return self.phrases


    def summary (
        self,
        *,
        focus="",
        bias=1,
        limit_phrases: int = 10,
        limit_sentences: int = 4,
        preserve_order: bool = False,
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

    yields:
texts for sentences, in order
        """
        # calculate textrank
        self.calc_textrank(focus, bias)

        # build a list of sentence indices sorted by distance
        sent_dist: typing.List[Sentence] = self.calc_sent_dist(limit_phrases)

        top_sent_ids: typing.List[int] = [
            sent.sent_id
            for sent in sorted(sent_dist, key=lambda sent: sent.distance)
            ]

        # truncated to the specified limit
        limit = min(limit_sentences, len(top_sent_ids))
        top_sent_ids = top_sent_ids[:limit]

        # optional: sort in ascending order of index to preserve the
        # order in which sentences appear in the original text
        if preserve_order:
            top_sent_ids.sort()

        # extract sentences with the least distance, up to the limit
        # requested
        for sent_id in top_sent_ids:
            yield sent_dist[sent_id].text(self.doc)
