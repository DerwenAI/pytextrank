#!/usr/bin/env python
# encoding: utf-8

import logging
import pytextrank
import spacy
import sys

######################################################################
## sample usage
######################################################################

# load a spaCy model, depending on language, scale, etc.

nlp = spacy.load("en_core_web_sm")

# logging is optional: to debug, set the `logger` parameter
# when initializing the TextRank object

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger("PyTR")

# add PyTextRank into the spaCy pipeline

tr = pytextrank.TextRank(logger=None)
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

# parse the document

with open("dat/mih.txt", "r") as f:
    text = f.read()

doc = nlp(text)

print("pipeline", nlp.pipe_names)
print("elapsed time: {} ms".format(tr.elapsed_time))

# examine the top-ranked phrases in the document

for phrase in doc._.phrases:
    print("{:.4f} {:5d}  {}".format(phrase.rank, phrase.count, phrase.text))
    print(phrase.chunks)


# generate a GraphViz doc to visualize the lemma graph

tr.write_dot(path="lemma_graph.dot")


# let's switch to a different text document:
print("----\n")
doc._.textrank.reset()

with open("dat/lee.txt", "r") as f:
    text = f.read()

doc = nlp(text)

for phrase in doc._.phrases:
    print(phrase)

# summarize the document based on the top 15 phrases, 
# yielding the top 5 sentences...
print("----\n")

for sent in doc._.textrank.summary(limit_phrases=15, limit_sentences=5):
    print(sent)
