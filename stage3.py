#!/usr/bin/env python
# encoding: utf-8

from datasketch import MinHash
import sys
import textrank

DEBUG = True # False

## Stage 3:
##  * foo bar baz
##  * output is in XYZ format

def mh_digest (data):
  m = MinHash(num_perm=512)

  for d in data:
    m.update(d.encode('utf8'))

  return m


if __name__ == "__main__":
  path = sys.argv[2]
  kernel = []

  for meta in textrank.json_iter(path):
    p = textrank.NormPhrase(**meta)
    m = mh_digest(map(lambda x: str(x), p.ids))
    kernel.append((p, m,))

  path = sys.argv[1]

  for meta in textrank.json_iter(path):
    graf = meta["graf"]
    tagged_sent = [textrank.WordNode._make(x) for x in graf]
    m_sent = mh_digest([str(w.word_id) for w in tagged_sent])

    dist = sum([m_sent.jaccard(m) * (p.norm_rank + p.rank) for p, m in kernel])
    text = " ".join([w.raw for w in tagged_sent])
    print("%0.3f\t%s" % (dist, text,))
