#!/usr/bin/env python
# encoding: utf-8

from pytextrank import pretty_print, rank_kernel, top_sentences
import sys

## Stage 3:
##  * calculate a significance weight for each sentence, using MinHash to
##  * approximate Jaccard distance from key phrases determined by TextRank
##
## INPUTS: <stage1> <stage2>
## OUTPUT: JSON format `SummarySent(dist, idx, text)`

if __name__ == "__main__":
    path_stage1 = sys.argv[1]
    path_stage2 = sys.argv[2]

    kernel = rank_kernel(path_stage2)

    for s in top_sentences(kernel, path_stage1):
        print(pretty_print(s._asdict()))
