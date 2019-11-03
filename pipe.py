#!/usr/bin/env python
# encoding: utf-8

from collections import defaultdict 
from math import sqrt
from spacy.tokens import Doc
import logging
import networkx as nx
import spacy
import sys
import time
import unicodedata


def default_scrubber (text):
    """
    remove spurious punctuation (for English)
    """
    return text.lower().replace("'", "")


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

    # some web content returns "not string" ?? ostensibly no longer possibly in Py 3.x
    # fyi, there are crazy "mixed modes" of character encodings found in the wild...

    try:
        assert type(x).__name__ == "str"
    except AssertionError:
        print("not a string?", type(line), line)

    return x


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
        self.token_lookback = token_lookback

        self.doc = None
        self.reset()


    def reset (self):
        """
        reset the data structures to default values, removing any state
        """
        self.elapsed_time = 0.0
        self.lemma_graph = nx.Graph()
        self.phrases = defaultdict(list)
        self.ranks = {}
        self.seen_lemma = {}


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
                key = (token.lemma_, token.pos_)

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
        t0 = time.time()

        for sent in self.doc.sents:
            self.link_sentence(sent)
            #break # only test one sentence

        if self.logger:
            self.logger.debug(self.seen_lemma)

        # to run the algorithm, we use PageRank – i.e., approximating
        # eigenvalue centrality – to calculate ranks for each of the
        # nodes in the lemma graph

        self.ranks = nx.pagerank(self.lemma_graph)

        # collect the top-ranked phrases based on both the noun chunks
        # and the named entities

        for chunk in self.doc.noun_chunks:
            self.collect_phrases(chunk)

        for ent in self.doc.ents:
            self.collect_phrases(ent)

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


    def PipelineComponent (self, doc):
        """
        define a custom pipeline component for spaCy
        and extend the Doc class to add TextRank
        """
        self.doc = doc
        Doc.set_extension("phrases", default=self.calc_textrank())

        return doc


if __name__ == "__main__":
    text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types."

    nlp = spacy.load("en_core_web_sm")

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logger = logging.getLogger("PyTR")

    tr = TextRank(logger=None)
    nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

    doc = nlp(text)

    print("pipeline", nlp.pipe_names)
    print("elapsed time: {} ms".format(tr.elapsed_time))

    for phrase in doc._.phrases:
        print("{:.4f} {:5d}  {}".format(phrase.rank, phrase.count, phrase.text))
        print(phrase.chunks)
