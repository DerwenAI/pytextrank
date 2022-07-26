#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/pytextrank#license-and-copyright

"""
Implements the *TopicRank* algorithm.
"""

from collections import defaultdict
from functools import lru_cache
import time
import typing

from icecream import ic  # type: ignore # pylint: disable=E0401,W0611 # lgtm[py/unused-import]
from scipy.cluster.hierarchy import fcluster, linkage  # type: ignore # pylint: disable=E0401
from scipy.spatial.distance import pdist  # type: ignore # pylint: disable=E0401
from spacy.tokens import Doc, Span  # type: ignore # pylint: disable=E0401
import networkx as nx  # type: ignore # pylint: disable=E0401

from .base import BaseTextRank, BaseTextRankFactory, Phrase, StopWordsLike


class TopicRankFactory (BaseTextRankFactory):
    """
A factory class that provides the document with its instance of
`TopicRank`
    """

    _CLUSTER_THRESHOLD: float = 0.25
    _CLUSTER_METHOD: str = "average"

    def __init__ (
        self,
        *,
        edge_weight: float = BaseTextRankFactory._EDGE_WEIGHT,
        pos_kept: typing.List[str] = None,
        token_lookback: int = BaseTextRankFactory._TOKEN_LOOKBACK,
        scrubber: typing.Optional[typing.Callable] = None,
        stopwords: typing.Optional[StopWordsLike] = None,
        threshold: float = _CLUSTER_THRESHOLD,
        method: str = _CLUSTER_METHOD,
        ) -> None:
        """
Constructor for the factory class.
        """
        super().__init__(
            edge_weight=edge_weight,
            pos_kept=pos_kept,
            token_lookback=token_lookback,
            scrubber=scrubber,
            stopwords=stopwords,
        )

        # TopicRank clustering parameters
        self.threshold: float = threshold
        self.method: str = method


    def __call__ (
        self,
        doc: Doc,
        ) -> Doc:
        """
Set the extension attributes on a `spaCy` [`Doc`](https://spacy.io/api/doc)
document to create a *pipeline component* for `TopicRank` as
a stateful component, invoked when the document gets processed.

See: <https://spacy.io/usage/processing-pipelines#pipelines>

    doc:
a document container, providing the annotations produced by earlier stages of the `spaCy` pipeline
        """
        Doc.set_extension("textrank", force=True, default=None)
        Doc.set_extension("phrases", force=True, default=[])

        doc._.textrank = TopicRank(
            doc,
            edge_weight=self.edge_weight,
            pos_kept=self.pos_kept,
            token_lookback=self.token_lookback,
            scrubber=self.scrubber,
            stopwords=self.stopwords,
            threshold=self.threshold,
            method=self.method,
        )

        doc._.phrases = doc._.textrank.calc_textrank()
        return doc


