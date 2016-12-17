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

  * [TextBlob](http://textblob.readthedocs.io/)
  * [spaCy](https://spacy.io/docs/usage/)
  * [NetworkX](http://networkx.readthedocs.io/)
  * [datasketch](https://github.com/ekzhu/datasketch)
  * [graphviz](https://pypi.python.org/pypi/graphviz)

To install:

    pip install textblob
    pip install -U git+https://github.com/sloria/textblob-aptagger.git@dev
    python -m nltk.downloader punkt
    python -m nltk.downloader wordnet
    python -m textblob.download_corpora
    pip install -U spacy
    python -m spacy.en.download all
    pip install networkx
    pip install statistics
    pip install datasketch -U
    pip install graphviz

NB: the runtime depends on a local file called `stop.txt` which contains a list of *stopwords*.


## Example Usage

Run a test case based on the Mihalcea paper:

    ./stage1.py dat/mih.json > out1.json
    ./stage2.py out1.json > out2.json


```
0.1286	types systems
0.0922	mixed types
0.0711	minimal set
0.0643	systems
0.0546	strict inequations
0.0474	considered
0.0461	types
0.0368	natural numbers
0.0355	minimal supporting set
0.0355	set
0.0351	solutions
0.0321	linear diophantine equations
0.0291	linear constraints
0.0286	solving
0.0275	corresponding algorithms
```

NB: results for this implementation are intended more to be used as *feature vectors*, 
not as academic paper summaries.


Run another test based on [Williams](http://mike.place/2016/summarization/), using text from a
*[Wired](https://www.wired.com/2016/03/googles-ai-wins-pivotal-game-two-match-go-grandmaster/)*
article:

    ./stage1.py dat/lee.json > out1.json
    ./stage2.py out1.json > out2.json
    ./stage3.py out1.json out2.json > out3.json
    ./stage4.py out2.json out3.json > out4.md

Which produces as a summary:

> **excerpts:** The surprisingly skillful Google machine, known as AlphaGo, now needs only one more win to claim victory in the match. The Korean-born Lee Sedol will go down in defeat unless he takes each of the match's last three games. Game Three is set for Saturday afternoon inside Seoul's Four Seasons hotel. Lee Sedol is widely-regarded as the top Go player of the last decade, after winning more international titles than all but one other player. Although AlphaGo topped Lee Sedol in the match's first game on Wednesday afternoon, the outcome of Game Two was no easier to predict. In his 1996 match with IBM's Deep Blue supercomputer, world chess champion Gary Kasparov lost the first game but then came back to win the second game and, eventually, the match as a whole. 

> **keywords:** first game, google ai lab, all-important match, lee sedol, more win, alphago, wednesday, seoul, seasons hotel, world chess champion gary kasparov, afternoon, game, second game


These results show a summarization similar to slide 30 of the talk; 
however, this approach is more amenable to:

  * bootstrapping work with new documents about a specific topic
  * producing results ready for use in a search engine or recommender system

## NB: Unicode

Note the `force_encode` flags on some of the function calls.
This forces `utf-8` encoding, in case the input has characters that couldn't be handled otherwise.
That may require some post-processing for your use cases -- 
see examples functions in the `stage4.py` code.
This is **turned off** by default.

## TODO: Stay tuned for more...

  1. Docker container for managing the installation/dependencies

## Kudos

[@htmartin](https://github.com/htmartin)
[@williamsmj](https://github.com/williamsmj/)
[@mattkohl](https://github.com/mattkohl)
[@HarshGrandeur](https://github.com/HarshGrandeur)
[@mnowotka](https://github.com/mnowotka)
