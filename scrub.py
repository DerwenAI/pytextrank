#!/usr/bin/env python
# encoding: utf-8

import sys
import textrank

DEBUG = True # False

## "It scrubs its unreadable characters out of its text stream...
## Then it generates a JSON doc again."

if __name__ == "__main__":
  path = sys.argv[1]
  lines = []

  with open(path, 'r') as f:
    for line in f.readlines():
      line = line.strip().replace('“', '"').replace('”', '"')
      line = line.replace('…', '...').replace('–', '-')
      line = line.replace("’", "'").replace("`", "'")

      lines.append(line)

  j = {}
  j["id"] = "777"
  j["text"] = " ".join(lines)

  print(textrank.pretty_print(j))
