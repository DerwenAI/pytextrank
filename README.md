# PyTextRank

*PyTextRank* is a Python implementation of *TextRank* as a
[spaCy extension](https://explosion.ai/blog/spacy-v2-pipelines-extensions),
for working with text documents to:

  - extract the top-ranked phrases
  - run extractive summarization

This work is based on the paper:

  - ["TextRank: Bringing Order into Text"](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)  
[**Rada Mihalcea**](https://web.eecs.umich.edu/~mihalcea/), 
[**Paul Tarau**](https://www.cse.unt.edu/~tarau/);  
[*Empirical Methods in Natural Language Processing*](https://www.researchgate.net/publication/200044196_TextRank_Bringing_Order_into_Texts)  
(2004)

Several modifications improve on the algorithm originally described in the paper:

  - fixed bug; see [Java impl, 2008](https://github.com/ceteri/textrank)
  - uses *lemmatization* in place of stemming
  - includes verbs in the graph, but not in resulting phrases
  - leverages preprocessing based on *noun chunking* and *named entity recognition*
  - provides *extractive summarization* based on vectors of ranked
    phrases
  - allows use of a *knowledge graph* for enriching the lemma graph and subsequent phrase extraction and summarization

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

If you install directly from this Git repo, be sure to install the dependencies as well:

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

For course materials and training, please check for calendar updates in
the article
["Natural Language Processing in Python"](https://medium.com/derwen/natural-language-processing-in-python-832b0a99791b).

Let us know if you find this useful, tell us about use cases,
describe what else you would like to see integrated, etc.
If you have questions about related consulting work in natural language, machine learning, knowledge graph, or other AI applications, contact 
[Derwen, Inc.](https://derwen.ai/contact)


## Attribution

*PyTextRank* has an [MIT](https://spdx.org/licenses/MIT.html) license,
which is succinct and simplifies use in commercial applications.

Please use the following Bibtex entry for citing *PyTextRank* in publications:

```
@Misc{PyTextRank,
author = {Nathan, Paco},
title = {PyTextRank, a Python implementation of TextRank for text document NLP parsing and summarization},
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