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

if __name__ == "__main__":
  path = sys.argv[1]
  phrases = "; ".join(textrank.limit_keyphrases(path, phrase_limit=12))

  path = sys.argv[2]
  sent_iter = sorted(textrank.limit_sentences(path, word_limit=150), key=lambda x: x[1])
  graf_text = " ".join([textrank.make_sentence(sent_text) for sent_text, idx in sent_iter])

  print("**excerpts:** %s\n\n**keywords:** %s" % (graf_text, phrases,))
