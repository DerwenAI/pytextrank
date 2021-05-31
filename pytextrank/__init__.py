#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/pytextrank#license-and-copyright

from .base import BaseTextRankFactory, BaseTextRank, Lemma, Phrase, Sentence, VectorElem, StopWordsLike

from .positionrank import PositionRankFactory, PositionRank

from .biasedrank import BiasedTextRankFactory, BiasedTextRank

from .util import groupby_apply, default_scrubber, maniacal_scrubber, split_grafs, filter_quotes

from .version import MIN_PY_VERSION, _versify, _check_version, __version__


######################################################################
## add component factories to the spaCy pipeline namespace

from spacy.language import Language  # type: ignore # pylint: disable=E0401
import pathlib
import typing


_DEFAULT_CONFIG = {
    "edge_weight": BaseTextRankFactory._EDGE_WEIGHT,  # pylint: disable=W0212
    "pos_kept": BaseTextRankFactory._POS_KEPT,  # pylint: disable=W0212
    "token_lookback": BaseTextRankFactory._TOKEN_LOOKBACK,  # pylint: disable=W0212
    "scrubber": None,
    "stopwords": None,
    }


@Language.factory("textrank", default_config=_DEFAULT_CONFIG)
def _create_component_tr (
    nlp: Language,  # pylint: disable=W0613
    name: str,  # pylint: disable=W0613
    edge_weight: float,
    pos_kept: typing.List[str],
    token_lookback: int,
    scrubber: typing.Optional[typing.Callable],
    stopwords: typing.Optional[StopWordsLike],
    ) -> BaseTextRankFactory:
    """
Component factory for the `TextRank` base class.
    """
    return BaseTextRankFactory(
        edge_weight = edge_weight,
        pos_kept = pos_kept,
        token_lookback = token_lookback,
        scrubber = scrubber,
        stopwords = stopwords,
        )


@Language.factory("positionrank", default_config=_DEFAULT_CONFIG)
def _create_component_pr (
    nlp: Language,  # pylint: disable=W0613
    name: str,  # pylint: disable=W0613
    edge_weight: float,
    pos_kept: typing.List[str],
    token_lookback: int,
    scrubber: typing.Optional[typing.Callable],
    stopwords: typing.Optional[StopWordsLike],
    ) -> PositionRankFactory:
    """
Component factory for the `PositionRank` extended class.
    """
    return PositionRankFactory(
        edge_weight = edge_weight,
        pos_kept = pos_kept,
        token_lookback = token_lookback,
        scrubber = scrubber,
        stopwords = stopwords,
        )


@Language.factory("biasedtextrank", default_config=_DEFAULT_CONFIG)
def _create_component_br (
    nlp: Language,  # pylint: disable=W0613
    name: str,  # pylint: disable=W0613
    edge_weight: float,
    pos_kept: typing.List[str],
    token_lookback: int,
    scrubber: typing.Optional[typing.Callable],
    stopwords: typing.Optional[StopWordsLike],
    ) -> BiasedTextRankFactory:
    """
Component factory for the `BiasedTextRank` extended class.
    """
    return BiasedTextRankFactory(
        edge_weight = edge_weight,
        pos_kept = pos_kept,
        token_lookback = token_lookback,
        scrubber = scrubber,
        stopwords = stopwords,
        )
