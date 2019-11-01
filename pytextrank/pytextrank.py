#!/usr/bin/env python
# encoding: utf-8

from collections import namedtuple
from datasketch import MinHash
from graphviz import Digraph
import hashlib
import json
import math
import networkx as nx
import os
import os.path
import re
import spacy
import statistics
import string

DEBUG = False # True

ParsedGraf = namedtuple('ParsedGraf', 'id, sha1, graf')
WordNode = namedtuple('WordNode', 'word_id, raw, root, pos, keep, idx')
RankedLexeme = namedtuple('RankedLexeme', 'text, rank, ids, pos, count')
SummarySent = namedtuple('SummarySent', 'dist, idx, text')


######################################################################
## filter the novel text versus quoted text in an email message

PAT_FORWARD = re.compile("\n\-+ Forwarded message \-+\n")
PAT_REPLIED = re.compile("\nOn.*\d+.*\n?wrote\:\n+\>")
PAT_UNSUBSC = re.compile("\n\-+\nTo unsubscribe,.*\nFor additional commands,.*")


def split_grafs (lines):
    """
    segment the raw text into paragraphs
    """
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
    """
    filter the quoted text out of a message
    """
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
UNIQ_WORDS = { ".": 0 }


def is_not_word (word):
    return PAT_PUNCT.match(word) or PAT_SPACE.match(word)


def get_word_id (root):
    """
    lookup/assign a unique identify for each word root
    """
    global UNIQ_WORDS

    # in practice, this should use a microservice via some robust
    # distributed cache, e.g., Redis, Cassandra, etc.
    if root not in UNIQ_WORDS:
        UNIQ_WORDS[root] = len(UNIQ_WORDS)

    return UNIQ_WORDS[root]


def fix_microsoft (foo):
    """
    fix special case for `c#`, `f#`, etc.; thanks Microsoft
    """
    i = 0
    bar = []

    while i < len(foo):
        text, lemma, pos, tag = foo[i]

        if (text == "#") and (i > 0):
            prev_tok = bar[-1]

            prev_tok[0] += "#"
            prev_tok[1] += "#"

            bar[-1] = prev_tok
        else:
            bar.append(foo[i])

        i += 1

    return bar


def fix_hypenation (foo):
    """
    fix hyphenation in the word list for a parsed sentence
    """
    i = 0
    bar = []

    while i < len(foo):
        text, lemma, pos, tag = foo[i]

        if (tag == "HYPH") and (i > 0) and (i < len(foo) - 1):
            prev_tok = bar[-1]
            next_tok = foo[i + 1]

            prev_tok[0] += "-" + next_tok[0]
            prev_tok[1] += "-" + next_tok[1]

            bar[-1] = prev_tok
            i += 2
        else:
            bar.append(foo[i])
            i += 1

    return bar


def parse_graf (doc_id, graf_text, base_idx, spacy_nlp=None):
    """
    CORE ALGORITHM: parse and markup sentences in the given paragraph
    """
    global DEBUG
    global POS_KEEPS, POS_LEMMA, SPACY_NLP

    # set up the spaCy NLP parser
    if not spacy_nlp:
        if not SPACY_NLP:
            SPACY_NLP = spacy.load("en")

        spacy_nlp = SPACY_NLP

    markup = []
    new_base_idx = base_idx
    doc = spacy_nlp(graf_text)

    for span in doc.sents:
        graf = []
        digest = hashlib.sha1()

        if DEBUG:
            print(span)

        # build a word list, on which to apply corrections
        word_list = []

        for tag_idx in range(span.start, span.end):
            token = doc[tag_idx]

            if DEBUG:
                print("IDX", tag_idx, token.text, token.tag_, token.pos_)
                print("reg", is_not_word(token.text))

            word_list.append([token.text, token.lemma_, token.pos_, token.tag_])

        # scan the parsed sentence, annotating as a list of `WordNode`
        corrected_words = fix_microsoft(fix_hypenation(word_list))

        for tok_text, tok_lemma, tok_pos, tok_tag in corrected_words:
            word = WordNode(word_id=0, raw=tok_text, root=tok_text.lower(), pos=tok_tag, keep=0, idx=new_base_idx)

            if is_not_word(tok_text) or (tok_tag == "SYM"):
                # a punctuation, or other symbol
                pos_family = '.'
                word = word._replace(pos=pos_family)
            else:
                pos_family = tok_tag.lower()[0]

            if pos_family in POS_LEMMA:
                # can lemmatize this word?
                word = word._replace(root=tok_lemma)

            if pos_family in POS_KEEPS:
                word = word._replace(word_id=get_word_id(word.root), keep=1)

            digest.update(word.root.encode('utf-8'))

            # schema: word_id, raw, root, pos, keep, idx
            if DEBUG:
                print(word)

            graf.append(list(word))
            new_base_idx += 1

        markup.append(ParsedGraf(id=doc_id, sha1=digest.hexdigest(), graf=graf))

    return markup, new_base_idx


