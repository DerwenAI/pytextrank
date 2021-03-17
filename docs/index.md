# PyTextRank

<img src="assets/logo.png" width="113" alt="I did not have semantic relations with that corpus"/>

The **PyTextRank** package is a Python implementation of *TextRank* as a
[spaCy pipeline extension](https://spacy.io/universe/project/spacy-pytextrank),
for graph-based natural language work (with related *knowledge graph*
practices) which gets used to:

  - *phrase extraction*: extract the top-ranked phrases from a text document
  - *extractive summarization*: run a simple, low-cost summarization of a text document
  - *entity linking*: help infer links from unstructured text into more structured representation

The entity linking aspects here are a *work-in-progress*, based on
[`kglab`](https://github.com/DerwenAI/kglab).


## Cut to the Chase

  1. To get started right away, jump to [*Getting Started*](start/)
  1. For a hands-on coding tour through **pytextrank**, see the [*Tutorial*](tutorial/) notebooks
  1. Check the source code at <https://github.com/DerwenAI/pytextrank>


## Motivations

The *TextRank* algorithm implementation here is based on research
published in
[[mihalcea04textrank]](biblio/#mihalcea04textrank),
plus subsequent research by
[[florescuc17]](biblio/#florescuc17)
and
[[kazemi2011corr]](biblio/#kazemi2011corr).
See the current *textgraph* research at <https://lit.eecs.umich.edu/textgraphs/>
in general for more details.

Some modifications in **PyTextRank** attempt to improve on the
original algorithm description:

  - fixed a bug: see [Java impl, 2008](https://github.com/ceteri/textrank)
  - use *lemmatization* in place of stemming
  - leverage preprocessing via *noun chunking* and *named entity recognition*
  - integration with `spaCy` as a pipeline component factory
  - simple *extractive summarization* based on vector distance from ranked phrases
  - optionally, include verbs in the graph (although not in the resulting ranked phrases)

Use of *graph algorithms* in natural language work -- notably,
[*eigenvector centrality*](https://demonstrations.wolfram.com/NetworkCentralityUsingEigenvectors/)
-- help provides a more flexible and robust basis for integrating
additional AI techniques.
While there have been many amazing innovations since late 2017 
in the application of *deep learning* for
[*language models*](http://nlpprogress.com/english/language_modeling.html),
these *transformer* models tend to imply trade-offs:

  * emphasis on predictive power for recognizing sequences
  * models which require substantial resources to train, deploy, etc.
  * relatively opaque models
  * large carbon footprint
  * disjoint from leveraging domain expertise

Our experience with *textgraphs* is this category of algorithms
provides computationally efficient methods that do not require
substantial training in advance, which can import and leverage 
domain expertise.
Moreover, this approach can be integrated with embedding methods
(deep learning) for complementary solutions.


## Community Resources

Links for other open source community resources:

  * [Issue Tracker](https://github.com/DerwenAI/pytextrank/issues)
  * [Project Board](https://github.com/DerwenAI/pytextrank/projects/1)
  * [Milestones](https://github.com/DerwenAI/pytextrank/milestones)
  * [spaCy uniVerse](https://spacy.io/universe/project/spacy-pytextrank)

Other good ways to help troubleshoot issues:

  - search [related discussions on StackOverflow](https://stackoverflow.com/search?q=pytextrank)
  - tweet to `#textrank` on [Twitter](https://twitter.com/search?q=%23textrank) (cc `@pacoid`)

The [Knowledge Graph Conference](glossary/#knowledge-graph-conference)
hosts several community resources where you can post questions and 
get help about **pytextrank** and related
[KG](glossary/#kg)
topics.

  * [community Slack](https://knowledgegraphconf.slack.com/ssb/redirect) – specifically on the `#ask` channel
  * [*Graph-Based Data Science*](https://www.linkedin.com/groups/6725785/) group on LinkedIn – join to receive related updates, news, conference coupons, etc.

[KGC](glossary/#knowledge-graph-conference)
also hosts 
["knowledge espresso"](https://www.notion.so/KG-Community-Events-Calendar-8aacbe22efa94d9b8b39b7288e22c2d3)
(monthly office hours) with [Paco Nathan](ack/#project-lead) 
and others involved in this open source project.

For related course materials and training, please check for calendar
updates in the article
["Natural Language Processing in Python"](https://medium.com/derwen/natural-language-processing-in-python-832b0a99791b).
