#!/usr/bin/env python
# encoding: utf-8

import sys
import textrank

DEBUG = True # False

## Stage 2:
##  * summarize key phrases from a parsed document in JSON format (Stage 1)
##  * output is in JSON format

if __name__ == "__main__":
  path = sys.argv[1]
  graph, ranks, summary = textrank.text_rank(path)

  if DEBUG:
    textrank.render_ranks(graph, ranks)

    for p in textrank.normalize_keyphrases(summary):
      print("%0.4f\t%s" % (p.rank, p.text), p.ids)

  # output as JSON

  for norm in textrank.get_kernel(summary):
    print(textrank.pretty_print(norm._asdict()))
