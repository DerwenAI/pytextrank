# Package Reference: `pytextrank`



## [`BaseTextRankFactory` class](#BaseTextRankFactory)

A factory class that provides the document with its instance of
`BaseTextRank`
    


---
#### [`__call__` method](#pytextrank.BaseTextRankFactory.__call__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L216)

```python
__call__(doc)
```

Set the extension attributes on a `spaCy` [`Doc`](https://spacy.io/api/doc)
document to create a *pipeline component* for `BaseTextRank` as
a stateful component, invoked when the document gets processed.

See: <https://spacy.io/usage/processing-pipelines#pipelines>

  * `doc` : `spacy.tokens.doc.Doc`  
a document container, providing the annotations produced by earlier stages of the `spaCy` pipeline

---
#### [`__init__` method](#pytextrank.BaseTextRankFactory.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L132)

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
optional "scrubber" function to clean up punctuation from a token; if `None` then defaults to `pytextrank.default_scrubber`; when running, PyTextRank will throw a `FutureWarning` warning if the configuration uses a deprecated approach for a scrubber function

  * `stopwords` : `typing.Union[str, pathlib.Path, typing.Dict[str, typing.List[str]], NoneType]`  
optional dictionary of `lemma: [pos]` items to define the *stop words*, where each item has a key as a lemmatized token and a value as a list of POS tags; may be a file name (string) or a [`pathlib.Path`](https://docs.python.org/3/library/pathlib.html) for a JSON file; otherwise throws a `TypeError` exception


## [`BaseTextRank` class](#BaseTextRank)

Implements the *TextRank* algorithm defined by
[[mihalcea04textrank]](https://derwen.ai/docs/ptr/biblio/#mihalcea04textrank),
deployed as a `spaCy` pipeline component.

This class does not get called directly; instantiate its factory
instead.
    


---
#### [`__init__` method](#pytextrank.BaseTextRank.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L256)

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
#### [`calc_sent_dist` method](#pytextrank.BaseTextRank.calc_sent_dist)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L671)

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
#### [`calc_textrank` method](#pytextrank.BaseTextRank.calc_textrank)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L321)

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
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L365)

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
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L627)

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
#### [`plot_keyphrases` method](#pytextrank.BaseTextRank.plot_keyphrases)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L797)

```python
plot_keyphrases()
```

Plot a document's keyphrases rank profile using
[`altair.Chart`](https://altair-viz.github.io/user_guide/generated/toplevel/altair.Chart.html)

Throws an `ImportError` if the `altair` and `pandas` libraries are not installed.

  * *returns* : `typing.Any`  
the `altair` chart being rendered

---
#### [`reset` method](#pytextrank.BaseTextRank.reset)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L307)

```python
reset()
```

Reinitialize the data structures needed for extracting phrases,
removing any pre-existing state.

---
#### [`summary` method](#pytextrank.BaseTextRank.summary)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L720)

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
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L767)

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
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/positionrank.py#L24)

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
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/positionrank.py#L64)

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


## [`BiasedTextRankFactory` class](#BiasedTextRankFactory)

A factory class that provides the document with its instance of
`BiasedTextRank`
    


---
#### [`__call__` method](#pytextrank.BiasedTextRankFactory.__call__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/biasedrank.py#L22)

```python
__call__(doc)
```

Set the extension attributes on a `spaCy` [`Doc`](https://spacy.io/api/doc)
document to create a *pipeline component* for `BiasedTextRank` as
a stateful component, invoked when the document gets processed.

See: <https://spacy.io/usage/processing-pipelines#pipelines>

  * `doc` : `spacy.tokens.doc.Doc`  
a document container, providing the annotations produced by earlier stages of the `spaCy` pipeline


## [`BiasedTextRank` class](#BiasedTextRank)

Implements the *Biased TextRank* algorithm described by
[[kazemi-etal-2020-biased]](https://derwen.ai/docs/ptr/biblio/#kazemi-etal-2020-biased),
deployed as a `spaCy` pipeline component.

This class does not get called directly; instantiate its factory
instead.
    


---
#### [`change_focus` method](#pytextrank.BiasedTextRank.change_focus)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/biasedrank.py#L122)

```python
change_focus(focus=None, bias=1.0, default_bias=1.0)
```

Re-runs the *Biased TextRank* algorithm with the given focus.
This approach allows an application to "change focus" without
re-running the entire pipeline.

  * `focus` : `str`  
optional text (string) with space-delimited tokens to use for the *focus set*; defaults to `None`

  * `bias` : `float`  
optional bias for *node weight* values on tokens found within the *focus set*; defaults to `1.0`

  * `default_bias` : `float`  
optional bias for *node weight* values on tokens not found within the *focus set*; set to `0.0` to enhance the focus, especially in the case of long documents; defaults to `1.0`

  * *returns* : `typing.List[pytextrank.base.Phrase]`  
list of ranked phrases, in descending order

---
#### [`get_personalization` method](#pytextrank.BiasedTextRank.get_personalization)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/biasedrank.py#L88)

```python
get_personalization()
```

Get the *node weights* for initializing the use of the
[*Personalized PageRank*](https://derwen.ai/docs/ptr/glossary/#personalized-pagerank)
algorithm.

  * *returns* : `typing.Union[typing.Dict[pytextrank.base.Lemma, float], NoneType]`  
biased restart probabilities to use in the *PageRank* algorithm.


## [`Lemma` class](#Lemma)

A data class representing one node in the *lemma graph*.
    


---
#### [`__delattr__` method](#pytextrank.Lemma.__delattr__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__delattr__(name)
```



---
#### [`__eq__` method](#pytextrank.Lemma.__eq__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__eq__(other)
```



---
#### [`__ge__` method](#pytextrank.Lemma.__ge__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__ge__(other)
```



---
#### [`__gt__` method](#pytextrank.Lemma.__gt__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__gt__(other)
```



---
#### [`__hash__` method](#pytextrank.Lemma.__hash__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__hash__()
```



---
#### [`__init__` method](#pytextrank.Lemma.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__init__(lemma, pos)
```



---
#### [`__le__` method](#pytextrank.Lemma.__le__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__le__(other)
```



---
#### [`__lt__` method](#pytextrank.Lemma.__lt__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__lt__(other)
```



---
#### [`__repr__` method](#pytextrank.Lemma.__repr__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/dataclasses.py#L350)

```python
__repr__()
```



---
#### [`__setattr__` method](#pytextrank.Lemma.__setattr__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__setattr__(name, value)
```



---
#### [`label` method](#pytextrank.Lemma.label)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L46)

```python
label()
```

Generates a more simplified string representation than `repr()`
provides.

  * *returns* : `str`  
string representation


## [`Phrase` class](#Phrase)

A data class representing one ranked phrase.
    


---
#### [`__eq__` method](#pytextrank.Phrase.__eq__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__eq__(other)
```



---
#### [`__init__` method](#pytextrank.Phrase.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

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
#### [`__eq__` method](#pytextrank.Sentence.__eq__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__eq__(other)
```



---
#### [`__init__` method](#pytextrank.Sentence.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__init__(start, end, sent_id, phrases, distance)
```



---
#### [`__repr__` method](#pytextrank.Sentence.__repr__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/dataclasses.py#L350)

```python
__repr__()
```



---
#### [`empty` method](#pytextrank.Sentence.empty)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L82)

```python
empty()
```

Test whether this sentence includes any ranked phrases.

  * *returns* : `bool`  
`True` if the `phrases` is not empty.

---
#### [`text` method](#pytextrank.Sentence.text)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/base.py#L94)

```python
text(doc)
```

Accessor for the text slice of the `spaCy` [`Doc`](https://spacy.io/api/doc)
document represented by this sentence.

  * `doc` : `spacy.tokens.doc.Doc`  
source document

  * *returns* : `str`  
the sentence text


## [`VectorElem` class](#VectorElem)

A data class representing one element in the *unit vector* of the document.
    


---
#### [`__eq__` method](#pytextrank.VectorElem.__eq__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

```python
__eq__(other)
```



---
#### [`__init__` method](#pytextrank.VectorElem.__init__)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main&lt;string&gt;#L2)

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
## [module functions](#pytextrank_functions)


---
#### [`default_scrubber` method](#pytextrank.default_scrubber)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/util.py#L49)

```python
default_scrubber(span)
```

Removes spurious punctuation from the given text.
Note: this is intended for documents in English.

  * `span` : `spacy.tokens.span.Span`  
input text `Span`

  * *returns* : `str`  
scrubbed text

---
#### [`filter_quotes` method](#pytextrank.filter_quotes)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/util.py#L128)

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
#### [`groupby_apply` method](#pytextrank.groupby_apply)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/util.py#L14)

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
#### [`maniacal_scrubber` method](#pytextrank.maniacal_scrubber)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/util.py#L65)

```python
maniacal_scrubber(span)
```

Applies multiple approaches for aggressively removing garbled Unicode
and spurious punctuation from the given text.

OH: "It scrubs the garble from its stream... or it gets the debugger again!"

  * `span` : `spacy.tokens.span.Span`  
input text `Span`

  * *returns* : `str`  
scrubbed text

---
#### [`split_grafs` method](#pytextrank.split_grafs)
[*\[source\]*](https://github.com/DerwenAI/pytextrank/blob/main/Users/paco/src/pytextrank/pytextrank/util.py#L100)

```python
split_grafs(lines)
```

Segments a raw text, given as a list of lines, into paragraphs.

  * `lines` : `typing.List[str]`  
the raw text document, split into a lists of lines

  * *yields* :  
text per paragraph


---
## [module types](#pytextrank_types)


#### [`StopWordsLike` type](#pytextrank.StopWordsLike)
```python
StopWordsLike = typing.Union[str, pathlib.Path, typing.Dict[str, typing.List[str]]]
```

