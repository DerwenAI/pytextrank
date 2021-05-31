#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore

"""Shared fixture functions."""
import pathlib
import pytest  # pylint: disable=E0401
import spacy  # pylint: disable=E0401
from spacy.language import Language  # pylint: disable=E0401
from spacy.tokens import Doc  # pylint: disable=E0401


@pytest.fixture(scope="session")
def nlp () -> Language:
    """
Language shared fixture.
    """
    nlp = spacy.load("en_core_web_sm")  # pylint: disable=W0621
    return nlp


@pytest.fixture(scope="session")
def doc (nlp: Language) -> Doc:  # pylint: disable=W0621
    """
Doc shared fixture.

    returns:
spaCy EN doc containing a piece of football news.
    """
    text = pathlib.Path("dat/cfc.txt").read_text()
    doc = nlp(text)  # pylint: disable=W0621
    return doc


@pytest.fixture(scope="session")
def long_doc (nlp: Language) -> Doc:  # pylint: disable=W0621
    """
Doc shared fixture.

    returns:
spaCy EN doc containing a long text.
    """
    text = pathlib.Path("dat/lee.txt").read_text()
    doc = nlp(text)  # pylint: disable=W0621
    return doc
