# Reference: `pytextrank` package
## [`BaseTextRankFactory` class](#BaseTextRankFactory)

A factory class that provides the document with its instance of
`BaseTextRank`
    
---
#### [`__init__` method](#pytextrank.BaseTextRankFactory.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L123)

```python
__init__(edge_weight=1.0, pos_kept=None, token_lookback=3, scrubber=None, stopwords=None)
```
Constructor for a factory used to instantiate the PyTextRank pipeline components.

  * `edge_weight` : `float`  
default weight for an edge

  * `pos_kept` : `typing.List[str]`  
parts of speech tags to be kept; adjust this if strings representing the POS tags change

  * `token_lookback` : `int`  
the window for neighboring tokens – similar to a *skip gram*

  * `scrubber` : `typing.Union[typing.Callable, NoneType]`  
optional "scrubber" function to clean up punctuation from a token; if `None` then defaults to `pytextrank.default_scrubber`

  * `stopwords` : `typing.Union[str, pathlib.Path, typing.Dict[str, typing.List[str]], NoneType]`  
optional dictionary of `lemma: [pos]` items to define the *stop words*, where each item has a key as a lemmatized token and a value as a list of POS tags; may be a file name (string) or a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html) for a JSON file; otherwise throws a `TypeError` exception



---
#### [`__call__` method](#pytextrank.BaseTextRankFactory.__call__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L207)

