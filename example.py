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

print("\n----\n")


# switch to a longer text document...

with open("dat/lee.txt", "r") as f:
    text = f.read()

doc = nlp(text)

for phrase in doc._.phrases:
    print(phrase)

print("\n----\n")

# summarize the document based on the top 15 phrases, 
# yielding the top 5 sentences...

for sent in doc._.textrank.summary(limit_phrases=15, limit_sentences=5):
    print(sent)

print("\n----\n")


# how to use stopwords, first show a baseline...

with open("dat/gen.txt", "r") as f:
    text = f.read()

doc = nlp(text)

MAX_PHRASE = 10
num_phrase = 0

for phrase in doc._.phrases:
    print(phrase)
    num_phrase += 1

    if num_phrase == MAX_PHRASE:
        break

print("\n----\n")

# now we'll add `("gensim", "PROPN")` to the stop words list
# and see how the top-ranked phrases differ...

tr.load_stopwords(path="stop.json")

doc = nlp(text)
num_phrase = 0

for phrase in doc._.phrases:
    print(phrase)
    num_phrase += 1

    if num_phrase == MAX_PHRASE:
        break
