# Overview

## Lemma Graph

Internally, **PyTextRank** constructs a *lemma graph* to represent
links among the candidate phrases (e.g., unrecognized entities) and
also references within supporting language within the text.


The results from components in earlier stages of the `spaCy` pipeline
produce two important kinds of annotations for each token in a parsed
document:

  1. *part-of-speech*
  2. *lemmatized*

Note that when you have these two annotation plus the disambiguated
*word sense* (i.e., the meaning of a word based on its context and
usage) then you can map from a token to a *concept*.

The gist of the *TextRank* algorithm is to apply a sliding window
across the tokens within a parsed sentence, constructing a graph from
the lemmatized tokens where neighbor within the window get linked.
Each lemma is unique within the lemma graph, such that repeated
instances collect more links.

A *centrality* measure gets calculated for each node in the graph,
then the nouns can be ranked in descending order.

An additional pass through the graph uses both *noun chunks* and
*named entities* to help agglomerate adjacent nouns into ranked
phrases.


## Leveraging Semantic Relations

Generally speaking, any means of enriching the lemma graph prior to
phrase ranking will tend to improve results.

Possible ways to enrich the lemma graph include
[*coreference resolution*](http://nlpprogress.com/english/coreference_resolution.html)
and
[*semantic relations*](https://en.wikipedia.org/wiki/Hyponymy_and_hypernymy).
The latter can leverage *knowledge graphs* or some form of *thesaurus*
in the general case.

For example,
[WordNet](https://spacy.io/universe/project/spacy-wordnet)
and
[DBpedia](https://wiki.dbpedia.org/)
both provide means for inferring links among entities, and
purpose-built knowledge graphs can be applied for specific use cases.
These can help enrich a lemma graph even in cases where links are not
explicit within the text.

Consider a paragraph that mentions `cats` and `kittens` in different
sentences: an implied semantic relation exists between the two nouns
since the lemma `kitten` is a hyponym of the lemma `cat` -- such that
an inferred link can be added between them.


## Entity Linking

One of the motivations for **PyTextRank** is to provide support (eventually) for
[*entity linking*](http://nlpprogress.com/english/entity_linking.html),
in contrast to the more commonplace usage of
[*named entity recognition*](http://nlpprogress.com/english/named_entity_recognition.html).
These approaches can be used together in complementary ways to improve
the results overall.

This has an additional benefit of linking parsed and annotated
documents into more structured data, and can also be used to support
knowledge graph construction.


## Extractive Summarization

The simple implementation of 
[*extractive summarization*](../glossary/#extractive-summarization)
**PyTextRank** was inspired by the
[[williams2016]](../biblio/#williams2016),
talk on text summarization.

Note that **much better** approaches exist for
[*summarizing text*](http://nlpprogress.com/english/summarization.html).
For instance, see <https://primer.ai> for a commercial example
using state of the art 
[*abstractive summarization*](../glossary/#abstractive-summarization)
based on a combination of
[*deep learning*](../glossary/#deep-learning)
and
[*knowledge graph*](https://derwen.ai/docs/kgl/glossary/#knowledge-graph)
approaches.

Even so, there are engineering and policy trade-offs[^1] to consider.
Arguably, lower-cost alternatives such as **PyTextRank** allow for a
wider range of trade-offs to suit your use cases.
[^1]: Both <https://arxiv.org/abs/1909.03004> and <https://arxiv.org/abs/1906.02243> explore these issues in detail.


## Feedback

Let us know if you find this package useful, tell us about use cases, 
describe what else you would like to see integrated, etc.

We're focused on our [community](../#community-resources) 
and pay special attention to the business use cases.
We're also eager to hear your feedback and suggestions for this 
open source project.
