#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/pytextrank#license-and-copyright

"""
Implements the *PositionRank* algorithm.
"""

import typing

from spacy.tokens import Doc  # type: ignore # pylint: disable=E0401

from .base import BaseTextRankFactory, BaseTextRank, Lemma
from .util import groupby_apply


class PositionRankFactory (BaseTextRankFactory):
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

        doc._.textrank = PositionRank(
            doc,
            edge_weight = self.edge_weight,
            pos_kept = self.pos_kept,
            token_lookback = self.token_lookback,
            scrubber = self.scrubber,
            stopwords = self.stopwords,
            )

        doc._.phrases = doc._.textrank.calc_textrank()
        return doc


class PositionRank (BaseTextRank):
    """
Implements the *PositionRank* algorithm described by
[[florescuc17]](https://derwen.ai/docs/ptr/biblio/#florescuc17),
deployed as a `spaCy` pipeline component.

This class does not get called directly; instantiate its factory
instead.
    """

    def get_personalization (
        self
        ) -> typing.Optional[typing.Dict[Lemma, float]]:
        """
Get the *node weights* for initializing the use of the
[*Personalized PageRank*](https://derwen.ai/docs/ptr/glossary/#personalized-pagerank)
algorithm.

From the cited reference:

> Specifically, we propose to assign a higher probability to a word
> found on the 2nd position as compared with a word found on the 50th
> position in the same document. The weight of each candidate word is
> equal to its inverse position in the document.  If the same word
> appears multiple times in the target document, then we sum all its
> position weights.

> For example, a word v_i occurring in the following positions: 2nd,
> 5th and 10th, has a weight p(v_i) = 1/2 + 1/5 + 1/10 = 4/5 = 0.8
> The weights of words are normalized before they are used in the
> position-biased PageRank.

    returns:
Biased restart probabilities to use in the *PageRank* algorithm.
        """
        weighted_tokens: typing.List[typing.Tuple[str, float]] = [
            (tok, 1 / (i + 1))
            for i, tok in enumerate(
                token.lemma_ for token in self.doc if token.pos_ in self.pos_kept
            )
        ]

        keyfunc = lambda x: x[0]
        applyfunc = lambda g: sum(w for text, w in g)

        accumulated_weighted_tokens: typing.List[typing.Tuple[str, float]] = groupby_apply(
            weighted_tokens,
            keyfunc,
            applyfunc,
        )

        accumulated_weighted_tokens = sorted(
            accumulated_weighted_tokens, key=lambda x: x[1]
        )

        norm_weighted_tokens = {
            k: w / sum(w_ for _, w_ in accumulated_weighted_tokens)
            for k, w in accumulated_weighted_tokens
        }

        # while the authors assign higher probability to a "word",
        # our *lemma graph* vertices are (lemma, pos) tuples,
        # therefore we map each `Lemma` weight to all the *lemma
        # graph* vertices which contain it

        # TODO: # pylint: disable=W0511
        # => should this map to (lemma, pos) pairs instead?

        weighted_nodes: typing.Dict[Lemma, float] = {
            Lemma(token.lemma_, token.pos_): norm_weighted_tokens[token.lemma_]
            for token in self.doc
            if token.pos_ in self.pos_kept
        }

        return weighted_nodes
