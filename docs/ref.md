# Reference: `pytextrank` package
## [`BaseTextRank` class](#BaseTextRank)

Implements TextRank by Mihalcea, et al., as a spaCy pipeline component.
    
---
#### [`__init__` method](#pytextrank.BaseTextRank.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L49)

```python
__init__(edge_weight=1.0, pos_kept=['ADJ', 'NOUN', 'PROPN', 'VERB'], token_lookback=3, scrubber=None)
```
Constructor for a `TextRank` object

  * `edge_weight` : `float`  
default weight for an edge

  * `pos_kept` : `typing.List[str]`  
parts of speech tags to be kept; adjust this if strings representing

  * `token_lookback` : `int`  
the window for neighboring tokens (similar to a skip gram)

  * `scrubber` : `typing.Union[typing.Callable, NoneType]`  
optional "scrubber" function to clean up punctuation from a token; if `None` then defaults to `pytextrank.default_scrubber`



---
#### [`__call__` method](#pytextrank.BaseTextRank.__call__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L87)

```python
__call__(doc)
```
Set the extension attributes on a spaCy[`Doc`](https://spacy.io/api/doc) 
document to create a *pipeline component factory* for `TextRank` as 
a stateful component, when the document gets processed.
See: <https://spacy.io/usage/processing-pipelines#pipelines>

  * `doc` : `spacy.tokens.doc.Doc`  
the document container for accessing linguistic annotations



---
#### [`reset` method](#pytextrank.BaseTextRank.reset)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L109)

```python
reset()
```
Initialize the data structures needed for extracting phrases, removing
any pre-existing state.



---
#### [`load_stopwords` method](#pytextrank.BaseTextRank.load_stopwords)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L123)

```python
load_stopwords(data=None, path=None)
```
Load a dictionary of *stop words* for tokens to be ignored when
constructing the lemma graph.

Note: be cautious when using this feature, it can get "greedy" and
bias/distort the results.

  * `data` : `typing.Union[typing.Dict[str, typing.List[str]], NoneType]`  
dictionary of `lemma: [pos]` items to define the stop words, where

  * `path` : `typing.Union[pathlib.Path, NoneType]`  
optional [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html)



---
#### [`calc_textrank` method](#pytextrank.BaseTextRank.calc_textrank)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L155)

```python
calc_textrank()
```
Iterate through each sentence in the doc, constructing a lemma graph
then returning the top-ranked phrases.

This method represents the heart of the algorithm implementation.

  * *returns* : `typing.List[pytextrank.base.Phrase]`  
list of ranked phrases, in descending order



---
#### [`summary` method](#pytextrank.BaseTextRank.summary)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L423)

```python
summary(limit_phrases=10, limit_sentences=4, preserve_order=False)
```
Run extractive summarization, based on the vector distance (per
sentence) for each of the top-ranked phrases.

  * `limit_phrases` : `inspect._empty`  
maximum number of top-ranked phrases to use in the distance vectors

  * `limit_sentences` : `inspect._empty`  
total number of sentences to yield for the extractive summary

  * `preserve_order` : `inspect._empty`  
flag to preserve the order of sentences as they originally occurred in

  * *yields* :  
texts for sentences, in order



---
#### [`write_dot` method](#pytextrank.BaseTextRank.write_dot)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L529)

```python
write_dot(path="graph.dot")
```
Serialize the lemma graph in the `Dot` file format.

  * `path` : `inspect._empty`  
path for the output file; defaults to `"graph.dot"`



## [`PositionRank` class](#PositionRank)

Implements the PositionRank algorithm by Florescu, et al. (2017) as a
spaCy pipeline component.
    
## [`Phrase` class](#Phrase)

Represents one extracted phrase.
    
---
#### [`__init__` method](#pytextrank.Phrase.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main<string>#L2)

```python
__init__(text, rank, count, chunks)
```

---
#### [`__repr__` method](#pytextrank.Phrase.__repr__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/dataclasses.py#L350)

```python
__repr__()
```

---
## [module functions](#pytextrank)
---
#### [`default_scrubber` function](#pytextrank.default_scrubber)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/util.py#L132)

```python
default_scrubber(text)
```
remove spurious punctuation (for English)



---
#### [`filter_quotes` function](#pytextrank.filter_quotes)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/util.py#L67)

```python
filter_quotes(text, is_email=True)
```
filter the quoted text out of a message



---
#### [`groupby_apply` function](#pytextrank.groupby_apply)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/util.py#L11)

```python
groupby_apply(data, keyfunc, applyfunc)
```
GroupBy using a key function and an apply function, without a `pandas`
dependency.
See: <https://docs.python.org/3/library/itertools.html#itertools.groupby>

  * `data` : `typing.Iterable[typing.Any]`  
iterable

  * `keyfunc` : `typing.Callable`  
callable to define the key by which you want to group

  * `applyfunc` : `typing.Callable`  
callable to apply to the group

  * *returns* : `typing.List[typing.Tuple[typing.Any, typing.Any]]`  
an iterable with the accumulated values



---
#### [`maniacal_scrubber` function](#pytextrank.maniacal_scrubber)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/util.py#L106)

```python
maniacal_scrubber(text)
```
it scrubs the garble from its stream...
or it gets the debugger again



---
#### [`split_grafs` function](#pytextrank.split_grafs)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/util.py#L47)

```python
split_grafs(lines)
```
segment raw text, given as a list of lines, into paragraphs



---
## [module types](#pytextrank)
#### [`Node` type](#pytextrank.Node)
```python
Node = typing.Tuple[str, str]
```

