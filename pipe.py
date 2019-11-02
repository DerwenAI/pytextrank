#!/usr/bin/env python
# encoding: utf-8

from math import sqrt
from operator import itemgetter
import logging
import networkx as nx
import spacy
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
LOGGER = logging.getLogger("PyTR")

POS_KEPT = ["ADJ", "NOUN", "PROPN", "VERB"]


def increment_edge (graph, node0, node1):
    """
    increment the weight for an edge between the two given nodes
    creating the edge first if needed
    """

    if LOGGER:
        LOGGER.debug("link {} {}".format(node0, node1))
    
    if graph.has_edge(node0, node1):
        graph[node0][node1]["weight"] += 1.0
    else:
        graph.add_edge(node0, node1, weight=1.0)


def link_sentence (doc, sent, lemma_graph, seen_lemma):
    """
    link nodes and edges into the lemma graph for one parsed sentence
    """

    visited_tokens = []
    visited_nodes = []

    for i in range(sent.start, sent.end):
        token = doc[i]

        if token.pos_ in POS_KEPT:
            key = (token.lemma_, token.pos_)

            if key not in seen_lemma:
                seen_lemma[key] = set([token.i])
            else:
                seen_lemma[key].add(token.i)

            node_id = list(seen_lemma.keys()).index(key)

            if not node_id in lemma_graph:
                lemma_graph.add_node(node_id)

            if LOGGER:
                LOGGER.debug("visit {} {}".format(visited_tokens, visited_nodes))
                LOGGER.debug("range {}".format(list(range(len(visited_tokens) - 1, -1, -1))))
            
            for prev_token in range(len(visited_tokens) - 1, -1, -1):
                if LOGGER:
                    LOGGER.debug("prev_tok {} {}".format(prev_token, (token.i - visited_tokens[prev_token])))
                
                if (token.i - visited_tokens[prev_token]) <= 3:
                    increment_edge(lemma_graph, node_id, visited_nodes[prev_token])
                else:
                    break

            if LOGGER:
                LOGGER.debug(" -- {} {} {} {} {} {}".format(token.i, token.text, token.lemma_, token.pos_, visited_tokens, visited_nodes))

            visited_tokens.append(token.i)
            visited_nodes.append(node_id)


def collect_phrases (chunk, phrases, counts, seen_lemma, ranks):
    """
    collect the top-ranked phrases from the lemma graph
    """

    chunk_len = chunk.end - chunk.start + 1
    sq_sum_rank = 0.0
    non_lemma = 0
    compound_key = set([])

    for i in range(chunk.start, chunk.end):
        token = doc[i]
        key = (token.lemma_, token.pos_)
        
        if key in seen_lemma:
            node_id = list(seen_lemma.keys()).index(key)
            rank = ranks[node_id]
            sq_sum_rank += rank
            compound_key.add(key)
        
            if LOGGER:
                LOGGER.debug(" {} {} {} {}".format(token.lemma_, token.pos_, node_id, rank))
        else:
            non_lemma += 1
    
    # although the noun chunking is greedy, we discount the ranks using a
    # point estimate based on the number of non-lemma tokens within a phrase

    non_lemma_discount = chunk_len / (chunk_len + (2.0 * non_lemma) + 1.0)

    # use root mean square (RMS) to normalize the contributions of all the tokens

    phrase_rank = sqrt(sq_sum_rank / (chunk_len + non_lemma))
    phrase_rank *= non_lemma_discount

    # remove spurious punctuation

    phrase = chunk.text.lower().replace("'", "")

    # create a unique key for the the phrase based on its lemma components

    compound_key = tuple(sorted(list(compound_key)))
    
    if not compound_key in phrases:
        phrases[compound_key] = set([ (phrase, phrase_rank) ])
        counts[compound_key] = 1
    else:
        phrases[compound_key].add( (phrase, phrase_rank) )
        counts[compound_key] += 1

    if LOGGER:
        LOGGER.debug("{} {} {} {} {} {}".format(phrase_rank, chunk.text, chunk.start, chunk.end, chunk_len, counts[compound_key]))


def text_rank (doc):
    """
    iterate through the sentences to construct the lemma graph, returning
    the top-ranked phrases
    """

    lemma_graph = nx.Graph()
    seen_lemma = {}

    for sent in doc.sents:
        link_sentence(doc, sent, lemma_graph, seen_lemma)
        #break # only test one sentence

    if LOGGER:
        LOGGER.debug(seen_lemma)

    # to run the algorithm, we use PageRank – which is
    # approximately eigenvalue centrality – to calculate ranks for
    # each of the nodes in the lemma graph

    ranks = nx.pagerank(lemma_graph)

    # collect the top-ranked phrases based on both the noun chunks and
    # the named entities

    phrases = {}
    counts = {}

    for chunk in doc.noun_chunks:
        collect_phrases(chunk, phrases, counts, seen_lemma, ranks)

    for ent in doc.ents:
        collect_phrases(ent, phrases, counts, seen_lemma, ranks)

    # since noun chunks can be expressed in different ways (e.g., may
    # have articles or prepositions), we need to find a minimum span
    # for each phrase based on combinations of lemmas

    min_phrases = {}

    for compound_key, rank_tuples in phrases.items():
        l = list(rank_tuples)
        l.sort(key=itemgetter(1), reverse=True)
    
        phrase, rank = l[0]
        count = counts[compound_key]
    
        min_phrases[phrase] = (rank, count)

    # yield results
    phrase_iter = iter([(p, r, c) for p, (r, c) in sorted(min_phrases.items(), key=lambda x: x[1][0], reverse=True)])

    return phrase_iter, lemma_graph


if __name__ == "__main__":
    text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types."

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    phrase_iter, lemma_graph = text_rank(doc)
    
    for phrase, rank, count in phrase_iter:
        print("{:.4f} {:5d}  {}".format(rank, count, phrase))
