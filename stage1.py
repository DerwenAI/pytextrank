#!/usr/bin/env python
# encoding: utf-8

from pytextrank import json_iter, parse_doc, pretty_print
import sys

## Stage 1:
##  * perform statistical parsing/tagging on a document in JSON format
##
## INPUTS: <stage0>
## OUTPUT: JSON format `ParsedGraf(id, sha1, graf)`

if __name__ == "__main__":
    path_stage0 = sys.argv[1]

    for graf in parse_doc(json_iter(path_stage0)):
        print(pretty_print(graf._asdict()))
