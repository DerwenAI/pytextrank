#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Shared fixture functions."""
import pathlib
import pytest
import spacy
from spacy.language import Language
from spacy.tokens import Doc


@pytest.fixture(scope="session")
def nlp () -> Language:
    """Language shared fixture."""
    nlp = spacy.load("en_core_web_sm")
    return nlp


@pytest.fixture(scope="session")
def doc (nlp: Language) -> Doc:
    """Doc shared fixture.

    Returns:
        spaCy EN doc containing a piece of football news.
    """
    text = pathlib.Path("dat/cfc.txt").read_text()
    doc = nlp(text)
    return doc

@pytest.fixture(scope="session")
def long_doc (nlp: Language) -> Doc:
    """Doc shared fixture.

    Returns:
        spaCy EN doc containing a long text.
    """
    text = pathlib.Path("dat/lee.txt").read_text()
    doc = nlp(text)
    return doc