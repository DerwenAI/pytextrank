#!/usr/bin/env python
# encoding: utf-8

import math
import sys
import textrank

DEBUG = False # True

## Stage 4:
##  * summarize a document based on most significant sentences and key phrases
##
## INPUTS: <stage2> <stage3>
## OUTPUT: Markdown format

def de_byte (lexeme):
  """a cheap hack, b/c unicode is hard"""
  return lexeme[1:].strip("'")


def de_byte_phrase (phrase):
  """a cheap hack, b/c unicode is hard"""
  return " ".join([de_byte(l) for l in phrase.split(" ")])


if __name__ == "__main__":
  path = sys.argv[1]
  phrases = ", ".join([p for p in textrank.limit_keyphrases(path, phrase_limit=12)])

  path = sys.argv[2]
  sent_iter = sorted(textrank.limit_sentences(path, word_limit=150), key=lambda x: x[1])
  s = []

  for sent_text, idx in sent_iter:
    s.append((textrank.make_sentence([w for w in sent_text])))

  graf_text = " ".join(s)

  print("**excerpts:** %s\n\n**keywords:** %s" % (graf_text, phrases,))
