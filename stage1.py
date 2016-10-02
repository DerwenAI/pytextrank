#!/usr/bin/env python
# encoding: utf-8

import sys
import textrank

## Stage 1:
##  * perform statistical parsing/tagging on a document in JSON format (Stage 0)
##  * output is in JSON format

if __name__ == "__main__":
  path = sys.argv[1]

  for graf in textrank.parse_doc(textrank.json_iter(path)):
    print(textrank.pretty_print(graf))
