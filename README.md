# Python impl for TextRank

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

## To Be Evaluated

http://stackoverflow.com/questions/9136539/how-do-weighted-edges-affect-pagerank-in-networkx
https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html

https://github.com/ashkonf/PageRank
