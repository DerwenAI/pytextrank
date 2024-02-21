#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/pytextrank#license-and-copyright

"""
Package definitions for the `pytextrank` library.
"""

import pathlib
import typing

from spacy.language import Language  # type: ignore # pylint: disable=E0401

from .base import BaseTextRankFactory, BaseTextRank, Lemma, Paragraph, Phrase, Sentence, VectorElem, StopWordsLike

from .biasedrank import BiasedTextRankFactory, BiasedTextRank

from .positionrank import PositionRankFactory, PositionRank

from .topicrank import TopicRankFactory, TopicRank

from .util import groupby_apply, default_scrubber, maniacal_scrubber, split_grafs, filter_quotes

from .version import get_repo_version, \
    __version__, __version_major__, __version_minor__, __version_patch__


######################################################################
## add component factories to the spaCy pipeline namespace

_DEFAULT_CONFIG = {
    "edge_weight": BaseTextRankFactory._EDGE_WEIGHT,  # pylint: disable=W0212
    "pos_kept": BaseTextRankFactory._POS_KEPT,  # pylint: disable=W0212
    "token_lookback": BaseTextRankFactory._TOKEN_LOOKBACK,  # pylint: disable=W0212
    "scrubber": None,
    "stopwords": None,
    }

_TOPIC_DEFAULT_CONFIG = {
    **_DEFAULT_CONFIG,
    "threshold": TopicRankFactory._CLUSTER_THRESHOLD,  # pylint: disable=W0212
    "method": TopicRankFactory._CLUSTER_METHOD,  # pylint: disable=W0212
    }


# wrap these factory definitions in a try-catch, so they don't cause
# exceptions during programmatic loading with `importlib`

try:
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


    @Language.factory("topicrank", default_config=_TOPIC_DEFAULT_CONFIG)
    def _create_component_tor (
        nlp: Language,  # pylint: disable=W0613
        name: str,  # pylint: disable=W0613
        edge_weight: float,
        pos_kept: typing.List[str],
        token_lookback: int,
        scrubber: typing.Optional[typing.Callable],
        stopwords: typing.Optional[StopWordsLike],
        threshold: float,
        method: str,
        ) -> TopicRankFactory:
        """
Component factory for the `TopicRank` extended class.
        """
        return TopicRankFactory(
            edge_weight = edge_weight,
            pos_kept = pos_kept,
            token_lookback = token_lookback,
            scrubber = scrubber,
            stopwords = stopwords,
            threshold = threshold,
            method = method,
        )

except Exception:  # pylint: disable=W0703
    print("ERROR: it appears that `spaCy` 3.x has not been imported?")
