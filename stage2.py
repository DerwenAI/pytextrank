#!/usr/bin/env python
# encoding: utf-8

import sys
import textrank

## Stage 2:
##  * summarize key phrases from a parsed document in JSON format (Stage 1)
##  * output is in TSV format

if __name__ == "__main__":
  path = sys.argv[1]
  summary = textrank.text_rank(path)

  for rank, phrase in textrank.normalize_keyphrases(summary):
    print("%0.4f\t%s" % (rank, phrase))
