#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore

"""
A simple stub to generate the expected "trace" used in unit tests.
"""

import sys  # pylint: disable=W0611

from icecream import ic  # pylint: disable=E0401
import pytextrank  # pylint: disable=E0401,W0611
import spacy  # pylint: disable=E0401

# set up
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] } })


## test_summary
## limit to TOP_K

with open("dat/lee.txt", "r") as f:
    text = f.read()
    doc = nlp(text)
    tr = doc._.textrank

    TOP_K = 5
    trace = []

    for sent_dist in tr.calc_sent_dist(limit_phrases=10):
        if not sent_dist.empty():
            trace.append([ sent_dist.sent_id, list(sent_dist.phrases) ])

    ic(trace[:TOP_K])
