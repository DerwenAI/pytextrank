# Getting Started

## Installation

To install from [PyPi](https://pypi.python.org/pypi/pytextrank):
```
python3 -m pip install pytextrank
python3 -m spacy download en_core_web_sm
```

If you work directly from this Git repo, be sure to install the 
[dependencies](https://pip.pypa.io/en/stable/cli/pip_install/#requirements-file-format):
```
python3 -m pip install -r requirements.txt
```


## Sample Usage

To use **pytextrank** in its simplest form:
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


## Hands-on Coding Tutorial

See the [*Tutorial*](../tutorial/) notebooks for sample code and
patterns to use when integrating **pytextrank** with other related
libraries in Python.
