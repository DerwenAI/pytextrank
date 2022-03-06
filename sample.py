#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import sys  # pylint: disable=W0611

from icecream import ic  # pylint: disable=E0401
import spacy  # pylint: disable=E0401

import pytextrank  # pylint: disable=W0611


######################################################################
## sample usage

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank into the spaCy pipeline
# NB: substitute `"textrank"` with the name of other algorithms, e.g., `"positionrank"`
nlp.add_pipe("textrank")

# parse the document
text = pathlib.Path("dat/mih.txt").read_text()
doc = nlp(text)

## access the TextRank component, for post-processing
tr = doc._.textrank
print("elapsed time: {:.2f} ms".format(tr.elapsed_time))

# examine the pipeline
ic("pipeline", nlp.pipe_names)
nlp.analyze_pipes(pretty=True)
print("\n----\n")

# examine the top-ranked phrases in the document
for phrase in doc._.phrases:
    print("{:.4f} {:5d}  {}".format(phrase.rank, phrase.count, phrase.text))
    ic(phrase.chunks)

# switch to a longer text document...
print("\n----\n")
print("dat/lee.txt")

text = pathlib.Path("dat/lee.txt").read_text()
doc = nlp(text)

for phrase in doc._.phrases[:20]:
    ic(phrase)

# to show use of stopwords: first we output a baseline...
print("\n----\n")
print("dat/gen.txt")

text = pathlib.Path("dat/gen.txt").read_text()
doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)

# now add `"word": ["NOUN"]` to the stop words, to remove instances
# of `"word"` or `"words"` then see how the ranked phrases differ...
print("\n----\n")
print("stopwords:")

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("textrank", config={ "stopwords": { "word": ["NOUN"] } })

doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)

# generate a GraphViz doc to visualize the lemma graph
print("\n----\n")
print("extractive summarization:")

tr = doc._.textrank
tr.write_dot(path="lemma_graph.dot")

# summarize the document based on its top 15 phrases,
# yielding its top 5 sentences...
for sent in tr.summary(limit_phrases=15, limit_sentences=5):
    ic(sent)

print("\n----\n")
print("Biased TextRank:")

EXPECTED_PHRASES = [
    "grandmaster Lee Sedol",
    "Lee Sedol",
    "Deep Blue",
    "world chess champion Gary Kasparov",
    "chess",
    "Gary Kasparov",
    "the following year",
    "Kasparov",
]

ic(EXPECTED_PHRASES)

# show use of Biased TextRank algorithm
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("biasedtextrank")

text = pathlib.Path("dat/lee.txt").read_text()
doc = nlp(text)

for phrase in doc._.phrases[:len(EXPECTED_PHRASES)]:
    ic(phrase)

print("\n----\n")
tr = doc._.textrank

# note how the bias parameters get set here, to help emphasize
# the *focus set*

phrases = tr.change_focus(
    focus="It wasn't until the following year that Deep Blue topped Kasparov over the course of a six-game contest.",
    bias=10.0,
    default_bias=0.0,
    )

for phrase in phrases[:len(EXPECTED_PHRASES)]:
    ic(phrase.text)
    ic(phrase.text in EXPECTED_PHRASES)