```python
__call__(doc)
```
Set the extension attributes on a `spaCy` [`Doc`](https://spacy.io/api/doc)
document to create a *pipeline component* for `TextRank` as
a stateful component, invoked when the document gets processed.

See: <https://spacy.io/usage/processing-pipelines#pipelines>

  * `doc` : `spacy.tokens.doc.Doc`  
a document container, providing the annotations produced by earlier stages of the `spaCy` pipeline



## [`BaseTextRank` class](#BaseTextRank)

Implements the *TextRank* algorithm defined by
[[mihalcea04textrank]](https://derwen.ai/docs/ptr/biblio/#mihalcea04textrank),
deployed as a `spaCy` pipeline component.

This class does not get called directly; instantiate its factory
instead.
    
---
#### [`__init__` method](#pytextrank.BaseTextRank.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L247)

```python
__init__(doc, edge_weight, pos_kept, token_lookback, scrubber, stopwords)
```
Constructor for a `TextRank` object.

  * `doc` : `spacy.tokens.doc.Doc`  
a document container, providing the annotations produced by earlier stages of the `spaCy` pipeline

  * `edge_weight` : `float`  
default weight for an edge

  * `pos_kept` : `typing.List[str]`  
parts of speech tags to be kept; adjust this if strings representing the POS tags change

  * `token_lookback` : `int`  
the window for neighboring tokens – similar to a *skip gram*

  * `scrubber` : `typing.Callable`  
optional "scrubber" function to clean up punctuation from a token

  * `stopwords` : `typing.Dict[str, typing.List[str]]`  
optional dictionary of `lemma: [pos]` items to define the *stop words*, where each item has a key as a lemmatized token and a value as a list of POS tags



---
#### [`reset` method](#pytextrank.BaseTextRank.reset)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L293)

```python
reset()
```
Reinitialize the data structures needed for extracting phrases,
removing any pre-existing state.



---
#### [`calc_textrank` method](#pytextrank.BaseTextRank.calc_textrank)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L307)

```python
calc_textrank()
```
Iterate through each sentence in the doc, constructing a
[*lemma graph*](https://derwen.ai/docs/ptr/glossary/#lemma-graph)
then returning the top-ranked phrases.

This method represents the heart of the *TextRank* algorithm.

  * *returns* : `typing.List[pytextrank.base.Phrase]`  
list of ranked phrases, in descending order



---
#### [`get_personalization` method](#pytextrank.BaseTextRank.get_personalization)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L352)

```python
get_personalization()
```
Get the *node weights* for initializing the use of the
[*Personalized PageRank*](https://derwen.ai/docs/ptr/glossary/#personalized-pagerank)
algorithm.

Defaults to a no-op for the base *TextRank* algorithm.

  * *returns* : `typing.Union[typing.Dict[pytextrank.base.Lemma, float], NoneType]`  
`None`



---
#### [`get_unit_vector` method](#pytextrank.BaseTextRank.get_unit_vector)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L592)

```python
get_unit_vector(limit_phrases)
```
Construct a *unit vector* representing the top-ranked phrases in a
`spaCy` [`Doc`](https://spacy.io/api/doc) document.
This provides a *characteristic* for comparing each sentence to the
entire document.
Taking the ranked phrases in descending order, the unit vector is a
normalized list of their calculated ranks, up to the specified limit.

  * `limit_phrases` : `int`  
maximum number of top-ranked phrases to use in the *unit vector*

  * *returns* : `typing.List[pytextrank.base.VectorElem]`  
the unit vector, as a list of `VectorElem` objects



---
#### [`calc_sent_dist` method](#pytextrank.BaseTextRank.calc_sent_dist)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L636)

```python
calc_sent_dist(limit_phrases)
```
For each sentence in the document, calculate its distance from a *unit
vector* of top-ranked phrases.

  * `limit_phrases` : `int`  
maximum number of top-ranked phrases to use in the *unit vector*

  * *returns* : `typing.List[pytextrank.base.Sentence]`  
a list of sentence distance measures



---
#### [`summary` method](#pytextrank.BaseTextRank.summary)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L685)

```python
summary(limit_phrases=10, limit_sentences=4, preserve_order=False)
```
Run an
[*extractive summarization*](https://derwen.ai/docs/ptr/glossary/#extractive-summarization),
based on the vector distance (per sentence) for each of the top-ranked phrases.

  * `limit_phrases` : `int`  
maximum number of top-ranked phrases to use in the distance vectors

  * `limit_sentences` : `int`  
total number of sentences to yield for the extractive summarization

  * `preserve_order` : `bool`  
flag to preserve the order of sentences as they originally occurred in the source text; defaults to `False`

  * *yields* :  
texts for sentences, in order



---
#### [`write_dot` method](#pytextrank.BaseTextRank.write_dot)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L732)

```python
write_dot(path="graph.dot")
```
Serialize the lemma graph in the `Dot` file format.

  * `path` : `typing.Union[str, pathlib.Path, NoneType]`  
path for the output file; defaults to `"graph.dot"`



## [`PositionRankFactory` class](#PositionRankFactory)

A factory class that provides the document with its instance of
`PositionRank`
    
---
#### [`__call__` method](#pytextrank.PositionRankFactory.__call__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/positionrank.py#L19)

```python
__call__(doc)
```
Set the extension attributes on a `spaCy` [`Doc`](https://spacy.io/api/doc)
document to create a *pipeline component* for `PositionRank` as
a stateful component, invoked when the document gets processed.

See: <https://spacy.io/usage/processing-pipelines#pipelines>

  * `doc` : `spacy.tokens.doc.Doc`  
a document container, providing the annotations produced by earlier stages of the `spaCy` pipeline



## [`PositionRank` class](#PositionRank)

Implements the *PositionRank* algorithm described by
[[florescuc17]](https://derwen.ai/docs/ptr/biblio/#florescuc17),
deployed as a `spaCy` pipeline component.

This class does not get called directly; instantiate its factory
instead.
    
---
#### [`get_personalization` method](#pytextrank.PositionRank.get_personalization)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/positionrank.py#L59)

```python
get_personalization()
```
Get the *node weights* for initializing the use of the
[*Personalized PageRank*](https://derwen.ai/docs/ptr/glossary/#personalized-pagerank)
algorithm.

From the cited reference:

> Specifically, we propose to assign a higher probability to a word
> found on the 2nd position as compared with a word found on the 50th
> position in the same document. The weight of each candidate word is
> equal to its inverse position in the document.  If the same word
> appears multiple times in the target document, then we sum all its
> position weights.

> For example, a word v_i occurring in the following positions: 2nd,
> 5th and 10th, has a weight p(v_i) = 1/2 + 1/5 + 1/10 = 4/5 = 0.8
> The weights of words are normalized before they are used in the
> position-biased PageRank.

  * *returns* : `typing.Union[typing.Dict[pytextrank.base.Lemma, float], NoneType]`  
Biased restart probabilities to use in the *PageRank* algorithm.



## [`Lemma` class](#Lemma)

A data class representing one node in the *lemma graph*.
    
---
#### [`__setattr__` method](#pytextrank.Lemma.__setattr__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main<string>#L2)

```python
__setattr__(name, value)
```

---
#### [`label` method](#pytextrank.Lemma.label)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L37)

```python
label()
```
Generates a more simplified string representation than `repr()`
provides.

  * *returns* : `str`  
string representation



---
#### [`__repr__` method](#pytextrank.Lemma.__repr__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/dataclasses.py#L350)

```python
__repr__()
```

## [`Phrase` class](#Phrase)

A data class representing one ranked phrase.
    
---
#### [`__init__` method](#pytextrank.Phrase.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main<string>#L2)

```python
__init__(text, chunks, count, rank)
```

---
#### [`__repr__` method](#pytextrank.Phrase.__repr__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/dataclasses.py#L350)

```python
__repr__()
```

## [`Sentence` class](#Sentence)

A data class representing the distance measure for one sentence.
    
---
#### [`__init__` method](#pytextrank.Sentence.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main<string>#L2)

```python
__init__(start, end, sent_id, phrases, distance)
```

---
#### [`empty` method](#pytextrank.Sentence.empty)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L73)

```python
empty()
```
Test whether this sentence includes any ranked phrases.

  * *returns* : `bool`  
`True` if the `phrases` is not empty.



---
#### [`text` method](#pytextrank.Sentence.text)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L85)

```python
text(doc)
```
Accessor for the text slice of the `spaCy` [`Doc`](https://spacy.io/api/doc)
document represented by this sentence.

  * `doc` : `spacy.tokens.doc.Doc`  
source document

  * *returns* : `str`  
the sentence text



---
#### [`__repr__` method](#pytextrank.Sentence.__repr__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/dataclasses.py#L350)

```python
__repr__()
```

## [`VectorElem` class](#VectorElem)

A data class representing one element in the *unit vector* of the document.
    
---
#### [`__init__` method](#pytextrank.VectorElem.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main<string>#L2)

```python
__init__(phrase, phrase_id, coord)
```

---
#### [`__repr__` method](#pytextrank.VectorElem.__repr__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/dataclasses.py#L350)

```python
__repr__()
```

---
## [module functions](#pytextrank)
---
#### [`default_scrubber` function](#pytextrank.default_scrubber)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/util.py#L46)

```python
default_scrubber(text)
```
Removes spurious punctuation from the given text.
Note: this is intended for documents in English.

  * `text` : `str`  
input text

  * *returns* : `str`  
scrubbed text



---
#### [`filter_quotes` function](#pytextrank.filter_quotes)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/util.py#L126)

```python
filter_quotes(text, is_email=True)
```
Filter the quoted text out of an email message.
This handles quoting methods for popular email systems.

  * `text` : `str`  
raw text data

  * `is_email` : `bool`  
flag for whether the text comes from an email message;

  * *returns* : `typing.List[str]`  
the filtered text representing as a list of lines



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
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/util.py#L62)

```python
maniacal_scrubber(text)
```
Applies multiple approaches for aggressively removing garbled Unicode
and spurious punctuation from the given text.

OH: "It scrubs the garble from its stream... or it gets the debugger again!"

  * `text` : `str`  
input text

  * *returns* : `str`  
scrubbed text



---
#### [`split_grafs` function](#pytextrank.split_grafs)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/util.py#L98)

```python
split_grafs(lines)
```
Segments a raw text, given as a list of lines, into paragraphs.

  * `lines` : `typing.List[str]`  
the raw text document, split into a lists of lines

  * *yields* :  
text per paragraph



---
## [module types](#pytextrank)
#### [`StopWordsLike` type](#pytextrank.StopWordsLike)
```python
StopWordsLike = typing.Union[str, pathlib.Path, typing.Dict[str, typing.List[str]]]
```

