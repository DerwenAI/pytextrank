#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore

"""Unit tests for BaseTextRank."""
from spacy.language import Language  # pylint: disable=E0401
from spacy.tokens import Doc  # pylint: disable=E0401
import spacy  # pylint: disable=E0401

import sys
sys.path.insert(0, "../pytextrank")

from pytextrank.base import BaseTextRankFactory  # pylint: disable=E0401


def test_base_text_rank (doc: Doc):
    """
Ranks unique keywords in a document correctly, sorted decreasing by
centrality.
    """
    # given
    base_text_rank = BaseTextRankFactory()

    # when
    processed_doc = base_text_rank(doc)
    phrases = processed_doc._.phrases

    # then
    assert len(phrases) > 0
    assert len(set(p.text for p in phrases)) == len(phrases)
    assert phrases[0].rank == max(p.rank for p in phrases)


def test_add_pipe (nlp: Language):
    """
Works as a pipeline component and can be disabled.
    """
    # given
    # base_text_rank = BaseTextRankFactory()
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
    text = """
everything you need to know about student loan interest rates variable
and fixed rates capitalization amortization student loan refinancing
and more.
"""

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


def test_summary (nlp: Language):
    """
Summarization produces the expected results.
    """
    # given
    expected_trace = [
        [0, [0, 2, 6, 7, 8]],
        [1, [8]],
        [2, [2]],
        [7, [8, 4]],
        [8, [8]],
        [11, [2]],
        [12, [1]],
        [14, [2, 5]],
        [15, [9, 3, 7]],
        [17, [2]],
        ]

    with open("dat/lee.txt", "r") as f:
        text = f.read()
        doc = nlp(text)
        tr = doc._.textrank

        # calculates *unit vector* and sentence distance measures
        # when
        trace = [
            [ sent_dist.sent_id, list(sent_dist.phrases) ]
            for sent_dist in tr.calc_sent_dist(limit_phrases=10)
            if not sent_dist.empty()
            ]

        # then
        assert trace == expected_trace


def test_multiple_summary (nlp: Language):
    """
Summarization produces consistent results when called across multiple
docs.
    """
    texts = []

    with open("dat/lee.txt", "r") as f:
        text = f.read()
        texts.append(text)

    with open("dat/mih.txt", "r") as f:
        text = f.read()
        texts.append(text)

    docs = [nlp(text) for text in texts]

    trace1 = [
        [sent_dist.sent_id, list(sent_dist.phrases)]
        for sent_dist in docs[0]._.textrank.calc_sent_dist(limit_phrases=10)
        if not sent_dist.empty()
    ]

    trace2 = [
        [sent_dist.sent_id, list(sent_dist.phrases)]
        for sent_dist in docs[1]._.textrank.calc_sent_dist(limit_phrases=10)
        if not sent_dist.empty()
    ]

    assert trace1 != trace2


def test_stop_words ():
    """
Works as a pipeline component and can be disabled.
    """
    # given
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] } })

    # when
    _expected_phrases = [
        "sentences",
        "Mihalcea et al",
        "text summarization",
        "gensim implements",
        "Okapi BM25 function",
        ]

    # add `"word": ["NOUN"]` to the *stop words*, to remove instances
    # of `"word"` or `"words"` then see how the ranked phrases differ?

    # then
    with open("dat/gen.txt", "r") as f:
        doc = nlp(f.read())

        phrases = [
            phrase.text
            for phrase in doc._.phrases[:5]
            ]

        assert phrases == _expected_phrases
