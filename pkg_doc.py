#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyfixdoc
import sys


######################################################################
## main entry point

if __name__ == "__main__":
    # NB: `inspect` is picky about paths and current working directory
    # this only works if run from the top-level directory of the repo
    sys.path.insert(0, "../")

    # customize the following, per use case
    import pytextrank # pylint: disable=W0611

    class_list = [
        "BaseTextRankFactory",
        "BaseTextRank",
        "TopicRankFactory",
        "TopicRank",
        "PositionRankFactory",
        "PositionRank",
        "BiasedTextRankFactory",
        "BiasedTextRank",
        "Lemma",
        "Phrase",
        "Sentence",
        "VectorElem",
        ]

    pkg_doc = pyfixdoc.PackageDoc(
        "pytextrank",
        "https://github.com/DerwenAI/pytextrank/blob/main",
        class_list,
        )

    # NB: uncomment to analyze/troubleshoot the results of `inspect`
    #pkg_doc.show_all_elements(); sys.exit(0)

    # build the apidocs markdown
    pkg_doc.build()

    # output the apidocs markdown
    ref_md_file = sys.argv[1]
    pkg_doc.write_markdown(ref_md_file)
