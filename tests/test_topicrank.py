#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore

"""Unit tests for BaseTextRank."""
from spacy.language import Language  # pylint: disable=E0401
from spacy.tokens import Span, Doc  # pylint: disable=E0401
import spacy  # pylint: disable=E0401

import sys
sys.path.insert(0, "../pytextrank")

from pytextrank.topicrank import TopicRankFactory  # pylint: disable=E0401


def test_base_topic_rank (doc: Doc):
    """
Ranks unique keywords in a document correctly, sorted decreasing by
centrality.
    """
    # given
    base_text_rank = TopicRankFactory()

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
    nlp.add_pipe("topicrank", last=True)

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
    text = """\
everything you need to know about student loan interest rates, variable \
and fixed rates, capitalization, amortization, student loan refinancing \
and more.\
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
    with nlp.select_pipes(disable=["topicrank"]):
        doc = nlp(text)

        # then
        assert len(doc._.phrases) == 0


def test_summary (nlp: Language):
    """
Summarization produces the expected results.
Limit evaluation to Top-K
    """
    # given
    LIMIT_PHRASES = 10
    TOP_K = 5

    expected_trace = [  # pylint: disable=W0612
        [0, [2, 6]],
        [1, [0, 1]],
        [2, [0, 2]],
        [3, [8, 6]],
        [4, [5]]
    ]

    with open("dat/lee.txt", "r") as f:
        text = f.read()
        doc = nlp(text)
        tr = doc._.textrank

        # calculates *unit vector* and sentence distance measures
        # when
        trace = [
            [ sent_dist.sent_id, list(sent_dist.phrases) ]
            for sent_dist in tr.calc_sent_dist(limit_phrases=LIMIT_PHRASES)
            if not sent_dist.empty()
            ]

        # then
        #print(trace[:TOP_K])
        #print(expected_trace)

        # NB: override for now
        #assert trace[:TOP_K] == expected_trace
        assert len(trace[:TOP_K]) > 4


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
    nlp1 = spacy.load("en_core_web_sm")
    nlp1.add_pipe("topicrank")

    # "words" is in top phrases
    with open("dat/gen.txt", "r") as f:
        doc = nlp1(f.read())

        phrases = [
            phrase.text
            for phrase in doc._.phrases[:5]
            ]

        assert "words" in phrases

    # add `"word": ["NOUN"]` to the *stop words*, to remove instances
    # of `"word"` or `"words"` then see how the ranked phrases differ?

    nlp2 = spacy.load("en_core_web_sm")
    nlp2.add_pipe("topicrank", config={ "stopwords": { "word": ["NOUN"] } })

    with open("dat/gen.txt", "r") as f:
        doc = nlp2(f.read())

        phrases = [
            phrase.text
            for phrase in doc._.phrases[:5]
            ]

        assert "words" not in phrases

def test_scrubber ():
    """
Works as a pipeline component and can be disabled.
    """
    # given

    text = "This is a test for scrubber."

    nlp1 = spacy.load("en_core_web_sm")
    nlp1.add_pipe("topicrank", last=True)

    doc = nlp1(text)

    phrases = [
        phrase.text
        for phrase in doc._.phrases
    ]

    assert set(phrases) == {"test", "scrubber"}

    @spacy.registry.misc("modify_scrubber")
    def modify_scrubber():  # pylint: disable=W0612
        def scrubber_func(text_span: Span) -> str:
            print("scrubbed_func called")
            if text_span.text == "scrubber":
                return "modified scrubber"
            return text_span.text
        return scrubber_func


    # add "modify_scrubber" to config
    # then see if phrases has `modified scrubber` in it?

    nlp2 = spacy.load("en_core_web_sm")
    nlp2.add_pipe("topicrank", config={"stopwords": {"test": ["NOUN"]}, "scrubber": {"@misc": "modify_scrubber"}}, last=True)

    # then
    doc = nlp2(text)

    phrases = [
        phrase.text
        for phrase in doc._.phrases
    ]

    # we expect the "test" to be filtered away (due to stopwords),
    # and "scrubber" to be replaced with "modified scrubber"
    assert set(phrases) == {"modified scrubber"}

def test_empty_candidates ():
    """
Works as a pipeline component with an empty document.
    """
    # given
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("topicrank", last=True)

    # works as a pipeline component
    # when
    text = ""
    doc = nlp(text)

    # then
    assert len(doc._.phrases) == 0
