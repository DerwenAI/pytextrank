"""Implements PositionRank."""
from typing import Dict, List, Optional, Tuple

from .base import BaseTextRank, Node, groupby_apply


class PositionRank(BaseTextRank):
    """Implements PositionRank by Florescu, et al. (2017) as a spaCy pipeline component."""

    def get_personalization(self) -> Optional[Dict[Node, float]]:
        """Get node weights for personalised PageRank.

        Returns:
            Biased restart probabilities for PageRank.

        Reference:
            > Specifically, we propose to assign a higher probability to a word
            found on the 2nd position as compared with a word found on the
            50th position in the same document. The weight of each candidate
            word is equal to its inverse position in the document.
            If the same word appears multiple times in the target document,
            then we sum all its position weights.
            For example, a word v_i occurring in the following positions:
            2nd, 5th and 10th, has a weight p(v_i) = 1/2 + 1/5 + 1/10 = 4/5 = 0.8
            The weights of words are normalized before they are used in the
            position-biased PageRank.
        """
        weighted_tokens: List[Tuple[str, float]] = [
            (tok, 1 / (i + 1))
            for i, tok in enumerate(
                token.lemma_ for token in self.doc if token.pos_ in self.pos_kept
            )
        ]

        keyfunc = lambda x: x[0]
        applyfunc = lambda g: sum(w for text, w in g)
        accumulated_weighted_tokens: List[Tuple[str, float]] = groupby_apply(
            weighted_tokens, keyfunc, applyfunc
        )
        accumulated_weighted_tokens = sorted(
            accumulated_weighted_tokens, key=lambda x: x[1]
        )

        norm_weighted_tokens = {
            k: w / sum(w_ for _, w_ in accumulated_weighted_tokens)
            for k, w in accumulated_weighted_tokens
        }

        weighted_nodes = {
            # the authors assign higher probability to a word
            # but our lemma graph vertices are (word, pos) tuples
            # so we map each word weight to all vertices containing that word
            (token.lemma_, token.pos_): norm_weighted_tokens[token.lemma_]
            for token in self.doc
            if token.pos_ in self.pos_kept
        }
        return weighted_nodes
