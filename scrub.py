#!/usr/bin/env python
# encoding: utf-8

import sys
import textrank
import unicodedata

DEBUG = False # True

## "It scrubs its unreadable characters out of its text stream...
## Then it generates a JSON doc again."

if __name__ == "__main__":
  path = sys.argv[1]
  lines = []

  with open(path, 'r') as f:
    for line in f.readlines():
      line = line.strip()
      line = line.replace('“', '"').replace('”', '"')
      line = line.replace("’", "'").replace("’", "'").replace("`", "'")
      line = line.replace('…', '...').replace('–', '-')
      unicodedata.normalize('NFKD', lines).encode('ascii', 'ignore')
      lines.append(line)

  j = {}
  j["id"] = "777"
  j["text"] = " ".join(lines)

  print(textrank.pretty_print(j))
