from pytextrank.base import BaseTextRank


def test_base_text_rank(doc):
    # given
    base_text_rank = BaseTextRank()

    # when
    processed_doc = base_text_rank(doc)
    phrases = processed_doc._.phrases

    # then
    assert len(phrases)
    assert len(set(p.text for p in phrases)) == len(phrases)
    assert phrases[0].rank == max(p.rank for p in phrases)
