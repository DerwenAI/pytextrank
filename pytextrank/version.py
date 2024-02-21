#!/usr/bin/env python
# -*- coding: utf-8 -*-
# see license https://github.com/DerwenAI/pytextrank#license-and-copyright

"""
Describe the GitHub repo version tags and commit hash for
the `pytextrank` library.
"""

from os.path import dirname, abspath
import pathlib
import typing

from git import Repo  # pylint: disable=E0401  # type: ignore


## use the local Git info for version info, if available
REPO_HASH: str = "xxxxxxxxx"  # default/placeholder
REPO_TAGS: str = "refs/tags/v1.0.0"  # default/placeholder

try:
    repo_path: pathlib.Path = pathlib.Path(dirname(abspath(__file__)))
    repo: Repo = Repo(repo_path.parents[0])

    REPO_HASH = str(repo.head.commit)
    REPO_TAGS = repo.tags
except Exception as ex:  # pylint: disable=W0703
    print(ex)


# cast version string into a float
try:
    v_seq: typing.List[ str ] = str(REPO_TAGS[-1]).replace("v", "").split(".")[:3]

    __version__ = ".".join(v_seq)  # this is the OpenAPI documentation version

    __version_major__ = int(v_seq[0])
    __version_minor__ = int(v_seq[1])
    __version_patch__ = int(v_seq[2])
except IndexError:
    # the code above may fail in Github Actions workflow
    __version__ = "0.0+test"

    __version_major__ = 0
    __version_minor__ = 0
    __version_patch__ = 0


def get_repo_version (
    ) -> typing.Tuple[ str, str ]:
    """
Access the Git repository information and return items to identify
the version/commit running in production.

    returns:
version tag and commit hash
    """
    return __version__, REPO_HASH
