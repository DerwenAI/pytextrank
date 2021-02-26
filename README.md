# PyTextRank

[![DOI](https://zenodo.org/badge/69814684.svg)](https://zenodo.org/badge/latestdoi/69814684)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/DerwenAI/pytextrank?style=plastic)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

**PyTextRank** is a Python implementation of *TextRank* as a
[spaCy pipeline extension](https://spacy.io/universe/project/spacy-pytextrank),
for graph-based natural language work (with related knowledge graph
practices) which gets used to:

  - extract the top-ranked phrases from a text document
  - run low-cost extractive summarization of a text document
  - help infer links from unstructured text into more structured representation

Documentation: <https://derwen.ai/docs/ptr/>


## Getting Started

See the ["Getting Started"](https://derwen.ai/docs/ptr/start/)
section of the online documentation.

To install from [PyPi](https://pypi.python.org/pypi/pytextrank):
```
pip install pytextrank
python -m spacy download en_core_web_sm
```

If you work directly from this Git repo, be sure to install the
dependencies as well:
```
pip install -r requirements.txt
```

Then to use the library with a simple use case:
```
import spacy
import pytextrank

# example text
text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types."

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank", last=True)
doc = nlp(text)

# examine the top-ranked phrases in the document
for p in doc._.phrases:
    print("{:.4f} {:5d}  {}".format(p.rank, p.count, p.text))
    print(p.chunks)
```

See the **tutorial notebooks** in the `examples` subdirectory for
sample code and patterns to use in integrating **pytextrank** with
related libraries in Python:
<https://derwen.ai/docs/ptr/tutorial/>


## Semantic Versioning

Generally speaking the major release number of **pytextrank** will
track with the major release number of the associated `spaCy` version.

We try to minimize any breaking changes between releases and provide
careful notes in the `changelog.txt` file.


## Build Instructions

**Note: most use cases won't need to build this package locally.**
Instead, simply install from
[PyPi](https://pypi.python.org/pypi/pytextrank)
or [Conda](https://docs.conda.io/).

To set up the build environment locally, see the 
["Build Instructions"](https://derwen.ai/docs/ptr/build/)
section of the online documentation.

[![thanks noam](https://github.com/DerwenAI/pytextrank/blob/master/docs/assets/noam.jpg)](https://memegenerator.net/img/instances/66942896.jpg)


## License and Copyright

Source code for **PyTextRank** plus its logo, documentation, and examples
have an [MIT license](https://spdx.org/licenses/MIT.html) which is
succinct and simplifies use in commercial applications.

All materials herein are Copyright &copy; 2016-2021 Derwen, Inc.


## Attribution

Please use the following BibTeX entry for citing **PyTextRank** if you 
use it in your research or software.
Citations are helpful for the continued development and maintenance of
this library.

```
@software{PyTextRank,
  author = {Paco Nathan},
  title = {{PyTextRank, a Python implementation of TextRank for phrase extraction and summarization of text documents}},
  year = 2016,
  publisher = {Derwen},
  doi = {10.5281/zenodo.4540784},
  url = {https://github.com/DerwenAI/pytextrank}
}
```

**DOI:** <https://doi.org/10.5281/zenodo.4540784>


## Kudos

Many thanks to our contributors:
[@louisguitton](https://github.com/louisguitton),
[@Lord-V15](https://github.com/Lord-V15),
[@anna-droid-beep](https://github.com/anna-droid-beep),
[@kavorite](https://github.com/kavorite),
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
[@shyamcody](https://github.com/shyamcody),
[@chikubee](https://github.com/chikubee),
outstanding NLP research work led by [@mihalcea](https://github.com/mihalcea),
encouragement from the wonderful folks at Explosion who develop [spaCy](https://github.com/explosion/spaCy),
plus general support from [Derwen, Inc.](https://derwen.ai/)
