#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Unit tests for BiasedRank."""
from spacy.tokens import Doc

import sys ; sys.path.insert(0, "../pytextrank")
from pytextrank.base import BaseTextRankFactory
from pytextrank.biasedrank  import BiasedTextRankFactory


def test_default_biased_rank (doc: Doc):
    """
    Biasedrank should behave like base textrank by default.
    """
    # given
    biased_rank = BiasedTextRankFactory()
    base_text_rank = BaseTextRankFactory()

    # when
    processed_doc = base_text_rank(doc)
    phrases = processed_doc._.phrases

    comparison_doc = biased_rank(doc)
    comparison_phrases = comparison_doc._.phrases

    # then
    assert tuple(p.text for p in phrases) == tuple(p.text for p in comparison_phrases)


def test_biased_rank (long_doc: Doc):
    """
    Rank phrases close to 'focus' higher.
    """
    # given
    biased_rank = BiasedTextRankFactory()
    base_text_rank = BaseTextRankFactory()

    # when
    processed_doc = base_text_rank(long_doc)
    phrases = processed_doc._.phrases

    # Article is primarily about match up between AlphaGo and Grandmaster Lee Sedol
    assert "grandmaster Lee Sedol" in [p.text for p in phrases][:3]
    assert "Gary Kasparov" not in [p.text for p in phrases][:3]

    comparison_doc = biased_rank(long_doc)
    tr = comparison_doc._.textrank
    tr.change_focus(
        "Chess",
        bias=10.0,
        default_bias=0.0)

    biased_phrases = comparison_doc._.phrases

    # then
    # shifting the focus to chess bring Gary Kasparov in top ranks
    assert "Gary Kasparov" in [p.text for p in biased_phrases][:3]