def parse_doc (json_iter):
    """
    parse one document to prep for TextRank
    """
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
    """
    generate word pairs for the TextRank graph
    """
    keeps = list(filter(lambda w: w.word_id > 0, graf))
    keeps_len = len(keeps)

    for i in iter(range(0, keeps_len - 1)):
        w0 = keeps[i]

        for j in iter(range(i + 1, min(keeps_len, i + 1 + size))):
            w1 = keeps[j]

            if (w1.idx - w0.idx) <= size:
                yield (w0.root, w1.root,)


def build_graph (json_iter):
    """
    construct the TextRank graph from parsed paragraphs
    """
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
                graph.adj[pair[0]][pair[1]]["weight"] += 1.0
            except KeyError:
                graph.add_edge(pair[0], pair[1], weight=1.0)

    return graph


def write_dot (graph, ranks, path="graph.dot"):
    """
    output the graph in Dot file format
    """
    dot = Digraph()

    for node in graph.nodes():
        dot.node(node, "%s %0.3f" % (node, ranks[node]))

    for edge in graph.edges():
        dot.edge(edge[0], edge[1], constraint="false")

    with open(path, 'w') as f:
        f.write(dot.source)


def render_ranks (graph, ranks, dot_file="graph.dot"):
    """
    render the TextRank graph for visual formats
    """
    if dot_file:
        write_dot(graph, ranks, path=dot_file)

    ## omitted since matplotlib isn't reliable enough
    #import matplotlib.pyplot as plt
    #nx.draw_networkx(graph)
    #plt.savefig(img_file)
    #plt.show()


def text_rank (path):
    """
    run the TextRank algorithm
    """
    graph = build_graph(json_iter(path))
    ranks = nx.pagerank(graph)

    return graph, ranks


######################################################################
## collect key phrases

SPACY_NLP = None
STOPWORDS = None


def load_stopwords (stop_file):
    stopwords = set([])

    # provide a default if needed
    if not stop_file:
        stop_file = "stop.txt"

    # check whether the path is fully qualified
    if os.path.isfile(stop_file):
        stop_path = stop_file

    # check for the file in the current working directory
    else:
        cwd = os.getcwd()
        stop_path = os.path.join(cwd, stop_file)

        # check for the file in the same directory as this code module
        if not os.path.isfile(stop_path):
            loc = os.path.realpath( os.path.join(cwd, os.path.dirname(__file__)) )
            stop_path = os.path.join(loc, stop_file)

    try:
        with open(stop_path, "r") as f:
            for line in f.readlines():
                stopwords.add(line.strip().lower())
    except FileNotFoundError:
        pass

    return stopwords


def find_chunk_sub (phrase, np, i):
    for j in iter(range(0, len(np))):
        p = phrase[i + j]

        if p.text != np[j]:
            return None

    return phrase[i:i + len(np)]


def find_chunk (phrase, np):
    """
    leverage noun phrase chunking
    """
    for i in iter(range(0, len(phrase))):
        parsed_np = find_chunk_sub(phrase, np, i)

        if parsed_np:
            return parsed_np


def enumerate_chunks (phrase, spacy_nlp):
    """
    iterate through the noun phrases
    """
    if (len(phrase) > 1):
        found = False
        text = " ".join([rl.text for rl in phrase])
        doc = spacy_nlp(text.strip())

        for np in doc.noun_chunks:
            if np.text != text:
                found = True
                yield np.text, find_chunk(phrase, np.text.split(" "))

        if not found and all([rl.pos[0] != "v" for rl in phrase]):
            yield text, phrase


def collect_keyword (sent, ranks, stopwords):
    """
    iterator for collecting the single-word keyphrases
    """
    for w in sent:
        if (w.word_id > 0) and (w.root in ranks) and (w.pos[0] in "NV") and (w.root not in stopwords):
            rl = RankedLexeme(text=w.raw.lower(), rank=ranks[w.root]/2.0, ids=[w.word_id], pos=w.pos.lower(), count=1)

            if DEBUG:
                print(rl)

            yield rl


