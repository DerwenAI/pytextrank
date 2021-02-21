from .base import BaseTextRank, Phrase, PhraseLike, Node

from .positionrank import PositionRank

from .util import groupby_apply, default_scrubber, maniacal_scrubber, split_grafs, filter_quotes

from .version import MIN_PY_VERSION, _versify, _check_version, __version__


######################################################################
## add component factories to the spaCy pipeline namespace

from spacy.language import Language  # type: ignore
import typing


_DEFAULT_CONFIG = {
    "edge_weight": BaseTextRank._EDGE_WEIGHT,
    "pos_kept": BaseTextRank._POS_KEPT,
    "token_lookback": BaseTextRank._TOKEN_LOOKBACK,
    "scrubber": None,
    }


@Language.factory("textrank", default_config=_DEFAULT_CONFIG)
def _create_component_tr (
    nlp: Language,
    name: str,
    edge_weight: float,
    pos_kept: typing.List[str],
    token_lookback: int,
    scrubber: typing.Optional[typing.Callable],
    ) -> BaseTextRank:
    """
Component factory for the `TextRank` base class.
    """
    return BaseTextRank(
        edge_weight = edge_weight,
        pos_kept = pos_kept,
        token_lookback = token_lookback,
        scrubber = scrubber,
        )

@Language.factory("positionrank", default_config=_DEFAULT_CONFIG)
def _create_component_pr (
    nlp: Language,
    name: str,
    edge_weight: float,
    pos_kept: typing.List[str],
    token_lookback: int,
    scrubber: typing.Optional[typing.Callable],
    ) -> BaseTextRank:
    """
Component factory for the `PositionRank` extended class.
    """
    return PositionRank(
        edge_weight = edge_weight,
        pos_kept = pos_kept,
        token_lookback = token_lookback,
        scrubber = scrubber,
        )
