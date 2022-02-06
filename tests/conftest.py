#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore

"""Shared fixture functions."""
import pathlib
import pytest  # pylint: disable=E0401
import spacy  # pylint: disable=E0401
from spacy.language import Language  # pylint: disable=E0401
from spacy.tokens import Doc  # pylint: disable=E0401


@pytest.fixture(scope="module")
def nlp () -> Language:
    """
Language shared fixture.
    """
    nlp = spacy.load("en_core_web_sm")  # pylint: disable=W0621
    return nlp


def get_doc (nlp: Language, file_path: str) -> Doc:  # pylint: disable=W0621
    """
Doc shared fixture.

    file_path:
String specifying the path to the doc of interest.

    returns:
spaCy EN doc containing the data from ``file_path``.
    """
    text = pathlib.Path(file_path).read_text()
    doc = nlp(text)  # pylint: disable=W0621
    return doc


@pytest.fixture(scope="module")
def doc_ars (nlp: Language) -> Doc:  # pylint: disable=W0621
    """
Doc shared fixture.

    returns:
spaCy EN doc containing a piece of weather research.
    """
    return get_doc(nlp, "dat/ars.txt")


@pytest.fixture(scope="module")
def doc_cfc (nlp: Language) -> Doc:  # pylint: disable=W0621
    """
Doc shared fixture.

    returns:
spaCy EN doc containing a piece of football news.
    """
    return get_doc(nlp, "dat/cfc.txt")


@pytest.fixture(scope="module")
def doc_gen (nlp: Language) -> Doc:  # pylint: disable=W0621
    """
Doc shared fixture.

    returns:
spaCy EN doc containing a bit of information on TextRank.
    """
    return get_doc(nlp, "dat/gen.txt")


@pytest.fixture(scope="module")
def doc_lee (nlp: Language) -> Doc:  # pylint: disable=W0621
    """
Doc shared fixture.

    returns:
spaCy EN doc containing a bit of news on Google's AlphaGo AI.
    """
    return get_doc(nlp, "dat/lee.txt")


@pytest.fixture(scope="module")
def doc_mih (nlp: Language) -> Doc:  # pylint: disable=W0621
    """
Doc shared fixture.

    returns:
spaCy EN doc containing a bit of math text.
    """
    return get_doc(nlp, "dat/mih.txt")


@pytest.fixture(scope="module")
def doc_suz (nlp: Language) -> Doc:  # pylint: disable=W0621
    """
Doc shared fixture.

    returns:
spaCy EN doc containing a bit of text with chemistry terms.
    """
    return get_doc(nlp, "dat/suz.txt")

doc = doc_cfc
long_doc = doc_lee
