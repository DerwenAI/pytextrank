# Reference: `pytextrank` package
## [`BaseTextRank` class](#BaseTextRank)

Implements the *TextRank* algorithm defined by
[[mihalcea04textrank]](https://derwen.ai/docs/ptr/biblio/#mihalcea04textrank),
deployed as a `spaCy` pipeline component.
    
---
#### [`__init__` method](#pytextrank.BaseTextRank.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L51)

```python
__init__(edge_weight=1.0, pos_kept=None, token_lookback=3, scrubber=None)
```
Constructor for a `TextRank` object

  * `edge_weight` : `float`  
default weight for an edge

  * `pos_kept` : `typing.List[str]`  
parts of speech tags to be kept; adjust this if strings representing

  * `token_lookback` : `int`  
the window for neighboring tokens (similar to a skip gram)

  * `scrubber` : `typing.Union[typing.Callable, NoneType]`  
optional "scrubber" function to clean up punctuation from a token;



---
#### [`__call__` method](#pytextrank.BaseTextRank.__call__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L101)

```python
__call__(doc)
```
Set the extension attributes on a `spaCy` [`Doc`](https://spacy.io/api/doc)
document to create a *pipeline component factory* for `TextRank` as
a stateful component, invoked when the document gets processed.
See: <https://spacy.io/usage/processing-pipelines#pipelines>

  * `doc` : `spacy.tokens.doc.Doc`  
a document container for accessing the annotations produced by earlier



---
#### [`reset` method](#pytextrank.BaseTextRank.reset)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L124)

```python
reset()
```
Reinitialize the data structures needed for extracting phrases,
removing any pre-existing state.



---
#### [`load_stopwords` method](#pytextrank.BaseTextRank.load_stopwords)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L138)

```python
load_stopwords(data=None, path=None)
```
Load a dictionary of
[*stop words*](https://derwen.ai/docs/ptr/glossary/#stop-words)
– i.e., tokens to be ignored when constructing the
[*lemma graph*](https://derwen.ai/docs/ptr/glossary/#lemma-graph).

Note: be cautious about use of this feature, since it can get "greedy"
and bias/distort the results.

  * `data` : `typing.Union[typing.Dict[str, typing.List[str]], NoneType]`  
dictionary of `lemma: [pos]` items to define the stop words, where

  * `path` : `typing.Union[pathlib.Path, NoneType]`  
optional [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html)



---
#### [`calc_textrank` method](#pytextrank.BaseTextRank.calc_textrank)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L173)

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
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L219)

```python
get_personalization()
```
Get the *node weights* for initializing the use of the
[*Personalized PageRank*](https://derwen.ai/docs/ptr/glossary/#personalized-pagerank)
algorithm.

Defaults to a no-op for the base *TextRank* algorithm.

  * *returns* : `typing.Union[typing.Dict[typing.Tuple[str, str], float], NoneType]`  
`None`



---
#### [`calc_sent_rank` method](#pytextrank.BaseTextRank.calc_sent_rank)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L446)

```python
calc_sent_rank(limit_phrases)
```
Calculates a rank for each sentence in the document, based on its distance
(per sentence) from a *unit vector* of the top-ranked phrases.

  * `limit_phrases` : `int`  
maximum number of top-ranked phrases to use in the *unit vector*

  * *returns* : `typing.Dict[int, float]`  
a dictionary of the calculated ranks per sentence



---
#### [`summary` method](#pytextrank.BaseTextRank.summary)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L516)

```python
summary(limit_phrases=10, limit_sentences=4, preserve_order=False)
```
Run
[*extractive summarization*](https://derwen.ai/docs/ptr/glossary/#extractive-summarization),
based on a vector distance (per sentence) for each of the top-ranked phrases.

  * `limit_phrases` : `int`  
maximum number of top-ranked phrases to use in the distance vectors

  * `limit_sentences` : `int`  
total number of sentences to yield for the extractive summarization

  * `preserve_order` : `bool`  
flag to preserve the order of sentences as they originally occurred in

  * *yields* :  
texts for sentences, in order



---
#### [`write_dot` method](#pytextrank.BaseTextRank.write_dot)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/base.py#L567)

```python
write_dot(path="graph.dot")
```
Serialize the lemma graph in the `Dot` file format.

  * `path` : `str`  
path for the output file; defaults to `"graph.dot"`



## [`PositionRank` class](#PositionRank)

Implements the *PositionRank* algorithm described by
[[florescuc17]](https://derwen.ai/docs/ptr/biblio/#florescuc17),
deployed as a `spaCy` pipeline component.
    
---
#### [`get_personalization` method](#pytextrank.PositionRank.get_personalization)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/pytextrank/positionrank.py#L17)

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

  * *returns* : `typing.Union[typing.Dict[typing.Tuple[str, str], float], NoneType]`  
Biased restart probabilities to use in the *PageRank* algorithm.



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
#### [`Node` type](#pytextrank.Node)
```python
Node = typing.Tuple[str, str]
```

#### [`PhraseLike` type](#pytextrank.PhraseLike)
```python
PhraseLike = typing.List[typing.Tuple[str, typing.List[typing.Tuple[float, spacy.tokens.span.Span]]]]
```

