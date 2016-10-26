#!/usr/bin/env python
# encoding: utf-8

import sys
import textrank

## Stage 1:
##  * perform statistical parsing/tagging on a document in JSON format
##
## INPUTS: <stage0>
## OUTPUT: JSON format `ParsedGraf(id, sha1, graf)`

if __name__ == "__main__":
  path = sys.argv[1]

  for graf in textrank.parse_doc(textrank.json_iter(path), force_encode=False):
    print(textrank.pretty_print(graf._asdict()))
