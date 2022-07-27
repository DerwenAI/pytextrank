# PyTextRank changelog

## 3.2.4

2022-07-27

  * better support for "ru" and other languages without `noun_chunks` support in spaCy
  * updated example notebook to illustrate `TopicRank` algorithm
  * made the node bias setting case-independent for `Biased Textrank` algorithm; kudos @Ankush-Chander
  * updated summarization tests; kudos @tomaarsen
  * reworked some unit tests to be less brittle, less dependent on specific spaCy point releases


## 3.2.3

2022-03-06

  * handles missing `noun_chunks` in some language models (e.g., "ru")
  * add *TopicRank* algorithm; kudos @tomaarsen
  * improved test suite; fixed tests for newer spaCy releases; kudos @tomaarsen


## 3.2.2

2021-10-09

  * adjust for changes in `NetworkX` where they are removing `SciPy` as a dependency; kudos @clabornd, @tomaarsen, @duarteocarmo
  * more scrubber examples; kudos @dayalstrub-cma


## 3.2.1

2021-07-24

  * add "paragraph" option into `summary()` function; kudos @CaptXiong


## 3.2.0

2021-07-17

  * **NB: THIS SCRUBBER UPDATE WILL BREAK PREVIOUS RELEASES**
  * allow `Span` as scrubber argument, to align with `spaCy` 3.1.x; kudos @Ankush-Chander
  * add `lgtm` code reviews (slow, not integrating into GitHub PRs directly)
  * evaluating `grayskull` to generate a conda-forge recipe
  * add use of `pipdeptree` to analyze dependencies
  * use KG from `biblio.ttl` to generate bibliography
  * fixed overlooked comment from earlier code; kudos @debraj135
  * add visualisation using `altair`; kudos @louisguitton
  * add scrubber usage in sample notebook; kudos @Ankush-Chander
  * integrating use of `MkRefs` to generate semantic reference pages in `docs`


## 3.1.1

2021-03-25

  * fix the span length calculation in explanation notebook; kudos @Ankush-Chander
  * add `BiasedTextRank` by @Ankush-Chander (many thanks!)
  * add conda `environment.yml` plus instructions
  * use `bandit` to check for security issues
  * use `codespell` to check for spelling errors
  * add `pre-commit` checks in general
  * update `doc._.phrases` in the call to `change_focus()` so the summarization will sync with the latest focus


## 3.1.0

2021-03-12

  * rename `master` branch to `main`
  * add a factory class that assigns each doc its own Textrank object; kudos @Ankush-Chander
  * refactor the stopwords feature as a constructor argument
  * add `get_unit_vector()` method to expose the characteristic *unit vector*
  * add `calc_sent_dist()` method to expose the sentence distance measures (for summarization)
  * include a unit test for summarization
  * updated contributor instructions
  * `pylint` coverage for code checking
  * linking definitions and citations in source code apidocs to our online docs
  * updated links on PyPi


## 3.0.1

2021-02-27

  * `mypy` coverage for type annotations
  * add DOI to README and CITATION
  * now deploying online docs at <https://derwen.ai/docs/ptr/>


## 3.0.0

2021-02-14

  * **THIS WILL BREAK THINGS!!!**
  * support for `spaCy` 3.0.x; kudos @Lord-V15
  * full integration of `PositionRank`
  * migrated all unit tests to `pytest`
  * removed use of `logger` for debugging, introducing `icecream` instead


## 2.1.0

2021-01-31

  * add `PositionRank` by @louisguitton (many thanks!)
  * fixes chunk in `explain_summ.ipynb` by @anna-droid-beep
  * add option `preserve_order` in TextRank.summary by @kavorite
  * tested with `spaCy` 2.3.5


## 2.0.3

2020-09-15

  * try-catch `ZeroDivisionError` in summary method -- kudos @shyamcody
  * tested with updated dependencies: `spaCy` 2.3.x and `NetworkX` 2.5


## 2.0.2

2020-05-20

  * fixed default value of `._.phrases` to allow for disabling PTR in a pipeline


## 2.0.1

2020-03-02

  * fix `KeyError` issue for pre Python 3.6
  * integrated `codecov.io`
  * added PyTextRank to the spaCy uniVerse
  * fixed README.md instructions to download `en_core_web_sm`


## 2.0.0

2019-11-05

  * refactored library to run as a `spaCy` extension
  * supports multiple languages
  * significantly faster, with less memory required
  * better extraction of top-ranked phrases
  * changed license to MIT
  * uses lemma-based stopwords for more precise control
  * WIP toward integration with knowledge graph use cases


## 1.2.1

2019-11-01

  * fixed error in installation instructions


## 1.2.0

2019-11-01

  * updated to fix for current versions of `spaCy` and `NetworkX` -- kudos @dimmu
  * removed deprecated argument -- kudos @laxatives


## 1.1.1

2017-09-15

  * patch disables use of NER in `spaCy` until an intermittent bug is resolved.
  * will probably replace named tuples with `spaCy` spans instead.


## 1.1.0

2017-06-07

  * replaced use of `TextBlob` with `spaCy`
  * updated other Py dependencies
  * better handling for UTF-8


## 1.0.1

2017-04-30

  * updated Jupyter notebook example -- kudos @kjam
  * better install/import for `aptagger`
  * comparing `spaCy` performance with `TextBlob`
