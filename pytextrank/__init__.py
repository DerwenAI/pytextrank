from .base import BaseTextRank, Phrase

from .positionrank import PositionRank

from .util import groupby_apply, split_grafs, filter_quotes, maniacal_scrubber, default_scrubber

from .version import MIN_PY_VERSION, _versify, _check_version, __version__


######################################################################
## add component factories to the spaCy pipeline namespace

from spacy.language import Language
from typing import Callable, List

_DEFAULT_CONFIG = {
    "edge_weight": BaseTextRank._EDGE_WEIGHT,
    "pos_kept": BaseTextRank._POS_KEPT,
    "scrubber": str.strip,
    "token_lookback": BaseTextRank._TOKEN_LOOKBACK,
    }


@Language.factory("textrank", default_config=_DEFAULT_CONFIG)
def _create_component (
    nlp: Language,
    name: str,
    edge_weight: float,
    pos_kept: List[str],
    scrubber: Callable,
    token_lookback: int,
    ) -> BaseTextRank:
    """
Component factory for the `TextRank` base class.
    """
    return BaseTextRank(
        edge_weight = edge_weight,
        pos_kept = pos_kept,
        scrubber = scrubber,
        token_lookback = token_lookback,
        )

@Language.factory("positionrank", default_config=_DEFAULT_CONFIG)
def _create_component (
    nlp: Language,
    name: str,
    edge_weight: float,
    pos_kept: List[str],
    scrubber: Callable,
    token_lookback: int,
    ) -> BaseTextRank:
    """
Component factory for the `PositionRank` extended class.
    """
    return PositionRank(
        edge_weight = edge_weight,
        pos_kept = pos_kept,
        scrubber = scrubber,
        token_lookback = token_lookback,
        )
