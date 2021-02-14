"""Unit tests for BaseTextRank."""
from spacy.language import Language
from spacy.tokens import Doc

import sys ; sys.path.insert(0, "../pytextrank")
from pytextrank.base import BaseTextRank


def test_base_text_rank (doc: Doc):
    """It ranks unique keywords in a document, sorted decreasing by centrality."""
    # given
    base_text_rank = BaseTextRank()

    # when
    processed_doc = base_text_rank(doc)
    phrases = processed_doc._.phrases

    # then
    assert len(phrases)
    assert len(set(p.text for p in phrases)) == len(phrases)
    assert phrases[0].rank == max(p.rank for p in phrases)


def test_add_pipe (nlp: Language):
    """It works as a pipeline component and can be disabled."""
    # given
    base_text_rank = BaseTextRank()
    nlp.add_pipe("textrank", last=True)

    # works as a pipeline component
    # when
    text = "linear constraints over the"
    doc = nlp(text)
    phrases = [ p.text for p in doc._.phrases ]

    # then
    assert len(doc._.phrases) > 0
    assert any(map(lambda x: "constraints" in x, phrases))

    # identifies phrases not in noun chunks
    # when
    text = "everything you need to know about student loan interest rates variable and fixed rates capitalization amortization student loan refinancing and more."
    doc = nlp(text)
    phrases = [ p.text for p in doc._.phrases ]

    # then
    assert len(doc._.phrases) >= 2

    # resolves Py 3.5 dict KeyError
    # when
    text = "linear constraints over the set of natural numbers"
    doc = nlp(text)
    phrases = [ p.text for p in doc._.phrases ]

    # then
    assert any(map(lambda x: "constraints" in x, phrases))

    # pipeline can be disabled
    # when
    with nlp.select_pipes(disable=["textrank"]):
        doc = nlp(text)

        # then
        assert len(doc._.phrases) == 0
