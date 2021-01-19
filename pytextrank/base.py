"""Implements TextRank, with placeholder for bias."""
import itertools
import math
from collections import Counter
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import networkx as nx
from spacy.tokens import Doc, Span


def groupby_apply(data: Iterable[Any], keyfunc: Callable, applyfunc: Callable) -> List[Tuple[Any, Any]]:
    """Groupby a key and apply function without pandas dependency.

    Arguments:
        data: iterable
        keyfunc: callable to define the key by which you want to group
        applyfunc: callable to apply to the group

    Returns:
        Iterable with accumulated values.

    Ref: https://docs.python.org/3/library/itertools.html#itertools.groupby
    """
    data = sorted(data, key=keyfunc)
    return [(k, applyfunc(g)) for k, g in itertools.groupby(data, keyfunc)]


@dataclass
class Phrase:
    """Holds data for extracted keyphrase."""

    text: str
    rank: float
    count: int
    chunks: List[Span]


Node = Tuple[str, str]  # (lemma, pos)


class BaseTextRank:
    """Implements TextRank by Milhacea, et al., as a spaCy pipeline component."""

    _EDGE_WEIGHT = 1.0
    _POS_KEPT = ["ADJ", "NOUN", "PROPN", "VERB"]
    _TOKEN_LOOKBACK = 3

    def __init__(
        self,
        edge_weight: float = _EDGE_WEIGHT,
        pos_kept: List[str] = _POS_KEPT,
        scrubber: Callable = str.strip,
        token_lookback: int = _TOKEN_LOOKBACK,
    ):
        self.edge_weight = edge_weight
        self.pos_kept = pos_kept
        self.scrubber = scrubber
        self.token_lookback = token_lookback

        self.doc = None

    def __call__(self, doc: Doc) -> Doc:
        """Run the spaCy pipeline component on the document."""
        self.doc = doc
        Doc.set_extension("phrases", force=True, default=[])
        Doc.set_extension("textrank", force=True, default=self)
        doc._.phrases = self.calc_textrank()
        return doc

    def calc_textrank(self) -> List[Phrase]:
        """Construct lemma graph and return top-ranked phrases."""
        lemma_graph = self.construct_graph()

        pagerank_personalization = self.get_personalization()

        ranks: Dict[Node, float] = nx.pagerank(
            lemma_graph, personalization=pagerank_personalization
        )

        nc_phrases = self.collect_phrases(self.doc.noun_chunks, ranks)
        ent_phrases = self.collect_phrases(self.doc.ents, ranks)
        all_phrases = {**nc_phrases, **ent_phrases}

        phrase_list: List[Phrase] = self.get_min_phrases(all_phrases)

        return sorted(phrase_list, key=lambda p: p.rank, reverse=True)

    def construct_graph(self) -> nx.Graph:
        """Construct lemma graph."""
        G = nx.Graph()
        # add nodes made of (lemma, pos)
        G.add_nodes_from(self.node_list)
        # add edges between nodes co-occuring within a window, weighted by the count
        G.add_edges_from(self.edge_list)
        return G

    @property
    def node_list(self) -> List[Tuple[str, str]]:
        """Build list of vertices for the lemma graph."""
        nodes = [
            (token.lemma_, token.pos_)
            for token in self.doc
            if token.pos_ in self.pos_kept
        ]
        return nodes

    @property
    def edge_list(self) -> List[Tuple[Node, Node, Dict[str, float]]]:
        """Build list of weighted edges  for the lemma graph."""
        edges: List[Tuple[Node, Node]] = []
        for sent in self.doc.sents:
            H = [
                (token.lemma_, token.pos_)
                for token in sent
                if token.pos_ in self.pos_kept
            ]
            for hop in range(self.token_lookback):
                for idx, node in enumerate(H[: -1 - hop]):
                    nbor = H[hop + idx + 1]
                    edges.append((node, nbor))

        # Include weight on the edge: (2, 3, {'weight': 3.1415})
        weighted_edges = [
            (*n, {"weight": w * self.edge_weight}) for n, w in Counter(edges).items()
        ]
        return weighted_edges

    def get_personalization(self) -> Optional[Dict[Node, float]]:
        """Get node weights for personalised PageRank."""
        pass

    def collect_phrases(
        self, spans: Iterable[Span], ranks: Dict[Node, float]
    ) -> Dict[Span, float]:
        """Aggregate ranks of individual tokens within phrases."""
        phrases = {
            span: sum(
                ranks[(token.lemma_, token.pos_)]
                for token in span
                if token.pos_ in self.pos_kept
            )
            for span in spans
        }
        return {
            span: self._calc_discounted_normalised_rank(span, sum_rank)
            for span, sum_rank in phrases.items()
        }

    def _calc_discounted_normalised_rank(self, span: Span, sum_rank: float) -> float:
        """Since the noun chunking is greedy, we discount the ranks using a
        point estimate based on the number of non-lemma tokens within a phrase.
        """
        non_lemma = len([tok for tok in span if tok.pos_ not in self.pos_kept])

        non_lemma_discount = len(span) / (len(span) + (2.0 * non_lemma) + 1.0)

        # use root mean square (RMS) to normalize the contributions of all the tokens
        phrase_rank = math.sqrt(sum_rank / (len(span) + non_lemma))

        return phrase_rank * non_lemma_discount

    def get_min_phrases(self, all_phrases: Dict[Span, float]) -> List[Phrase]:
        """Group phrases by text, get max rank and collect spans in a list."""
        data = [
            (self.scrubber(span.text), rank, span) for span, rank in all_phrases.items()
        ]

        keyfunc = lambda x: x[0]
        applyfunc = lambda g: list((rank, spans) for text, rank, spans in g)
        phrases: List[Tuple[str, List[Tuple[float, Span]]]] = groupby_apply(
            data, keyfunc, applyfunc
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
