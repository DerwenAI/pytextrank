from collections import defaultdict, Counter
from dataclasses import dataclass
import itertools
import math
from typing import List, Tuple, Dict, Iterable, Set, Optional

import networkx as nx
from spacy.tokens import Doc, Span


@dataclass
class Phrase:
    text: str
    rank: float
    count: int
    phrase_list: List[Span]


Node = Tuple[str, str]  # (lemma, pos)


class BaseTextRank:
    _EDGE_WEIGHT = 1.0
    _POS_KEPT = ["ADJ", "NOUN", "PROPN", "VERB"]
    _TOKEN_LOOKBACK = 3

    def __init__(
        self,
        edge_weight=_EDGE_WEIGHT,
        pos_kept=_POS_KEPT,
        scrubber=str.strip,
        token_lookback=_TOKEN_LOOKBACK,
    ):
        self.edge_weight = edge_weight
        self.pos_kept = pos_kept
        self.scrubber = scrubber
        self.token_lookback = token_lookback

        self.doc = None

    def __call__(self, doc: Doc) -> Doc:
        """Call the inner EntityRuler."""
        self.doc = doc
        Doc.set_extension("phrases", force=True, default=[])
        Doc.set_extension("textrank", force=True, default=self)
        doc._.phrases = self.calc_textrank()
        return doc

    def calc_textrank(self) -> List[Phrase]:
        lemma_graph = self.construct_graph()

        pagerank_personalization = self.get_personalization()

        ranks: Dict[str, float] = nx.pagerank(
            lemma_graph, personalization=pagerank_personalization
        )

        nc_phrases = self.collect_phrases(self.doc.noun_chunks, ranks)
        ent_phrases = self.collect_phrases(self.doc.ents, ranks)
        all_phrases = {**nc_phrases, **ent_phrases}

        phrase_list: List[Phrase] = self.get_min_phrases(all_phrases)

        return sorted(phrase_list, key=lambda p: p.rank, reverse=True)

    def construct_graph(self) -> nx.Graph:
        G = nx.Graph()
        # add nodes made of (lemma, pos)
        G.add_nodes_from(self.node_list)
        # add edges between nodes co-occuring within a window, weighted by the count
        G.add_edges_from(self.edge_list)
        return G

    @property
    def node_list(self) -> List[Tuple[str, str]]:
        nodes = [
            (token.lemma_, token.pos_)
            for token in self.doc
            if token.pos_ in self.pos_kept
        ]
        return nodes

    @property
    def edge_list(self) -> List[Tuple[Node, Node, Dict[str, float]]]:
        edges = []
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
        edges = [
            (*n, dict(weight=w * self.edge_weight)) for n, w in Counter(edges).items()
        ]
        return edges

    def get_personalization(self) -> Optional[Dict[Node, float]]:
        return None

    def collect_phrases(
        self, spans: Iterable[Span], ranks: Dict[str, float]
    ) -> Dict[Span, float]:
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
        non_lemma = len([tok for tok in span if tok.pos_ not in self.pos_kept])

        # although the noun chunking is greedy, we discount the ranks using a
        # point estimate based on the number of non-lemma tokens within a phrase
        non_lemma_discount = len(span) / (len(span) + (2.0 * non_lemma) + 1.0)

        # use root mean square (RMS) to normalize the contributions of all the tokens
        phrase_rank = math.sqrt(sum_rank / (len(span) + non_lemma))

        return phrase_rank * non_lemma_discount

    def get_min_phrases(self, all_phrases=Dict[Span, float]) -> List[Phrase]:
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
                phrase_list=list(span for rank, span in p[1]),
            )
            for p in phrases
        ]
        return phrase_list


def groupby_apply(data, keyfunc, applyfunc):
    """Groupby a key and sum without pandas dependency.

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
