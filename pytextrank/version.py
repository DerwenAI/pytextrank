#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/pytextrank#license-and-copyright

import sys
import typing


######################################################################
## Python version checking

MIN_PY_VERSION: typing.Tuple = (3, 7,)
__version__: str = "3.1.1"


def _versify (
    py_version_info: typing.Tuple
    ) -> str:
    """
Semiprivate helper function to convert Python version to a point release (a string).

    py_version_info:
Python version info as a named tuple from the operating system, e.g., from
[`sys.version_info[:2]`](https://docs.python.org/3/library/sys.html#sys.version_info)

    returns:
Python version info in [*semantic versioning*](https://semver.org/) format
    """
    return ".".join([ str(x) for x in py_version_info ])


def _check_version () -> None:
    """
Semiprivate helper function to check the Python version info versus
the minimum required for **pytextrank**.

Throws a `RuntimeError` if the installed Python interpreter is out of
date.
    """
    py_version_info: typing.Tuple = sys.version_info[:2]

    if py_version_info < MIN_PY_VERSION:
        error_msg = "This version of pytextrank requires Python {} or later ({} detected)\n"
        raise RuntimeError(error_msg.format(_versify(MIN_PY_VERSION), _versify(py_version_info)))
