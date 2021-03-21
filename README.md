# PyTextRank

[![DOI](https://zenodo.org/badge/69814684.svg)](https://zenodo.org/badge/latestdoi/69814684)
![Licence](https://img.shields.io/github/license/DerwenAI/pytextrank)
![Repo size](https://img.shields.io/github/repo-size/DerwenAI/pytextrank)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/DerwenAI/pytextrank?style=plastic)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

**PyTextRank** is a Python implementation of *TextRank* as a
[spaCy pipeline extension](https://spacy.io/universe/project/spacy-pytextrank),
for graph-based natural language work -- and related knowledge graph practices.
This includes the [*textgraphs*](http://www.textgraphs.org/) algorithms:

  - *TextRank* by [[mihalcea04textrank]](https://derwen.ai/docs/ptr/biblio/#mihalcea04textrank)
  - *PositionRank* by [[florescuc17]](https://derwen.ai/docs/ptr/biblio/#florescuc17)
  - *Biased TextRank* by [[kazemi2011corr]](https://derwen.ai/docs/ptr/biblio/#kazemi2011corr)

Popular use cases for this library include:

  - *phrase extraction*: get the top-ranked phrases from a text document
  - low-cost *extractive summarization* of a text document
  - help infer links from unstructured text into more structured representation

See our full documentation at: <https://derwen.ai/docs/ptr/>


## Getting Started

See the ["Getting Started"](https://derwen.ai/docs/ptr/start/)
section of the online documentation.

To install from [PyPi](https://pypi.python.org/pypi/pytextrank):
```
python3 -m pip install pytextrank
python3 -m spacy download en_core_web_sm
```

If you work directly from this Git repo, be sure to install the
dependencies as well:
```
python3 -m pip install -r requirements.txt
```

Alternatively, to install dependencies using `conda`:
```
conda env create -f environment.yml
conda activate pytextrank
```

Then to use the library with a simple use case:
```python
import spacy
import pytextrank

# example text
text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types systems and systems of mixed types."

# load a spaCy model, depending on language, scale, etc.
nlp = spacy.load("en_core_web_sm")

# add PyTextRank to the spaCy pipeline
nlp.add_pipe("textrank")
doc = nlp(text)

# examine the top-ranked phrases in the document
for phrase in doc._.phrases:
    print(phrase.text)
    print(phrase.rank, phrase.count)
    print(phrase.chunks)
```

See the **tutorial notebooks** in the `examples` subdirectory for
sample code and patterns to use in integrating **PyTextTank** with
related libraries in Python:
<https://derwen.ai/docs/ptr/tutorial/>


<details>
  <summary>Contributing Code</summary>

We welcome people getting involved as contributors to this open source
project!

For detailed instructions please see:
[CONTRIBUTING.md](https://github.com/DerwenAI/pytextrank/blob/main/CONTRIBUTING.md)
</details>

<details>
  <summary>Build Instructions</summary>

<strong>
Note: unless you are contributing code and updates,
in most use cases won't need to build this package locally.
</strong>

Instead, simply install from
[PyPi](https://pypi.python.org/pypi/pytextrank)
or use [Conda](https://docs.conda.io/).

To set up the build environment locally, see the 
["Build Instructions"](https://derwen.ai/docs/ptr/build/)
section of the online documentation.
</details>

<details>
  <summary>Semantic Versioning</summary>

Generally speaking the major release number of <strong>PyTextRank</strong> 
will track with the major release number of the associated <code>spaCy</code>
version.

See:
[changelog.txt](https://github.com/DerwenAI/pytextrank/blob/main/changelog.txt)
</details>

<img
 alt="thanks noam!"
 src="https://raw.githubusercontent.com/DerwenAI/pytextrank/main/docs/assets/noam.jpg"
 width="231"
/>


## License and Copyright

Source code for **PyTextRank** plus its logo, documentation, and examples
have an [MIT license](https://spdx.org/licenses/MIT.html) which is
succinct and simplifies use in commercial applications.

All materials herein are Copyright &copy; 2016-2021 Derwen, Inc.


## Attribution

Please use the following BibTeX entry for citing **PyTextRank** if you 
use it in your research or software:
```bibtex
@software{PyTextRank,
  author = {Paco Nathan},
  title = {{PyTextRank, a Python implementation of TextRank for phrase extraction and summarization of text documents}},
  year = 2016,
  publisher = {Derwen},
  doi = {10.5281/zenodo.4602393},
  url = {https://github.com/DerwenAI/pytextrank}
}
```

Citations are helpful for the continued development and maintenance of
this library.
For example, see our citations listed on
[Google Scholar](https://scholar.google.com/scholar?q=related:5tl6J4xZlCIJ:scholar.google.com/&scioq=&hl=en&as_sdt=0,5).


## Kudos

Many thanks to our contributors:
[@louisguitton](https://github.com/louisguitton),
[@Ankush-Chander](https://github.com/Ankush-Chander),
[@Lord-V15](https://github.com/Lord-V15),
[@anna-droid-beep](https://github.com/anna-droid-beep),
[@dvsrepo](https://github.com/dvsrepo),
[@kavorite](https://github.com/kavorite),
[@htmartin](https://github.com/htmartin),
[@williamsmj](https://github.com/williamsmj/),
[@mattkohl](https://github.com/mattkohl),
[@vanita5](https://github.com/vanita5),
[@HarshGrandeur](https://github.com/HarshGrandeur),
[@mnowotka](https://github.com/mnowotka),
[@kjam](https://github.com/kjam),
[@SaiThejeshwar](https://github.com/SaiThejeshwar),
[@laxatives](https://github.com/laxatives),
[@dimmu](https://github.com/dimmu), 
[@JasonZhangzy1757](https://github.com/JasonZhangzy1757), 
[@jake-aft](https://github.com/jake-aft),
[@junchen1992](https://github.com/junchen1992),
[@shyamcody](https://github.com/shyamcody),
[@chikubee](https://github.com/chikubee),
outstanding NLP research work led by [@mihalcea](https://github.com/mihalcea),
encouragement from the wonderful folks at Explosion who develop [spaCy](https://github.com/explosion/spaCy),
plus general support from [Derwen, Inc.](https://derwen.ai/)
