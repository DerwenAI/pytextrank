#!/usr/bin/env python
# encoding: utf-8

from collections import namedtuple
from operator import itemgetter
import hashlib
import json
import math
import matplotlib.pyplot as plt
import networkx as nx
import re
import string
import textblob
import textblob_aptagger as tag

DEBUG = False # True

WordNode = namedtuple('WordNode', 'word_id, raw, root, pos, keep, idx')
Phrase = namedtuple('Phrase', 'rank, ids, text')


######################################################################
## filter the novel text versus quoted text in an email message

PAT_FORWARD = re.compile("\n\-+ Forwarded message \-+\n")
PAT_REPLIED = re.compile("\nOn.*\d+.*\n?wrote\:\n+\>")
PAT_UNSUBSC = re.compile("\n\-+\nTo unsubscribe,.*\nFor additional commands,.*")


def split_grafs (lines):
  """segment the raw text into paragraphs"""

  graf = []

  for line in lines:
    line = line.strip()

    if len(line) < 1:
      if len(graf) > 0:
        yield "\n".join(graf)
        graf = []
    else:
      graf.append(line)

  if len(graf) > 0:
    yield "\n".join(graf)


def filter_quotes (text, is_email=True):
  """filter the quoted text out of a message"""

  global DEBUG
  global PAT_FORWARD, PAT_REPLIED, PAT_UNSUBSC

  if is_email:
    text = filter(lambda x: x in string.printable, text)

    if DEBUG:
      print("text:", text)

    # strip off quoted text in a forward
    m = PAT_FORWARD.split(text, re.M)

    if m and len(m) > 1:
      text = m[0]

    # strip off quoted text in a reply
    m = PAT_REPLIED.split(text, re.M)

    if m and len(m) > 1:
      text = m[0]

    # strip off any trailing unsubscription notice
    m = PAT_UNSUBSC.split(text, re.M)

    if m:
      text = m[0]

  # replace any remaining quoted text with blank lines
  lines = []

  for line in text.split("\n"):
    if line.startswith(">"):
      lines.append("")
    else:
      lines.append(line)

  return list(split_grafs(lines))


######################################################################
## parse and markup text paragraphs for semantic analysis

PAT_PUNCT = re.compile(r'^\W+$')
PAT_SPACE = re.compile(r'\_+$')

POS_KEEPS = ['v', 'n', 'j']
POS_LEMMA = ['v', 'n']
TAGGER = tag.PerceptronTagger()
UNIQ_WORDS = { ".": 0 }


def is_not_word (word):
  return PAT_PUNCT.match(word) or PAT_SPACE.match(word)


def get_word_id (word):
  """lookup/assign a unique identify for each word"""

  global UNIQ_WORDS

  # in practice, this should use a microservice via some robust
  # distributed cache, e.g., Cassandra, Redis, etc.

  if word.root not in UNIQ_WORDS:
    UNIQ_WORDS[word.root] = len(UNIQ_WORDS)

  return UNIQ_WORDS[word.root]


def parse_graf (doc_id, graf_text, base_idx):
  """CORE ALGORITHM: parse and markup sentences in the given paragraph"""

  global DEBUG
  global POS_KEEPS, POS_LEMMA, TAGGER

  markup = []
  new_base_idx = base_idx

  for sent in textblob.TextBlob(graf_text).sentences:
    graf = []
    digest = hashlib.sha1()

    tagged_sent = TAGGER.tag(str(sent))
    tag_idx = 0
    raw_idx = 0

    if DEBUG:
      print(tagged_sent)

    while tag_idx < len(tagged_sent):
      pos_tag = tagged_sent[tag_idx]
      word = WordNode(word_id=0, raw=pos_tag[0], root=pos_tag[0], pos=pos_tag[1], keep=0, idx=new_base_idx)

      if DEBUG:
        print("IDX", tag_idx, pos_tag)
        print("reg", is_not_word(pos_tag[0]))
        print("   ", raw_idx, len(sent.words), sent.words)
        print(graf)

      if is_not_word(pos_tag[0]) or (pos_tag[1] == "SYM"):
        parsed_raw = pos_tag[0]
        pos_family = '.'
        word = word._replace(pos = pos_family)
      elif raw_idx < len(sent.words):
        parsed_raw = sent.words[raw_idx]
        pos_family = pos_tag[1].lower()[0]
        raw_idx += 1

      word = word._replace(raw = str(parsed_raw))

      if pos_family in POS_LEMMA:
        word = word._replace(root = str(parsed_raw.singularize().lemmatize(pos_family)).lower())
      elif pos_family != '.':
        word = word._replace(root = str(parsed_raw).lower())
      else:
        word = word._replace(root = str(parsed_raw))

      if pos_family in POS_KEEPS:
        word = word._replace(word_id = get_word_id(word), keep = 1)

      digest.update(word.root.encode("utf-8"))

      # schema: word_id, raw, root, pos, keep, idx
      if DEBUG:
        print(word)

      graf.append(list(word))

      new_base_idx += 1
      tag_idx += 1

    #"lang": s.detect_language(),
    markup.append({
        "id": doc_id,
        "sha1": digest.hexdigest(),
        "graf": graf
        })

  return markup, new_base_idx


