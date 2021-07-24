#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import sys
import traceback

import kglab  # pylint: disable=E0401,W0611
import rdflib  # pylint: disable=E0401,W0611

from mkrefs import PackageDoc  # pylint: disable=E0401
from mkrefs.util import render_reference  # pylint: disable=E0401


if __name__ == "__main__":
    package_name = "pytextrank"
    git_url = "https://github.com/DerwenAI/pytextrank/blob/main"
    includes = [
        "BaseTextRankFactory",
        "BaseTextRank",
        "PositionRankFactory",
        "PositionRank",
        "BiasedTextRankFactory",
        "BiasedTextRank",
        "Lemma",
        "Paragraph",
        "Phrase",
        "Sentence",
        "VectorElem",
    ]

    pkg_doc = PackageDoc(
        package_name,
        git_url,
        includes,
    )


    try:
        pkg_doc.build()

        # render the JSON into Markdown using the Jinja2 template
        groups = {
            "package": [ pkg_doc.meta ],
        }

        print(groups)

        template_path = pathlib.Path("docs/ref.jinja")
        markdown_path = pathlib.Path("docs/ref.md")

        render_reference(
            template_path,
            markdown_path,
            groups,
        )

        sys.exit(0)

        # show results
        kg = pkg_doc.get_rdf()
        print(kg.save_rdf_text())

    except Exception:  # pylint: disable=W0703
        traceback.print_exc()
