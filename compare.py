from textblob import TextBlob
import spacy

text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered."

blob = TextBlob(text)

for sent in blob.sentences:
    print(sent)
    print(sent.tags)


nlp = spacy.load('en')
doc = nlp(text)

for sent in doc.sents:
    print(sent)
    print(type(sent))
    print(repr(sent))

    print(sent.start, sent.end, len(sent))

    #for word in nlp(repr(sent)):
    #for word in sent.__iter__:
    for i in range(len(sent)):
        word = sent[i]
        print(word.text, word.lemma, word.lemma_, word.tag, word.tag_, word.pos, word.pos_)

for np in doc.noun_chunks:
    print(np.text)


print("---")
from spacy.symbols import *

np_labels = set([nsubj, nsubjpass, dobj, iobj, pobj]) # Probably others too

def iter_nps(doc):
    for word in doc:
        if word.dep in np_labels:
            yield word.subtree


for np in iter_nps(doc):
    print(list(np))
