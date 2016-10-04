#!/usr/bin/env python
# encoding: utf-8

from datasketch import MinHash
import textblob
import sys
import textrank

DEBUG = False # True

## Stage 3:
##  * calculates a significance weight for each sentence, using MinHash
##  * to approximate Jaccard distance from key phrases determined by TextRank
##  * output is in TSV format

def mh_digest (data, num_perm=512):
  """create a MinHash digest"""
  m = MinHash(num_perm)

  for d in data:
    m.update(d.encode('utf8'))

  return m


def rank_kernel (path):
  """return a list (matrix-ish) of the key phrases and their ranks"""
  kernel = []

  for meta in textrank.json_iter(path):
    p = textrank.NormPhrase(**meta)
    m = mh_digest(map(lambda x: str(x), p.ids))
    kernel.append((p, m,))

  return kernel


def find_chunk_sub (tagged_sent, np, i):
  """not used: np chunking"""
  for j in iter(range(0, len(np))):
    w = tagged_sent[i + j]

    if w.raw != np[j]:
      return None

  return tagged_sent[i:i + len(np)]


def find_chunk (tagged_sent, np):
  """not used: np chunking"""
  for i in iter(range(0, len(tagged_sent))):
    parsed_np = find_chunk_sub(tagged_sent, np, i)

    if parsed_np:
      return parsed_np


def np_chunk (tagged_sent, text, key_phrases):
  """not used: np chunking"""
  chunks = set(textblob.en.np_extractors.FastNPExtractor().extract(text))
  #chunks = set(textblob.en.np_extractors.ConllExtractor().extract(text))

  for np_text in chunks:
    np = np_text.split(" ")
    parsed_np = find_chunk(tagged_sent, np)

    if parsed_np:
      m_np = mh_digest([str(w.word_id) for w in parsed_np])
      key_phrases[np_text.lower()] = sum([m_np.jaccard(m) * (p.norm_rank + p.rank) for p, m in kernel])


def top_sentences (kernel, path):
  """determine distance for each sentence"""
  key_sent = {}
  i = 0

  for meta in textrank.json_iter(path):
    graf = meta["graf"]
    tagged_sent = [textrank.WordNode._make(x) for x in graf]
    text = " ".join([w.raw for w in tagged_sent])

    m_sent = mh_digest([str(w.word_id) for w in tagged_sent])
    dist = sum([m_sent.jaccard(m) * (p.norm_rank + p.rank) for p, m in kernel])
    key_sent[text] = (dist, i)
    i += 1

  for text, (dist, i) in sorted(key_sent.items(), key=lambda x: x[1][0], reverse=True):
    yield textrank.SummarySent(dist=dist, idx=i, text=text)


if __name__ == "__main__":
  path = sys.argv[2]
  kernel = rank_kernel(path)

  path = sys.argv[1]

  for s in top_sentences(kernel, path):
    print(textrank.pretty_print(s._asdict()))
