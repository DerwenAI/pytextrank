#!/usr/bin/env python
# encoding: utf-8

import pytextrank
import sys
import unicodedata

DEBUG = False # True

def cleanup_text (text):
    """
    It scrubs the unreadable characters out of its stream...
    Or it gets the debugger again.
    """
    x = " ".join(map(lambda x: x.strip(), text.split("\n"))).strip()

    x = x.replace('“', '"').replace('”', '"')
    x = x.replace("‘", "'").replace("’", "'")
    x = x.replace('…', '...').replace('–', '-')

    x = str(unicodedata.normalize('NFKD', x).encode('ascii', 'ignore'))

    return x


if __name__ == "__main__":
    path = sys.argv[1]

    with open(path) as f:
        text = f.read()

        j = {}
        j["id"] = "777"
        j["text"] = cleanup_text(text)

        print(pytextrank.pretty_print(j))