def find_entity (sent, ranks, ent, i):
    if i >= len(sent):
        return None, None
    else:
        for j in iter(range(0, len(ent))):
            w = sent[i + j]

            if w.raw != ent[j]:
                return find_entity(sent, ranks, ent, i + 1)

        w_ranks = []
        w_ids = []

        for w in sent[i:i + len(ent)]:
            w_ids.append(w.word_id)

            if w.root in ranks:
                w_ranks.append(ranks[w.root])
            else:
                w_ranks.append(0.0)

        return w_ranks, w_ids


def collect_entities (sent, ranks, stopwords, spacy_nlp):
    """
    iterator for collecting the named-entities
    """
    global DEBUG
    sent_text = " ".join([w.raw for w in sent])

    if DEBUG:
        print("sent:", sent_text)

    for ent in spacy_nlp(sent_text).ents:
        if DEBUG:
            print("NER:", ent.label_, ent.text)

        if (ent.label_ not in ["CARDINAL"]) and (ent.text.lower() not in stopwords):
            w_ranks, w_ids = find_entity(sent, ranks, ent.text.split(" "), 0)

            if w_ranks and w_ids:
                rl = RankedLexeme(text=ent.text.lower(), rank=w_ranks, ids=w_ids, pos="np", count=1)

                if DEBUG:
                    print(rl)

                yield rl


def collect_phrases (sent, ranks, spacy_nlp):
    """
    iterator for collecting the noun phrases
    """
    tail = 0
    last_idx = sent[0].idx - 1
    phrase = []

    while tail < len(sent):
        w = sent[tail]

        if (w.word_id > 0) and (w.root in ranks) and ((w.idx - last_idx) == 1):
            # keep collecting...
            rl = RankedLexeme(text=w.raw.lower(), rank=ranks[w.root], ids=w.word_id, pos=w.pos.lower(), count=1)
            phrase.append(rl)
        else:
            # just hit a phrase boundary
            for text, p in enumerate_chunks(phrase, spacy_nlp):
                if p:
                    id_list = [rl.ids for rl in p]
                    rank_list = [rl.rank for rl in p]
                    np_rl = RankedLexeme(text=text, rank=rank_list, ids=id_list, pos="np", count=1)

                    if DEBUG:
                        print(np_rl)

                    yield np_rl

            phrase = []

        last_idx = w.idx
        tail += 1


def calc_rms (values):
    """
    calculate a root-mean-squared metric for a list of float values
    """
    #return math.sqrt(sum([x**2.0 for x in values])) / float(len(values))
    # take the max() which works fine
    return max(values)


def normalize_key_phrases (path, ranks, stopwords=None, spacy_nlp=None, skip_ner=True):
    """
    collect keyphrases, named entities, etc., while removing stop words
    """
    global STOPWORDS, SPACY_NLP

    # set up the stop words
    if (type(stopwords) is list) or (type(stopwords) is set):
        # explicit conversion to a set, for better performance
        stopwords = set(stopwords)
    else:
        if not STOPWORDS:
            STOPWORDS = load_stopwords(stopwords)

        stopwords = STOPWORDS

    # set up the spaCy NLP parser
    if not spacy_nlp:
        if not SPACY_NLP:
            SPACY_NLP = spacy.load("en")

        spacy_nlp = SPACY_NLP

    # collect keyphrases
    single_lex = {}
    phrase_lex = {}

    if isinstance(path, str):
        path = json_iter(path)

    for meta in path:
        sent = [w for w in map(WordNode._make, meta["graf"])]

        for rl in collect_keyword(sent, ranks, stopwords):
            id = str(rl.ids)

            if id not in single_lex:
                single_lex[id] = rl
            else:
                prev_lex = single_lex[id]
                single_lex[id] = rl._replace(count = prev_lex.count + 1)

        if not skip_ner:
            for rl in collect_entities(sent, ranks, stopwords, spacy_nlp):
                id = str(rl.ids)

                if id not in phrase_lex:
                    phrase_lex[id] = rl
                else:
                    prev_lex = phrase_lex[id]
                    phrase_lex[id] = rl._replace(count = prev_lex.count + 1)

        for rl in collect_phrases(sent, ranks, spacy_nlp):
            id = str(rl.ids)

            if id not in phrase_lex:
                phrase_lex[id] = rl
            else:
                prev_lex = phrase_lex[id]
                phrase_lex[id] = rl._replace(count = prev_lex.count + 1)

    # normalize ranks across single keywords and longer phrases:
    #    * boost the noun phrases based on their length
    #    * penalize the noun phrases for repeated words
    rank_list = [rl.rank for rl in single_lex.values()]

    if len(rank_list) < 1:
        max_single_rank = 0
    else:
        max_single_rank = max(rank_list)

    repeated_roots = {}

    for rl in sorted(phrase_lex.values(), key=lambda rl: len(rl), reverse=True):
        rank_list = []

        for i in iter(range(0, len(rl.ids))):
            id = rl.ids[i]

            if not id in repeated_roots:
                repeated_roots[id] = 1.0
                rank_list.append(rl.rank[i])
            else:
                repeated_roots[id] += 1.0
                rank_list.append(rl.rank[i] / repeated_roots[id])

        phrase_rank = calc_rms(rank_list)
        single_lex[str(rl.ids)] = rl._replace(rank = phrase_rank)

    # scale all the ranks together, so they sum to 1.0
    sum_ranks = sum([rl.rank for rl in single_lex.values()])

    for rl in sorted(single_lex.values(), key=lambda rl: rl.rank, reverse=True):
        if sum_ranks > 0.0:
            rl = rl._replace(rank=rl.rank / sum_ranks)
        elif rl.rank == 0.0:
            rl = rl._replace(rank=0.1)

        rl = rl._replace(text=re.sub(r"\s([\.\,\-\+\:\@])\s", r"\1", rl.text))
        yield rl


