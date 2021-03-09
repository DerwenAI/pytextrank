"""Unit tests for PositionRank."""
from spacy.tokens import Doc

import sys ; sys.path.insert(0, "../pytextrank")
from pytextrank.base import BaseTextRankFactory
from pytextrank.positionrank import PositionRankFactory


def test_position_rank (doc: Doc):
    """It ranks keywords that appear early in the document higher than TextRank."""
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
    # the test article mentions Chelsea at the begginning of the article
    # while it mentions Shanghai Shenhua annecdotally later in the article
    # with normal TextRank, Shanghai Shenhua is part of top 10 phrases and Chelsea is not
    # with PositionRank, the situation is the opposite, which is desired for a piece of news.
    assert "Chelsea" in [p.text for p in phrases[:10]]
    assert "Chelsea" not in [p.text for p in comparison_phrases[:10]]
    assert "Shanghai Shenhua" not in [p.text for p in phrases[:10]]
    assert "Shanghai Shenhua" in [p.text for p in comparison_phrases[:10]]