class TopicRank (BaseTextRank):
    """
Implements the *TopicRank* algorithm described by
[[bougouin-etal-2013-topicrank]](https://derwen.ai/docs/ptr/biblio/#bougouin-etal-2013-topicrank)
deployed as a `spaCy` pipeline component.

This class does not get called directly; instantiate its factory
instead.

Algorithm Overview:

1. Preprocessing: Sentence segmentation, word tokenization, POS tagging.
   After this stage, we have preprocessed text.
2. Candidate extraction: Extract sequences of nouns and adjectives (i.e. noun chunks)
   After this stage, we have a list of keyphrases that may be topics.
3. Candidate clustering: Hierarchical Agglomerative Clustering algorithm with average
   linking using simple set-based overlap of lemmas. Similarity is achieved at > 25%
   overlap. **Note**: PyTextRank deviates from the original algorithm here, which uses
   stems rather than lemmas.
   After this stage, we have a list of topics.
4. Candidate ranking: Apply *TextRank* on a complete graph, with topics as nodes
   (i.e. clusters derived in the last step), where edge weights are higher between
   topics that appear closer together within the document.
   After this stage, we have a ranked list of topics.
5. Candidate selection: Select the first occurring keyphrase from each topic to
   represent that topic.
   After this stage, we have a ranked list of topics, with a keyphrase to represent
   the topic.
    """

    def __init__(
        self,
        doc: Doc,
        edge_weight: float,
        pos_kept: typing.List[str],
        token_lookback: int,
        scrubber: typing.Callable,
        stopwords: typing.Dict[str, typing.List[str]],
        threshold: float,
        method: str,
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

    threshold:
threshold used in *TopicRank* candidate clustering; the original algorithm uses 0.25

    method:
clustering method used in *TopicRank* candidate clustering: see [`scipy.cluster.hierarchy.linkage`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html) for valid methods; the original algorithm uses "average"
        """
        super().__init__(
            doc, edge_weight, pos_kept, token_lookback, scrubber, stopwords
        )

        # TopicRank candidate clustering parameters
        self.threshold: float = threshold
        self.method: str = method


    def _cluster (
        self,
        candidates: typing.List[Span],
        ) -> typing.List[typing.List[Span]]:
        """
Cluster candidates using Hierarchical Agglomerative Clustering (HAC),
where similarity is defined by overlap of lemmas in candidates.

The `threshold` and `method` parameters influence the clustering
behaviour. A `threshold` of 0.25 means that there must at least be
a 25% overlap of lemmas between two candidates for them to be allowed
in the same cluster.

    candidates:
list of spans, where each span is a candidate topic.

    returns:
list of clusters of candidates.
        """
        if not candidates:
            return []

        bag_of_words = list(
            {
                word.text
                for candidate in candidates
                for word in candidate
                if not word.is_stop
            }
        )

        # Create a bag-of-words representation with a
        # |candidates|x|bag_of_words| matrix
        # matrix = [[0] * len(bag_of_words) for _ in candidates]
        matrix = []

        for candidate in candidates:
            matrix.append([0] * len(bag_of_words))

            for term in candidate:
                if not term.is_stop:
                    try:
                        matrix[-1][bag_of_words.index(term.text)] += 1
                    except IndexError:
                        pass

        # Apply average clustering on pairwise distance,
        # using a threshold of 0.01 below 1 - threshold.
        # So, 0.74 for the default 0.25 threshold.
        pairwise_dist = pdist(matrix, "jaccard")

        if not pairwise_dist.size:
            return [[candidate] for candidate in candidates]

        raw_clusters = linkage(pairwise_dist, method=self.method)
        cluster_ids = fcluster(
            raw_clusters, t=0.99 - self.threshold, criterion="distance"
        )

        # Map cluster_ids to the corresponding candidates, and then
        # ignore the cluster id keys.
        clusters = defaultdict(list)

        for cluster_id, candidate in zip(cluster_ids, candidates):
            clusters[cluster_id].append(candidate)

        return list(clusters.values())


    def _get_candidates (
        self
        ) -> typing.List[Span]:
        """
Return a list of spans with candidate topics, such that the start of
each candidate is a noun chunk that was trimmed of stopwords or tokens
with POS tags that we wish to ignore.

    returns:
list of candidate spans
        """
        candidates: typing.List[Span] = []

        try:
            noun_chunks = list(self.doc.noun_chunks)

            for chunk in noun_chunks:
                for token in chunk:
                    if self._keep_token(token):
                        candidates.append(self.doc[token.i : chunk.end])
                        break
        except NotImplementedError as ex:
            # some languages don't have `noun_chunks` support in spaCy models, e.g. "ru"
            ic.disable()
            ic(ex)
            ic.enable()

        return candidates


    @property  # type: ignore
    @lru_cache(maxsize=1)
    def node_list (  # type: ignore
        self
        ) -> typing.List[typing.Tuple[Span, ...]]:
        """
Build a list of vertices for the graph, cached for efficiency.

    returns:
list of nodes
        """
        # Rely on spaCy to perform *preprocessing* and *candidate extraction*
        # through ``noun_chunks``, thus completing the first two steps of
        # the *TopicRank* algorithm.
        candidates = self._get_candidates()

        # Cluster candidates together using a simple set-based overlap of
        # lemmas. Clustering can occur if the overlap is more than 25%.
        # Map to a tuple so these clusters are hashable.
        clustered = [tuple(cluster) for cluster in self._cluster(candidates)]

        return clustered


    @property
    def edge_list (  # type: ignore
        self,
        ) -> typing.List[typing.Tuple[typing.List[Span], typing.List[Span], typing.Dict[str, float]]]:
        """
Build a list of weighted edges for the graph.

    returns:
list of weighted edges
        """
        weighted_edges = []

        for i, source_topic in enumerate(self.node_list):  # type: ignore
            for target_topic in self.node_list[i + 1 :]:  # type: ignore
                weight = 0.0

                for source_member in source_topic:
                    for target_member in target_topic:
                        distance = abs(source_member.start - target_member.start)

                        if distance:
                            weight += 1.0 / distance

                weight_dict = {"weight": weight * self.edge_weight}
                weighted_edges.append((source_topic, target_topic, weight_dict))
                weighted_edges.append((target_topic, source_topic, weight_dict))

        return weighted_edges


    def calc_textrank (
        self
        ) -> typing.List[Phrase]:
        """
Construct a complete graph using potential topics as nodes,
then apply the *TextRank* algorithm to return the top-ranked phrases.

This method represents the heart of the *TopicRank* algorithm.

    returns:
list of ranked phrases, in descending order
        """
        t0 = time.time()
        self.reset()

        # for *TopicRank*, the constructed graph is complete
        # with topics as nodes and a distance measure between
        # two topics as the weights for the edge between them.
        self.lemma_graph = self._construct_graph()

        # to run the algorithm, we use the NetworkX implementation
        # for PageRank (i.e., based on eigenvector centrality)
        # to calculate a rank for each node in the lemma graph
        self.ranks: typing.Dict[typing.List[Span], float] = nx.pagerank(  # type: ignore
            self.lemma_graph,
            personalization=self.get_personalization(),
        )

        # we convert the topics into a list of Phrases,
        # such that the Phrase text is the first occurring
        # candidate keyphrase of that topic.
        # The chunks correspond to the topic clustering, the
        # rank is simply the TextRank score, and the count is
        # the number candidate keyphrases that make up the topic.
        raw_phrase_list = [
            Phrase(
                text=self.scrubber(
                    # get first occurring keyphrase for topic
                    min(
                        ((keyphrase, keyphrase.start) for keyphrase in topic),
                        key=lambda tup: tup[1],
                    )[0]
                ),
                chunks=list(topic),
                count=len(topic),
                rank=score,
            )
            for topic, score in self.ranks.items()
        ]

        phrase_list: typing.List[Phrase] = sorted(
            raw_phrase_list, key=lambda p: p.rank, reverse=True
        )

        t1 = time.time()
        self.elapsed_time = (t1 - t0) * 1000.0

        return phrase_list


    def reset (
        self
        ) -> None:
        """
Reinitialize the data structures needed for extracting phrases,
removing any pre-existing state.
        """
        super().reset()
        TopicRank.node_list.fget.cache_clear()  # type: ignore # pylint: disable=E1101
