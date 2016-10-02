# Python impl for TextRank

A pure Python implementation of *TextRank*, 
based on the [Mihalcea 2004](http://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf) paper.

Modifications to the original algorithm include:

  * fixed bug; see [Java impl, 2008](https://github.com/ceteri/textrank)
  * use of lemmatization instead of stemming
  * verbs included in the graph (but not in the resulting keyphrases)
  * normalized keyphrase ranks for summarization


## Installation Notes

    conda config --add channels https://conda.binstar.org/sloria
    conda install textblob
    sudo python -m nltk.downloader punkt
    sudo python -m nltk.downloader wordnet


## Example Usage

Run a test case based on the Mihalcea paper:

    ./stage1.py dat/mihalcea.json > out.json
    ./stage2.py out.json

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
