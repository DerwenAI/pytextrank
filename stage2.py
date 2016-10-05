#!/usr/bin/env python
# encoding: utf-8

import sys
import textrank

DEBUG = False # True

## Stage 2:
##  * collect and normalize the key phrases from a parsed document
##
## INPUTS: <stage1>
## OUTPUT: JSON format `RankedLexeme(text, rank, ids, pos)`

if __name__ == "__main__":
  path = sys.argv[1]
  graph, ranks = textrank.text_rank(path)

  textrank.render_ranks(graph, ranks)

  # output as JSON

  for rl in textrank.normalize_key_phrases(path, ranks):
    print(textrank.pretty_print(rl._asdict()))
