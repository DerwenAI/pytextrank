#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate the `apidocs` markdown needed for the package reference.
"""

import importlib
import json
import sys

import pyfixdoc


######################################################################
## main entry point

if __name__ == "__main__":
    ref_md_file: str = sys.argv[1]

    # NB: `inspect` is picky about paths and current working directory
    # this only works if run from the top-level directory of the repo
    sys.path.insert(0, "../")

    with open("pkg_doc.cfg", "r", encoding="utf-8") as fp:
        config: dict = json.load(fp)

        importlib.import_module(config["module"])

        pkg_doc: pyfixdoc.PackageDoc = pyfixdoc.PackageDoc(
            config["module"],
            config["src_url"],
            config["classes"],
        )

        # NB: uncomment to analyze/troubleshoot the results of `inspect`
        #pkg_doc.show_all_elements(); sys.exit(0)

        # build the apidocs markdown
        pkg_doc.build()

        # output the apidocs markdown
        pkg_doc.write_markdown(ref_md_file)
