#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore

"""Unit tests for PositionRank."""
from spacy.tokens import Doc  # pylint: disable=E0401

import sys
sys.path.insert(0, "../pytextrank")

from pytextrank.base import BaseTextRankFactory  # pylint: disable=E0401
from pytextrank.positionrank import PositionRankFactory  # pylint: disable=E0401


def test_position_rank (doc: Doc):
    """
Ranks keywords that appear early in the document higher than TextRank
does.
    """
    # given
    position_rank = PositionRankFactory()
    base_text_rank = BaseTextRankFactory()

    # when
    processed_doc = position_rank(doc)
    phrases = processed_doc._.phrases
    comparison_doc = base_text_rank(doc)
    comparison_phrases = comparison_doc._.phrases

    # then
    assert set(p.rank for p in phrases) != set(p.rank for p in comparison_phrases)

    # The test article mentions `Chelsea` at the beginning of the
    # article while it mentions `Shanghai Shenhua` anecdotally later
    # in the article. However, with normal TextRank, `Shanghai
    # Shenhua` is part of top 10 phrases and `Chelsea` isn't. With
    # PositionRank, the situation is the opposite, which is the
    # desired outcome when parsing a news article.

    assert "Chelsea" in [p.text for p in phrases[:10]]
    assert "Chelsea" not in [p.text for p in comparison_phrases[:10]]
    assert "Shanghai Shenhua" not in ";".join(p.text for p in phrases[:10])
    assert "Shanghai Shenhua" in ";".join(p.text for p in comparison_phrases[:10])
