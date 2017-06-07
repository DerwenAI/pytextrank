#!/usr/bin/env python
# encoding: utf-8

from pytextrank import normalize_key_phrases, pretty_print, render_ranks, text_rank
import sys

## Stage 2:
##  * collect and normalize the key phrases from a parsed document
##
## INPUTS: <stage1>
## OUTPUT: JSON format `RankedLexeme(text, rank, ids, pos)`

if __name__ == "__main__":
    path_stage1 = sys.argv[1]

    graph, ranks = text_rank(path_stage1)
    render_ranks(graph, ranks)

    for rl in normalize_key_phrases(path_stage1, ranks):
        print(pretty_print(rl._asdict()))
