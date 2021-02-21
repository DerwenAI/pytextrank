#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Callable, Iterable, List, Tuple
import itertools
import re
import string
import unicodedata


def groupby_apply (
    data: Iterable[Any],
    keyfunc: Callable,
    applyfunc: Callable,
    ) -> List[Tuple[Any, Any]]:
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
    accum = [ (k, applyfunc(g)) for k, g in itertools.groupby(data, keyfunc) ]

    return accum


######################################################################
## utility functions

PAT_FORWARD = re.compile(r"\n-+ Forwarded message -+\n")
PAT_REPLIED = re.compile(r"\nOn.*\d+.*\n?wrote\:\n+\>")
PAT_UNSUBSC = re.compile(r"\n-+\nTo unsubscribe,.*\nFor additional commands,.*")


def split_grafs (lines):
    """
    segment raw text, given as a list of lines, into paragraphs
    """
    graf = []

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


def filter_quotes (text, is_email=True):
    """
    filter the quoted text out of a message
    """
    global PAT_FORWARD, PAT_REPLIED, PAT_UNSUBSC

    if is_email:
        text = filter(lambda x: x in string.printable, text)

        # strip off quoted text in a forward
        m = PAT_FORWARD.split(text, re.M)

        if m and len(m) > 1:
            text = m[0]

        # strip off quoted text in a reply
        m = PAT_REPLIED.split(text, re.M)

        if m and len(m) > 1:
            text = m[0]

        # strip off any trailing unsubscription notice
        m = PAT_UNSUBSC.split(text, re.M)

        if m:
            text = m[0]

    # replace any remaining quoted text with blank lines
    lines = []

    for line in text.split("\n"):
        if line.startswith(">"):
            lines.append("")
        else:
            lines.append(line)

    return list(split_grafs(lines))


def maniacal_scrubber (text):
    """
    it scrubs the garble from its stream...
    or it gets the debugger again
    """
    x = " ".join(map(lambda s: s.strip(), text.split("\n"))).strip()

    x = x.replace('“', '"').replace('”', '"')
    x = x.replace("‘", "'").replace("’", "'").replace("`", "'")
    x = x.replace("…", "...").replace("–", "-")

    x = str(unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode("utf-8"))

    # some web content returns "not string" ??
    # ostensibly this is no longer possible in Py 3.x ...
    # even so some crazy-making "mixed modes" of character encodings
    # have been found in the wild -- YMMV

    try:
        assert type(x).__name__ == "str"
    except AssertionError:
        print("not a string?", type(line), line)

    return x


def default_scrubber (text):
    """
    remove spurious punctuation (for English)
    """
    return text.replace("'", "")
