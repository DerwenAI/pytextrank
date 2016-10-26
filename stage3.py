#!/usr/bin/env python
# encoding: utf-8

import sys
import textrank

DEBUG = False # True

## Stage 3:
##  * calculate a significance weight for each sentence, using MinHash to
##  * approximate Jaccard distance from key phrases determined by TextRank
##
## INPUTS: <stage1> <stage2>
## OUTPUT: JSON format `SummarySent(dist, idx, text)`

if __name__ == "__main__":
  path = sys.argv[2]
  kernel = textrank.rank_kernel(path, force_encode=False)

  path = sys.argv[1]

  for s in textrank.top_sentences(kernel, path, force_encode=False):
    print(textrank.pretty_print(s._asdict()))