def parse_doc (json_iter):
  """parse one document to prep for TextRank"""

  global DEBUG

  for meta in json_iter:
    base_idx = 0

    for graf_text in filter_quotes(meta["text"], is_email=False):
      if DEBUG:
        print("graf_text:", graf_text)

      grafs, new_base_idx = parse_graf(meta["id"], graf_text, base_idx)
      base_idx = new_base_idx

      for graf in grafs:
        yield graf


######################################################################
## graph analytics

def get_tiles (graf, size=3):
  """generate word pairs for the TextRank graph"""

  keeps = list(filter(lambda w: w.word_id > 0, graf))
  keeps_len = len(keeps)

  for i in iter(range(0, keeps_len - 1)):
    w0 = keeps[i]

    for j in iter(range(i + 1, min(keeps_len, i + 1 + size))):
      w1 = keeps[j]

      if (w1.idx - w0.idx) <= size:
        yield (w0.root, w1.root,)


def build_graph (json_iter):
  """construct the TextRank graph from parsed paragraphs"""

  global DEBUG, WordNode

  graph = nx.DiGraph()

  for meta in json_iter:
    if DEBUG:
      print(meta["graf"])

    for pair in get_tiles(map(WordNode._make, meta["graf"])):
      if DEBUG:
        print(pair)

      for word_id in pair:
        if not graph.has_node(word_id):
          graph.add_node(word_id)

      try:
        graph.edge[pair[0]][pair[1]]["weight"] += 1.0
      except KeyError:
        graph.add_edge(pair[0], pair[1], weight=1.0)

  return graph


def render_ranks (graph, ranks, img_file="graph.png", show_img=None):
  """render the TextRank graph as an image"""

  for node, rank in sorted(ranks.items(), key=itemgetter(1), reverse=True):
    print("%0.4f %s" % (rank, node))

  nx.draw_networkx(graph)

  if img_file:
    plt.savefig(img_file)

  if show_img:
    plt.show()


def emit_phrase (phrase):
  """reconstruct a phrase based on ranks"""

  global DEBUG, Phrase

  ## denominator increases the relative rank of phrases
  size = len(phrase)
  rank = math.sqrt(sum(map(lambda w: w[0]**2.0, phrase)))

  if size > 1:
    rank = rank / (float(size) ** -math.e)

  ids = set(map(lambda w: w[1], phrase))
  text = " ".join(map(lambda w: w[2], phrase)).lower()

  p = Phrase(rank=rank, ids=ids, text=text)

  if DEBUG:
    print("---", p)

  return p


def apply_ranks (ranks, json_iter):
  """determine the highest ranked noun phrases"""

  global DEBUG, WordNode
  summary = []

  for meta in json_iter:
    last_idx = -1
    phrase = []

    # schema: word_id, raw, root, pos, keep, idx

    for w in map(WordNode._make, meta["graf"]):
      if (w.word_id > 0) and (w.root in ranks) and (w.pos[0] != 'V'):
        if last_idx >= 0 and (w.idx - last_idx) > 1:
          summary.append(emit_phrase(phrase))
          phrase = []

        phrase.append((ranks[w.root], w.word_id, w.raw,))

        if DEBUG:
          print("%3d %0.4f %s %s %d" % (w.idx, ranks[w.root], w.root, w.raw, last_idx))

        last_idx = w.idx

    summary.append(emit_phrase(phrase))

  return summary


def text_rank (path):
  """run the TextRank algorithm"""

  global DEBUG

  graph = build_graph(json_iter(path))
  ranks = nx.pagerank(graph)

  if DEBUG:
    render_ranks(graph, ranks)

  return apply_ranks(ranks, json_iter(path))


######################################################################
## keyphrase summary

def normalize_keyphrases (summary):
  """normalize the given list of TextRank key phrases"""

  # L1 norm, to scale the keyphrase ranks
  rank_norm = sum([p.rank for p in summary])

  key_phrases = {}
  known = []

  for p in sorted(summary, key=lambda x: len(x[2]), reverse=True):
    seen = False

    for k in known:
      if p.ids.issubset(k):
        seen = True
        break

    if not seen:
      known.append(p.ids)
      key_phrases[p.text] = p.rank

  for phrase, rank in sorted(key_phrases.items(), key=itemgetter(1), reverse=True):
    yield rank / rank_norm, phrase


######################################################################
## common utilities

def json_iter (path):
  """iterator for JSON-per-line in a file"""

  with open(path, 'r') as f:
    for line in f.readlines():
      yield json.loads(line)


def pretty_print (obj, indent=False):
  """pretty print a JSON object"""

  if indent:
    return json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': '))
  else:
    return json.dumps(obj, sort_keys=True)
