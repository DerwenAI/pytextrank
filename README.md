# PyTextRank

**PyTextRank** is a Python implementation of *TextRank* as a
[spaCy pipeline extension](https://spacy.io/universe/project/spacy-pytextrank),
used to:

  - extract the top-ranked phrases from text documents
  - infer links from unstructured text into structured data
  - run extractive summarization of text documents

## Background

Note that **PyTextRank** is intended to provide support for
[*entity linking*](http://nlpprogress.com/english/entity_linking.html),
in contrast to the more commonplace usage of
[*named entity recognition*](http://nlpprogress.com/english/named_entity_recognition.html).
These approaches can be used together in complementary ways to improve
the results overall.
The introduction of graph algorithms -- notably,
[*eigenvector centrality*](https://demonstrations.wolfram.com/NetworkCentralityUsingEigenvectors/)
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
[WordNet](https://spacy.io/universe/project/spacy-wordnet)
and
[DBpedia](https://wiki.dbpedia.org/)
both provide means for inferring links among entities, and purpose-built knowledge
graphs can be applied for specific use cases.
These can help enrich a lemma graph even in cases where links are not explicit 
within the text.
Consider a paragraph that mentions `cats` and `kittens` in different sentences: 
an implied semantic relation exists between the two nouns since the lemma `kitten` 
is a hyponym of the lemma `cat` -- such that an inferred link can be added 
between them.

This has an additional benefit of linking parsed and annotated documents
into more structured data, and can also be used to support
[*knowledge graph construction*](https://www.akbc.ws/).

The *TextRank* algorithm used here is based on research published in:  
["TextRank: Bringing Order into Text"](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf)  
[**Rada Mihalcea**](https://web.eecs.umich.edu/~mihalcea/), 
[**Paul Tarau**](https://www.cse.unt.edu/~tarau/)  
[*Empirical Methods in Natural Language Processing*](https://www.researchgate.net/publication/200044196_TextRank_Bringing_Order_into_Texts) (2004)

Several modifications in **PyTextRank** improve on the algorithm originally
described in the paper:

  - fixed a bug: see [Java impl, 2008](https://github.com/ceteri/textrank)
  - use *lemmatization* in place of stemming
  - include verbs in the graph (but not in the resulting phrases)
  - leverage preprocessing via *noun chunking* and *named entity recognition*
  - provide *extractive summarization* based on ranked phrases

This implementation was inspired by the
[Williams 2016](http://mike.place/2016/summarization/)
talk on text summarization.
Note that while there are better approaches for
[*summarizing text*](http://nlpprogress.com/english/summarization.html),
questions linger about some of the top contenders -- see:
[1](https://arxiv.org/abs/1909.03004),
[2](https://arxiv.org/abs/1906.02243).
Arguably, having alternatives such as this allow for cost trade-offs.


## Installation

Prerequisites:

- [Python 3.5+](https://www.python.org/downloads/)
- [spaCy](https://spacy.io/docs/usage/)
- [NetworkX](http://networkx.readthedocs.io/)
- [GraphViz](https://graphviz.readthedocs.io/)

To install from [PyPi](https://pypi.python.org/pypi/pytextrank):

```
pip install pytextrank
python -m spacy download en_core_web_sm
```

If you install directly from this Git repo, be sure to install the dependencies
as well:

```
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```


## Usage

```
import spacy
import pytextrank

# example text
text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types."

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

doc = nlp(text)

# examine the top-ranked phrases in the document
for p in doc._.phrases:
    print("{:.4f} {:5d}  {}".format(p.rank, p.count, p.text))
    print(p.chunks)
```

For other example usage, see the 
[PyTextRank wiki](https://github.com/DerwenAI/pytextrank/wiki).
If you need to troubleshoot any problems:

  - use [GitHub issues](https://github.com/DerwenAI/pytextrank/issues) (most recommended)
  - search [related discussions on StackOverflow](https://stackoverflow.com/search?q=pytextrank)
  - tweet to `#textrank` on [Twitter](https://twitter.com/search?q=%23textrank) (cc `@pacoid`)

For related course materials and training, please check for calendar updates in the article
["Natural Language Processing in Python"](https://medium.com/derwen/natural-language-processing-in-python-832b0a99791b).

Let us know if you find this package useful, tell us about use cases, 
describe what else you would like to see integrated, etc.
For inquiries about consulting work in machine learning, natural language,
knowledge graph, and other AI applications, contact 
[Derwen, Inc.](https://derwen.ai/contact)


## Links

  - https://spacy.io/universe/project/spacy-pytextrank
  - https://pypi.org/project/pytextrank/


## Testing

To run the unit tests:

```
coverage run -m unittest discover
```

To generate a coverage report and upload it to the `codecov.io`
reporting site:

```
coverage report
bash <(curl -s https://codecov.io/bash) -t @.cc_token
```

Test coverage reports can be viewed at
<https://codecov.io/gh/DerwenAI/pytextrank>


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


## TODOs

  - fix Sphinx errors, generate docs
  - build a conda package
  - include more unit tests
  - show examples of `spacy-wordnet` to enrich the lemma graph
  - leverage `neuralcoref` to enrich the lemma graph
  - generate a phrase graph, with entity linking to DBpedia, etc.


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
[@JasonZhangzy1757](https://github.com/JasonZhangzy1757), 
[@jake-aft](https://github.com/jake-aft),
[@junchen1992](https://github.com/junchen1992),
[@Ankush-Chander](https://github.com/Ankush-Chander),
encouragement from the wonderful folks at [spaCy](https://github.com/explosion/spaCy),
plus general support from [Derwen, Inc.](https://derwen.ai/)

[![thx noam](https://github.com/DerwenAI/pytextrank/blob/master/docs/noam.jpg)](https://memegenerator.net/img/instances/66942896.jpg)
