# PyTextRank

**PyTextRank** is a Python implementation of *TextRank* as a
[spaCy extension](https://explosion.ai/blog/spacy-v2-pipelines-extensions),
to:

  - extract the top-ranked phrases from text documents
  - run extractive summarization of text documents
  - infer links from unstructured text into structured data


## Background

Note that **PyTextRank** is intended to provide support for
[*entity linking*](http://nlpprogress.com/english/entity_linking.html),
in contrast to the more commonplace usage of
[*named entity recognition*](http://nlpprogress.com/english/named_entity_recognition.html).
These approaches can be used together in complementary ways to improve
the results overall.
The introduction of graph algorithms -- notably,
[*eigenvalue centrality*](https://demonstrations.wolfram.com/NetworkCentralityUsingEigenvectors/)
-- provides a more flexible and robust basis for integrating additional
techniques that enhance the natural language work being performed.

Internally **PyTextRank** constructs a *lemma graph* to represent links
among the candidate phrases (e.g., unrecognized entities) and their
supporting language.
Generally speaking, any means of enriching that graph prior to phrase
ranking will tend to improve results.
Possible ways to enrich the lemma graph include
[*coreference resolution*](http://nlpprogress.com/english/coreference_resolution.html)
and
[*semantic relations*](https://en.wikipedia.org/wiki/Hyponymy_and_hypernymy),
as well as leveraging *knowledge graphs* in the general case.

For example,
[DBpedia](https://wiki.dbpedia.org/)
and
[WordNet](https://spacy.io/universe/project/spacy-wordnet)
both provide means for inferring links among entities, and can be applied
even in cases where those links are not explicit within the text.
Consider a paragraph that mentions `cats` and `kittens`: there is an implied
semantic relation between the two nouns since the lemma `kitten` is a hyponym
of the lemma `cat` so an inferred link can be added between them.
Purpose-built knowledge graphs can be applied to enrich the lemma graph for
specific use cases.

This has an additional benefit of linking parsed and annotated documents
into more structured data, and can also be used to support
[*knowledge graph construction*](https://www.akbc.ws/).

The *TextRank* algorithm used here is based on research published in:

  - ["TextRank: Bringing Order into Text"](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)  
[**Rada Mihalcea**](https://web.eecs.umich.edu/~mihalcea/), 
[**Paul Tarau**](https://www.cse.unt.edu/~tarau/);  
[*Empirical Methods in Natural Language Processing*](https://www.researchgate.net/publication/200044196_TextRank_Bringing_Order_into_Texts)  
(2004)

Several modifications in **PyTextRank** improve on the algorithm originally
described in the paper:

  - fixes a bug: see [Java impl, 2008](https://github.com/ceteri/textrank)
  - uses *lemmatization* in place of stemming
  - includes verbs in the graph (but not in the resulting phrases)
  - leverages preprocessing via *noun chunking* and *named entity recognition*
  - provides *extractive summarization* based on ranked phrases

This implementation was inspired by the
[Williams 2016](http://mike.place/2016/summarization/)
talk on text summarization.


## Installation

Prerequisites:

- [Python 3.x](https://www.python.org/downloads/)
- [spaCy](https://spacy.io/docs/usage/)
- [NetworkX](http://networkx.readthedocs.io/)

To install from [PyPi](https://pypi.python.org/pypi/pytextrank):

```
pip install pytextrank
```

If you install directly from this Git repo, be sure to install the dependencies
as well:

```
pip install -r requirements.txt
```


## Usage

For example usage, see the 
[PyTextRank wiki](https://github.com/DerwenAI/pytextrank/wiki).
If you need to troubleshoot any problems:

  - use [GitHub issues](https://github.com/DerwenAI/pytextrank/issues)
    (recommended)
  - search [related discussions on StackOverflow](https://stackoverflow.com/search?q=pytextrank)

For course materials and training, please check for calendar updates
in the article
["Natural Language Processing in Python"](https://medium.com/derwen/natural-language-processing-in-python-832b0a99791b).

Let us know if you find this useful, tell us about use cases, describe
what else you would like to see integrated, etc.
If you have inquiries about related consulting work in machine learning,
natural language, knowledge graph, and other AI applications, contact 
[Derwen, Inc.](https://derwen.ai/contact)


## Attribution

**PyTextRank** has an [MIT](https://spdx.org/licenses/MIT.html) license,
which is succinct and simplifies use in commercial applications.

Please use the following BibTeX entry for citing **PyTextRank** in
publications:

```
@Misc{PyTextRank,
author = {Nathan, Paco},
title = {PyTextRank, a Python implementation of TextRank for phrase extraction and summarization of text documents},
    howpublished = {\url{https://github.com/DerwenAI/pytextrank/}},
    year = {2016}
    }
```


## Kudos

Many thanks to contributors:
[@htmartin](https://github.com/htmartin),
[@williamsmj](https://github.com/williamsmj/),
[@mattkohl](https://github.com/mattkohl),
[@vanita5](https://github.com/vanita5),
[@HarshGrandeur](https://github.com/HarshGrandeur),
[@mnowotka](https://github.com/mnowotka),
[@kjam](https://github.com/kjam),
[@dvsrepo](https://github.com/dvsrepo),
[@SaiThejeshwar](https://github.com/SaiThejeshwar),
[@laxatives](https://github.com/laxatives),
[@dimmu](https://github.com/dimmu), 
and for support from [Derwen, Inc.](https://derwen.ai/)

![noam](noam.jpg)