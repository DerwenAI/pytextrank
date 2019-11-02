Python impl for TextRank
========================

Python implementation of *TextRank* as a
`spaCy extension <https://explosion.ai/blog/spacy-v2-pipelines-extensions>`_,
to extract the top-ranked phrases from a text document.

This work is based on the paper
`TextRank: Bringing Order into Text <https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf>`_
by 
`Rada Mihalcea <https://web.eecs.umich.edu/~mihalcea/>`_,
`Paul Tarau <https://www.cse.unt.edu/~tarau/>`_;
`Empirical Methods in Natural Language Processing <https://www.researchgate.net/publication/200044196_TextRank_Bringing_Order_into_Texts>`_
(2004).

Modifications to the algorithm originallly described in the paper include:

-  fixed bug; see `Java impl, 2008 <https://github.com/ceteri/textrank>`_
-  uses *lemmatization* in place of stemming
-  includes verbs in the graph (but not in resulting phrases by default)
-  leverages preprocessing based on *noun chunking* and x*named entity recognition*
-  provides *extractive summarization* based on vectors of ranked phrases
-  allows use of *knowledge graph* for enriching the lemma graph

This implementation was originally inspired by the
 `Williams 2016 <http://mike.place/2016/summarization/>`_
talk on *text summarization*.


Usage
-----

For example usage, see the
`PyTextRank wiki <https://github.com/DerwenAI/pytextrank/wiki>`_.

If you need to troubleshoot any problems:

- use `GitHub issues <https://github.com/DerwenAI/pytextrank/issues>`_ (recommended)
- search `related discussions on StackOverflow <https://stackoverflow.com/search?q=pytextrank>`_

For related course materials and training, see the calendar updates in the article
`Natural Language Processing in Python <https://medium.com/derwen/natural-language-processing-in-python-832b0a99791b>`_.

If you have questions about related consulting work, contact `Derwen, Inc. <https://derwen.ai/contact>`_



Dependencies and Installation
-----------------------------

This code has dependencies on other Python projects:

-  `spaCy <https://spacy.io/docs/usage/>`_
-  `NetworkX <http://networkx.readthedocs.io/>`_

To install from `PyPi <https://pypi.python.org/pypi/pytextrank>`_:

::

    pip install pytextrank


To install from this Git repo:

::

    pip install -r requirements.txt


Attribution
-----------
*PyTextRank* has an `MIT <https://spdx.org/licenses/MIT.html>`_ 
license, so you can use it for commercial applications.

Please let us know if you find this useful, and tell us about use cases, 
what else you'd like to see integrated, etc.

Here's a Bibtex entry for citing *PyTextRank* in publications:

::

    @Misc{PyTextRank,
    author =   {Nathan, Paco},
    title =    {PyTextRank, a Python implementation of TextRank for text document NLP parsing and summarization},
    howpublished = {\url{https://github.com/DerwenAI/pytextrank/}},
    year = {2016}
    }


Kudos
-----

Many thanks to all of the contributors:
`@htmartin <https://github.com/htmartin>`_,
`@williamsmj <https://github.com/williamsmj/>`_,
`@eugenep <https://github.com/eugenep/>`_,
`@mattkohl <https://github.com/mattkohl>`_,
`@vanita5 <https://github.com/vanita5>`_,
`@HarshGrandeur <https://github.com/HarshGrandeur>`_,
`@mnowotka <https://github.com/mnowotka>`_,
`@kjam <https://github.com/kjam>`_,
`@dvsrepo <https://github.com/dvsrepo>`_,
`@SaiThejeshwar <https://github.com/SaiThejeshwar>`_,
`@laxatives <https://github.com/laxatives>`_,
`@dimmu <https://github.com/dimmu>`_,
and for support from
`Derwen, Inc. <https://derwen.ai/>`_.
