"""Shared fixture functions."""
import pytest
import spacy
from spacy.language import Language
from spacy.tokens import Doc


@pytest.fixture(scope="session")
def nlp() -> Language:
    """Language shared fixture."""
    nlp = spacy.load("en_core_web_sm")
    return nlp


@pytest.fixture(scope="session")
def doc(nlp: Language) -> Doc:
    """Doc shared fixture.

    Returns:
        spaCy EN doc containing a piece of football news.
    """
    text = """
    Chelsea 'opted against' signing Salomon Rondón on deadline day.

    Chelsea reportedly opted against signing Salomón Rondón on deadline day despite
    their long search for a new centre forward.
    With Olivier Giroud expected to leave, the Blues targeted Edinson Cavani,
    Dries Mertens and Moussa Dembele – only to end up with none of them.
    According to Telegraph Sport, Dalian Yifang offered Rondón to Chelsea only for
    them to prefer keeping Giroud at the club.
    Manchester United were also linked with the Venezuela international before agreeing
    a deal for Shanghai Shenhua striker Odion Ighalo.
    Manager Frank Lampard made no secret of his transfer window frustration, hinting
    that to secure top four football he ‘needed’ signings.
    Their draw against Leicester on Saturday means they have won just four of the last
    13 Premier League matches.
    """
    doc = nlp(text)
    return doc