######################################################################
## sentence significance

def mh_digest (data):
    """
    create a MinHash digest
    """
    num_perm = 512
    m = MinHash(num_perm)

    for d in data:
        m.update(d.encode('utf8'))

    return m


def rank_kernel (path):
    """
    return a list (matrix-ish) of the key phrases and their ranks
    """
    kernel = []

    if isinstance(path, str):
        path = json_iter(path)

    for meta in path:
        if not isinstance(meta, RankedLexeme):
            rl = RankedLexeme(**meta)
        else:
            rl = meta

        m = mh_digest(map(lambda x: str(x), rl.ids))
        kernel.append((rl, m,))

    return kernel


def top_sentences (kernel, path):
    """
    determine distance for each sentence
    """
    key_sent = {}
    i = 0

    if isinstance(path, str):
        path = json_iter(path)

    for meta in path:
        graf = meta["graf"]
        tagged_sent = [WordNode._make(x) for x in graf]
        text = " ".join([w.raw for w in tagged_sent])

        m_sent = mh_digest([str(w.word_id) for w in tagged_sent])
        dist = sum([m_sent.jaccard(m) * rl.rank for rl, m in kernel])
        key_sent[text] = (dist, i)
        i += 1

    for text, (dist, i) in sorted(key_sent.items(), key=lambda x: x[1][0], reverse=True):
        yield SummarySent(dist=dist, idx=i, text=text)


######################################################################
## document summarization

def limit_keyphrases (path, phrase_limit=20):
    """
    iterator for the most significant key phrases
    """
    rank_thresh = None

    if isinstance(path, str):
        lex = []

        for meta in json_iter(path):
            rl = RankedLexeme(**meta)
            lex.append(rl)
    else:
        lex = path

    if len(lex) > 0:
        rank_thresh = statistics.mean([rl.rank for rl in lex])
    else:
            rank_thresh = 0

    used = 0

    for rl in lex:
        if rl.pos[0] != "v":
            if (used > phrase_limit) or (rl.rank < rank_thresh):
                return

            used += 1
            yield rl.text.replace(" - ", "-")


def limit_sentences (path, word_limit=100):
    """
    iterator for the most significant sentences, up to a specified limit
    """
    word_count = 0

    if isinstance(path, str):
        path = json_iter(path)

    for meta in path:
        if not isinstance(meta, SummarySent):
            p = SummarySent(**meta)
        else:
            p = meta

        sent_text = p.text.strip().split(" ")
        sent_len = len(sent_text)

        if (word_count + sent_len) > word_limit:
            break
        else:
            word_count += sent_len
            yield sent_text, p.idx


def make_sentence (sent_text):
    """
    construct a sentence text, with proper spacing
    """
    lex = []
    idx = 0

    for word in sent_text:
        if len(word) > 0:
            if (idx > 0) and not (word[0] in ",.:;!?-\"'"):
                lex.append(" ")

            lex.append(word)

        idx += 1

    return "".join(lex)


######################################################################
## common utilities

def json_iter (path):
    """
    iterator for JSON-per-line in a file pattern
    """
    with open(path, 'r') as f:
        for line in f.readlines():
            yield json.loads(line)


def pretty_print (obj, indent=False):
    """
    pretty print a JSON object
    """

    if indent:
        return json.dumps(obj, sort_keys=True, indent=2, separators=(',', ': '))
    else:
        return json.dumps(obj, sort_keys=True)
