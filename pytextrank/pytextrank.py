#!/usr/bin/env python
# encoding: utf-8

from collections import defaultdict, OrderedDict
from math import sqrt
from operator import itemgetter
from spacy.tokens import Doc
import graphviz
import json
import logging
import networkx as nx
import os
import os.path
import re
import spacy
import string
import sys
import time
import unicodedata


######################################################################
## utility functions
######################################################################

PAT_FORWARD = re.compile("\n\-+ Forwarded message \-+\n")
PAT_REPLIED = re.compile("\nOn.*\d+.*\n?wrote\:\n+\>")
PAT_UNSUBSC = re.compile("\n\-+\nTo unsubscribe,.*\nFor additional commands,.*")


def split_grafs (lines):
    """
    segment raw text, given as a list of lines, into paragraphs
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
    global PAT_FORWARD, PAT_REPLIED, PAT_UNSUBSC

    if is_email:
        text = filter(lambda x: x in string.printable, text)

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


def maniacal_scrubber (text):
    """
    it scrubs the garble from its stream...
    or it gets the debugger again
    """
    x = " ".join(map(lambda s: s.strip(), text.split("\n"))).strip()

    x = x.replace('“', '"').replace('”', '"')
    x = x.replace("‘", "'").replace("’", "'").replace("`", "'")
    x = x.replace("…", "...").replace("–", "-")

    x = str(unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8"))

    # some web content returns "not string" ??
    #
    # ostensibly that's no longer possible in Py 3.x even so some
    # crazy-making "mixed modes" of character encodings have been
    # found in the wild -- YMMV

    try:
        assert type(x).__name__ == "str"
    except AssertionError:
        print("not a string?", type(line), line)

    return x


def default_scrubber (text):
    """
    remove spurious punctuation (for English)
    """
    return text.lower().replace("'", "")


######################################################################
## class definitions
######################################################################

class CollectedPhrase:
    """
    represents one phrase during the collection process
    """

    def __init__ (self, chunk, scrubber):
        self.sq_sum_rank = 0.0
        self.non_lemma = 0
        
        self.chunk = chunk
        self.text = scrubber(chunk.text)


    def __repr__ (self):
        return "{:.4f} ({},{}) {} {}".format(
            self.rank, self.chunk.start, self.chunk.end, self.text, self.key
        )


    def range (self):
        """
        generate the index range for the span of tokens in this phrase
        """
        return range(self.chunk.start, self.chunk.end)


    def set_key (self, compound_key):
        """
        create a unique key for the the phrase based on its lemma components
        """
        self.key = tuple(sorted(list(compound_key)))


    def calc_rank (self):
        """
        since noun chunking is greedy, we normalize the rank values
        using a point estimate based on the number of non-lemma
        tokens within the phrase
        """
        chunk_len = self.chunk.end - self.chunk.start + 1
        non_lemma_discount = chunk_len / (chunk_len + (2.0 * self.non_lemma) + 1.0)

        # normalize the contributions of all the kept lemma tokens
        # within the phrase using root mean square (RMS)

        self.rank = sqrt(self.sq_sum_rank / (chunk_len + self.non_lemma)) * non_lemma_discount


class Phrase:
    """
    represents one extracted phrase
    """

    def __init__ (self, text, rank, count, phrase_list):
        self.text = text
        self.rank = rank
        self.count = count
        self.chunks = [p.chunk for p in phrase_list]


    def __repr__ (self):
        return self.text


class TextRank:
    """
    Python impl of TextRank by Milhacea, et al., as a spaCy extension,
    used to extract the top-ranked phrases from a text document
    """
    _EDGE_WEIGHT = 1.0
    _POS_KEPT = ["ADJ", "NOUN", "PROPN", "VERB"]
    _TOKEN_LOOKBACK = 3
    

    def __init__ (
            self,
            edge_weight=_EDGE_WEIGHT,
            logger=None,
            pos_kept=_POS_KEPT,
            scrubber=default_scrubber,
            token_lookback=_TOKEN_LOOKBACK
    ):
        self.edge_weight = edge_weight
        self.logger = logger
        self.pos_kept = pos_kept
        self.scrubber = scrubber
        self.stopwords = defaultdict(list)
        self.token_lookback = token_lookback

        self.doc = None
        self.reset()


    def reset (self):
        """
        initialize the data structures needed for extracting phrases
        removing any state
        """
        self.elapsed_time = 0.0
        self.lemma_graph = nx.Graph()
        self.phrases = defaultdict(list)
        self.ranks = {}
        self.seen_lemma = OrderedDict()


    def load_stopwords (self, path="stop.json"):
        """
        load a list of "stop words" that get ignored when constructing
        the lemma graph -- NB: be cautious when using this feature
        """
        stop_path = None

        # check if the path is fully qualified, or if the file is in
        # the current working directory

        if os.path.isfile(path):
            stop_path = path
        else:
            cwd = os.getcwd()
            stop_path = os.path.join(cwd, path)

            if not os.path.isfile(stop_path):
                loc = os.path.realpath(os.path.join(cwd, os.path.dirname(__file__)))
                stop_path = os.path.join(loc, path)

        try:
            with open(stop_path, "r") as f:
                data = json.load(f)

                for lemma, pos_list in data.items():
                    self.stopwords[lemma] = pos_list
        except FileNotFoundError:
            pass


    def increment_edge (self, node0, node1):
        """
        increment the weight for an edge between the two given nodes,
        creating the edge first if needed
        """
        if self.logger:
            self.logger.debug("link {} {}".format(node0, node1))
    
        if self.lemma_graph.has_edge(node0, node1):
            self.lemma_graph[node0][node1]["weight"] += self.edge_weight
        else:
            self.lemma_graph.add_edge(node0, node1, weight=self.edge_weight)


    def link_sentence (self, sent):
        """
        link nodes and edges into the lemma graph for one parsed sentence
        """
        visited_tokens = []
        visited_nodes = []

        for i in range(sent.start, sent.end):
            token = self.doc[i]

            if token.pos_ in self.pos_kept:
                # skip any stop words...
                lemma = token.lemma_.lower().strip()

                if lemma in self.stopwords and token.pos_ in self.stopwords[lemma]:
                    continue

                # ...otherwise proceed
                key = (token.lemma_, token.pos_,)

                if key not in self.seen_lemma:
                    self.seen_lemma[key] = set([token.i])
                else:
                    self.seen_lemma[key].add(token.i)

                node_id = list(self.seen_lemma.keys()).index(key)

                if not node_id in self.lemma_graph:
                    self.lemma_graph.add_node(node_id)

                if self.logger:
                    self.logger.debug("visit {} {}".format(
                        visited_tokens, visited_nodes
                    ))
                    self.logger.debug("range {}".format(
                        list(range(len(visited_tokens) - 1, -1, -1))
                    ))
            
                for prev_token in range(len(visited_tokens) - 1, -1, -1):
                    if self.logger:
                        self.logger.debug("prev_tok {} {}".format(
                            prev_token, (token.i - visited_tokens[prev_token])
                        ))
                
                    if (token.i - visited_tokens[prev_token]) <= self.token_lookback:
                        self.increment_edge(node_id, visited_nodes[prev_token])
                    else:
                        break

                if self.logger:
                    self.logger.debug(" -- {} {} {} {} {} {}".format(
                        token.i, token.text, token.lemma_, token.pos_, visited_tokens, visited_nodes
                    ))

                visited_tokens.append(token.i)
                visited_nodes.append(node_id)


    def collect_phrases (self, chunk):
        """
        collect instances of phrases from the lemma graph
        based on the given chunk
        """
        phrase = CollectedPhrase(chunk, self.scrubber)
        compound_key = set([])

        for i in phrase.range():
            token = self.doc[i]
            key = (token.lemma_, token.pos_)
        
            if key in self.seen_lemma:
                node_id = list(self.seen_lemma.keys()).index(key)
                rank = self.ranks[node_id]
                phrase.sq_sum_rank += rank
                compound_key.add(key)
        
                if self.logger:
                    self.logger.debug(" {} {} {} {}".format(
                        token.lemma_, token.pos_, node_id, rank
                    ))
            else:
                phrase.non_lemma += 1
    
        phrase.set_key(compound_key)
        phrase.calc_rank()

        self.phrases[phrase.key].append(phrase)

        if self.logger:
            self.logger.debug(phrase)


    def calc_textrank (self):
        """
        iterate through each sentence in the doc, constructing a lemma graph
        then returning the top-ranked phrases
        """
        self.reset()
        t0 = time.time()

        for sent in self.doc.sents:
            self.link_sentence(sent)

        if self.logger:
            self.logger.debug(self.seen_lemma)

        # to run the algorithm, we use the NetworkX implementation of
        # PageRank – i.e., approximating eigenvalue centrality – to
        # calculate ranks for each of the nodes in the lemma graph

        self.ranks = nx.pagerank(self.lemma_graph)

        # collect the top-ranked phrases based on both the noun chunks
        # and the named entities

        for chunk in self.doc.noun_chunks:
            self.collect_phrases(chunk)

        for ent in self.doc.ents:
            self.collect_phrases(ent)

        # TODO:
        # there are edge cases where the built-in noun chunking in
        # spaCy fails to extract much, for example:

        # > "everything you need to know about student loan interest rates variable and fixed rates capitalization amortization student loan refinancing and more."

        # we should test `len(self.phrases.keys())` vs. a brute-force
        # noun chunking approach, then add the brute-force override to
        # `self.phrases`

        #for k, p in self.phrases.items():
        #    print(" >>", k, p)

        #for key, lemma in self.seen_lemma.items():
        #    node_id = list(self.seen_lemma.keys()).index(key)
        #    print(node_id, key, lemma, self.ranks[node_id])


        # since noun chunks can be expressed in different ways (e.g., may
        # have articles or prepositions), we need to find a minimum span
        # for each phrase based on combinations of lemmas

        min_phrases = {}

        for phrase_key, phrase_list in self.phrases.items():
            phrase_list.sort(key=lambda p: p.rank, reverse=True)
            best_phrase = phrase_list[0]
            min_phrases[best_phrase.text] = (best_phrase.rank, len(phrase_list), phrase_key)

        # yield results

        results = sorted(min_phrases.items(), key=lambda x: x[1][0], reverse=True)

        phrase_list = [
            Phrase(p, r, c, self.phrases[k]) for p, (r, c, k) in results
        ]

        t1 = time.time()
        self.elapsed_time = (t1 - t0) * 1000.0

        return phrase_list


    def write_dot (self, path="graph.dot"):
        """
        output the lemma graph in Dot file format
        """
        keys = list(self.seen_lemma.keys())
        dot = graphviz.Digraph()

        for node_id in self.lemma_graph.nodes():
            text = keys[node_id][0].lower()
            rank = self.ranks[node_id]
            label = "{} ({:.4f})".format(text, rank)
            dot.node(str(node_id), label)

        for edge in self.lemma_graph.edges():
            dot.edge(str(edge[0]), str(edge[1]), constraint="false")

        with open(path, "w") as f:
            f.write(dot.source)


    def summary (self, limit_phrases=10, limit_sentences=4, preserve_order=False):
        """
        run extractive summarization, based on vector distance 
        per sentence from the top-ranked phrases
        """
        unit_vector = []

        # construct a list of sentence boundaries with a phrase set
        # for each (initialized to empty)

        sent_bounds = [ [s.start, s.end, set([])] for s in self.doc.sents ]

        # iterate through the top-ranked phrases, added them to the
        # phrase vector for each sentence

        phrase_id = 0

        for p in self.doc._.phrases:
            unit_vector.append(p.rank)

            if self.logger:
                self.logger.debug(
                    "{} {} {}".format(phrase_id, p.text, p.rank)
                )
    
            for chunk in p.chunks:
                for sent_start, sent_end, sent_vector in sent_bounds:
                    if chunk.start >= sent_start and chunk.start <= sent_end:
                        sent_vector.add(phrase_id)

                        if self.logger:
                            self.logger.debug(
                                " {} {} {} {}".format(sent_start, chunk.start, chunk.end, sent_end)
                                )

                        break

            phrase_id += 1

            if phrase_id == limit_phrases:
                break

        # construct a unit_vector for the top-ranked phrases, up to
        # the requested limit

        sum_ranks = sum(unit_vector)

        try:
            unit_vector = [ rank/sum_ranks for rank in unit_vector ]
        except ZeroDivisionError:
            unit_vector = (0.0,) * len(unit_vector)

        # iterate through each sentence, calculating its euclidean
        # distance from the unit vector

        sent_rank = {}
        sent_id = 0

        for sent_start, sent_end, sent_vector in sent_bounds:
            sum_sq = 0.0
    
            for phrase_id in range(len(unit_vector)):
                if phrase_id not in sent_vector:
                    sum_sq += unit_vector[phrase_id]**2.0

            sent_rank[sent_id] = sqrt(sum_sq)
            sent_id += 1

        # extract the sentences with the lowest distance

        sent_text = {}
        sent_id = 0

        for sent in self.doc.sents:
            sent_text[sent_id] = sent
            sent_id += 1

        # build a list of sentence indices, sorted according to their
        # corresponding rank
        top_sent_ids = list(range(len(sent_rank)))
        top_sent_ids.sort(key=lambda sent_id: sent_rank[sent_id])
        # truncate to the given limit
        top_sent_ids = top_sent_ids[:limit_sentences]
        # sort in ascending order of index to preserve the order in which the
        # sentences appear in the original text
        if preserve_order:
            top_sent_ids.sort()
        # yield results, up to the limit requested
        for sent_id in top_sent_ids:
            yield sent_text[sent_id]


    def PipelineComponent (self, doc):
        """
        define a custom pipeline component for spaCy and extend the
        Doc class to add TextRank
        """
        self.doc = doc
        Doc.set_extension("phrases", force=True, default=[])
        Doc.set_extension("textrank", force=True, default=self)
        doc._.phrases = self.calc_textrank()

        return doc
