import pytextrank
import sys
import json

sometext = 'Compatibility of systems of linear constraints over the set of natural numbers. ' + \
           'Criteria of compatibility of a system of linear Diophantine equations, ' + \
           'strict inequations, and nonstrict inequations are considered. Upper bounds ' + \
           'for components of a minimal set of solutions and algorithms of construction of ' + \
           'minimal generating sets of solutions for all types of systems are given. ' + \
           'These criteria and the corresponding algorithms for constructing a minimal ' + \
           'supporting set of solutions can be used in solving all the considered types ' + \
           'systems and systems of mixed types.'
someothertext = 'Amazon.com, Inc. is located in Seattle, WA and was founded July 5th, 1994 by Jeff Bezos, ' + \
    'allowing customers to buy everything from books to blenders. Seattle is north of Portland and ' + \
    'south of Vancouver, BC. Other notable Seattle - based companies are Starbucks and Boeing.'

docs = [{
    'text': someothertext,
    'id': 777}]

grafs = [{'graf': graf.graf} for graf in pytextrank.parse_doc(docs)]
graph, ranks = pytextrank.text_rank(grafs)
rank_list = [rl._asdict() for rl in pytextrank.normalize_key_phrases(grafs, ranks, skip_ner=False)]
kernel = pytextrank.rank_kernel(rank_list)
sents = [s._asdict() for s in pytextrank.top_sentences(kernel, grafs)]
phrases = [p for p in pytextrank.limit_keyphrases(rank_list, phrase_limit=6)]

sent_iter = sorted(pytextrank.limit_sentences(sents, word_limit=150), key=lambda x: x[1])
sents = [pytextrank.make_sentence(sent_text) for sent_text, idx in sent_iter]
graf_text = ' '.join(sents)

print("\n**excerpts:** %s\n\n**keywords:** %s" % (graf_text, phrases,))