# Python impl for TextRank

A pure Python implementation of *TextRank*, 
based on the [Mihalcea 2004](http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf) paper.
This work leads toward integration with the [Williams 2016](http://mike.place/2016/summarization/)
talk on *text summarization*.

Modifications to the original Mihalcea algorithm include:

  * fixed bug; see [Java impl, 2008](https://github.com/ceteri/textrank)
  * use of lemmatization instead of stemming
  * verbs included in the graph (but not in the resulting keyphrases)
  * normalized keyphrase ranks used in summarization


## Dependencies and Installation

This code has dependencies on several other Python projects:

  * [NLTK](http://www.nltk.org/)
  * [TextBlob](http://textblob.readthedocs.io/)
  * [NetworkX](http://networkx.readthedocs.io/)
  * [datasketch](https://github.com/ekzhu/datasketch)

To install:

    conda config --add channels https://conda.binstar.org/sloria
    conda install textblob
    pip install -U git+https://github.com/sloria/textblob-aptagger.git@dev
    sudo python -m nltk.downloader punkt
    sudo python -m nltk.downloader wordnet
    pip install datasketch -U


## Example Usage

Run a test case based on the Mihalcea paper:

    ./stage1.py dat/mih.json > out1.json
    ./stage2.py out1.json > out2.json

That test case should result as:

```
0.2230	  minimal supporting set
0.1345	  types systems
0.1339	  linear diophantine equations
0.0802	  mixed types
0.0541	  strict inequations
0.0505	  nonstrict inequations
0.0368	  linear constraints
0.0356	  natural numbers
0.0252	  corresponding algorithms
0.0116	  upper bounds
0.0091	  solutions
0.0027	  components
0.0025	  construction
0.0014	  compatibility
0.0010	  criteria
```

Run another test based on [Williams](http://mike.place/2016/summarization/), using text from a
*[Wired](https://www.wired.com/2016/03/googles-ai-wins-pivotal-game-two-match-go-grandmaster/)*
article:

    ./stage1.py dat/ars.json > out1.json
    ./stage2.py out1.json > out2.json
    ./stage3.py out1.json out2.json > out3.json
    ./stage4.py out2.json out3.json > out4.md

Which produces as a summary:

> **excerpts:** The surprisingly skillful Google machine, known as AlphaGo, now needs only one more win to claim victory in the match. The Korean-born Lee Sedol will go down in defeat unless he takes each of the match's last three games. Lee Sedol is widely-regarded as the top Go player of the last decade, after winning more international titles than all but one other player. Although AlphaGo topped Lee Sedol in the match's first game on Wednesday afternoon, the outcome of Game Two was no easier to predict. In his 1996 match with IBM's Deep Blue supercomputer, world chess champion Gary Kasparov lost the first game but then came back to win the second game and, eventually, the match as a whole.

> **keywords:** world chess champion gary kasparov; grandmaster lee sedol; korean-born lee sedol; many other games; google ai lab; skillful google machine; historic best-of-five match; intelligent go-playing computer system; four seasons hotel; other big-name internet companies; top go player; search engine results; more international titles

These results show a summarization similar to slide 30 of the talk; 
however, this approach is more amenable to:

  * bootstrapping work with new documents about a specific topic
  * producing results ready for use in a search engine or recommender system


## Kudos

[@williamsmj](https://github.com/williamsmj/),
[@mattkohl](https://github.com/mattkohl)
