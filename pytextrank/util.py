#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/pytextrank#license-and-copyright

import itertools
import re
import string
import typing
import unicodedata

from spacy.tokens import Span  # type: ignore # pylint: disable=E0401


def groupby_apply (
    data: typing.Iterable[typing.Any],
    keyfunc: typing.Callable,
    applyfunc: typing.Callable,
    ) -> typing.List[typing.Tuple[typing.Any, typing.Any]]:
    """
GroupBy using a key function and an apply function, without a `pandas`
dependency.
See: <https://docs.python.org/3/library/itertools.html#itertools.groupby>

    data:
iterable

    keyfunc:
callable to define the key by which you want to group

    applyfunc:
callable to apply to the group

    returns:
an iterable with the accumulated values
    """
    data = sorted(data, key=keyfunc)

    accum: typing.List[typing.Tuple[typing.Any, typing.Any]] = [
        (k, applyfunc(g),)
        for k, g in itertools.groupby(data, keyfunc)
        ]

    return accum


######################################################################
## utility functions

def default_scrubber (
    span: Span
    ) -> str:
    """
Removes spurious punctuation from the given text.
Note: this is intended for documents in English.

    span:
input text `Span`

    returns:
scrubbed text
    """
    return span.text.replace("'", "")


def maniacal_scrubber (
    span: Span
    ) -> str:
    """
Applies multiple approaches for aggressively removing garbled Unicode
and spurious punctuation from the given text.

OH: "It scrubs the garble from its stream... or it gets the debugger again!"

    span:
input text `Span`

    returns:
scrubbed text
    """
    # some web content returns "not string" ??
    # ostensibly this is no longer possible in Py 3.x ...
    # even so some crazy-making "mixed modes" of character encodings
    # have been found in the wild -- YMMV
    text = span.text

    if type(text).__name__ != "str":
        print("not a string?", type(text), text)

    x = " ".join(map(lambda s: s.strip(), text.split("\n"))).strip()

    x = x.replace('“', '"').replace('”', '"')
    x = x.replace("‘", "'").replace("’", "'").replace("`", "'")
    x = x.replace("…", "...").replace("–", "-")

    x = str(unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8"))

    return x


def split_grafs (
    lines: typing.List[str]
    ) -> typing.Iterator[str]:
    """
Segments a raw text, given as a list of lines, into paragraphs.

    lines:
the raw text document, split into a lists of lines

    yields:
text per paragraph
    """
    graf: typing.List[str] = []

    for line in lines:
        line = line.strip()

        if len(line) < 1:
            if len(graf) > 0:
                yield "\n".join(graf)
                graf = []
        else:
            graf.append(line)

    if len(graf) > 0:
        yield "\n".join(graf)


def filter_quotes (
    text: str,
    *,
    is_email: bool = True,
    ) -> typing.List[str]:
    """
Filter the quoted text out of an email message.
This handles quoting methods for popular email systems.

    text:
raw text data

    is_email:
flag for whether the text comes from an email message;
defaults to `True`

    returns:
the filtered text representing as a list of lines
    """
    _PAT_FORWARD = re.compile(r"\n-+ Forwarded message -+\n")
    _PAT_REPLIED = re.compile(r"\nOn.*\d+.*\n?wrote\:\n+\>")
    _PAT_UNSUBSC = re.compile(r"\n-+\nTo unsubscribe,.*\nFor additional commands,.*")

    if is_email:
        text = str(filter(lambda x: x in string.printable, text))

        # strip off quoted text in a forward
        m = _PAT_FORWARD.split(text, re.M)

        if m and len(m) > 1:
            text = m[0]

        # strip off quoted text in a reply
        m = _PAT_REPLIED.split(text, re.M)

        if m and len(m) > 1:
            text = m[0]

        # strip off any trailing unsubscription notice
        m = _PAT_UNSUBSC.split(text, re.M)

        if m:
            text = m[0]

    # replace any remaining quoted text with blank lines
    lines: typing.List[str] = []

    for line in text.split("\n"):
        if line.startswith(">"):
            lines.append("")
        else:
            lines.append(line)

    return list(split_grafs(lines))
