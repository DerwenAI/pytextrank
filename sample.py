#!/usr/bin/env python
# -*- coding: utf-8 -*-

from icecream import ic
import pathlib
import pytextrank
import spacy
import sys


######################################################################
## sample usage

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank into the spaCy pipeline
#nlp.add_pipe("positionrank")
nlp.add_pipe("textrank")

# parse the document
with open("dat/mih.txt", "r") as f:
    text = f.read()

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

print("\n----\n")

# switch to a longer text document...
with open("dat/lee.txt", "r") as f:
    text = f.read()

doc = nlp(text)

for phrase in doc._.phrases[:20]:
    ic(phrase)

print("\n----\n")

# show use of stopwords: first we output a baseline...
with open("dat/gen.txt", "r") as f:
    text = f.read()

doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)

print("\n----\n")

# now add `"word": ["NOUN"]` to the stop words, to remove instances
# of `"word"` or `"words"` then see how the ranked phrases differ...
tr.load_stopwords(data = { "word": ["NOUN"] })

doc = nlp(text)

for phrase in doc._.phrases[:10]:
    ic(phrase)

print("\n----\n")

# generate a GraphViz doc to visualize the lemma graph
tr.write_dot(path="lemma_graph.dot")

# summarize the document based on its top 15 phrases, 
# yielding its top 5 sentences...
for sent in tr.summary(limit_phrases=15, limit_sentences=5):
    ic(sent)

