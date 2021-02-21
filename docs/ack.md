# Acknowledgements

## Contributors

Many thanks to the contributors on this **kglab** project:
[@louisguitton](https://github.com/louisguitton),
[@jake-aft](https://github.com/jake-aft),
[@dmoore247](https://github.com/dmoore247),
plus general support from [Derwen, Inc.](https://derwen.ai/)
and [The Knowledge Graph Conference](https://www.knowledgegraph.tech/),
plus an even larger scope of [use cases](../use_case/) represented by its community.


## Project Lead

[Paco Nathan](https://derwen.ai/paco)
is lead committer on **kglab** and lead author for its documentation and tutorial.
By day he's the Managing Partner at [Derwen, Inc.](https://derwen.ai/)
Paco's formal background is in 
Mathematics (advisor: [Richard Cottle](https://engineering.stanford.edu/people/richard-cottle))
and
Computer Science (advisor: [Douglas Lenat](https://en.wikipedia.org/wiki/Douglas_Lenat)),
with additional work in Design and Linguistics.
His business experience includes: 
Director, VP, and CTO positions leading data teams and machine learning projects;
former CTO/Board member at two publicly-traded tech firms on NASDAQ OTC:BB;
and an equity partner at [Amplify Partners](https://derwen.ai/s/hcxhybks9nbh).
Cited in 2015 as one of the 
[Top 30 People in Big Data and Analytics](http://www.kdnuggets.com/2015/02/top-30-people-big-data-analytics.html)
by Innovation Enterprise.

  * ~40 years tech industry experience, ranging from Bell Labs
    to early-stage start-ups
  * 7+ years R&D in *neural networks* (incl. h/w accelerators) during 1980-90s
  * early "guinea pig" for Amazon AWS (2006), who led the first
    large-scale Hadoop use case on [cloud computing](../glossary/#cloud-computing) (2008)
  * former Director, Community Evangelism at Databricks (2014-2015) for
    [Apache Spark](https://spark.apache.org/)
  * lead committer on [PyTextRank](https://derwen.ai/s/xdw563z8b4gj) ([spaCy](https://spacy.io/) pipeline);
    open source community work on 
    [Jupyter](https://jupyter.org/),
    [Ray](https://ray.io/),
    [Cascading](https://www.cascading.org/)
  * consultant to enterprise organizations for [data strategy](../glossary/#data-strategy);
    advisor to several AI start-ups, including
    [Recognai](https://derwen.ai/s/hk4g),
    [KUNGFU.AI](https://derwen.ai/s/rwg8prbgqp36),
    [Primer](https://derwen.ai/s/tm9jxzcm67hc)

As an author/speaker/instructor, Paco has taught many people (+9000) 
in industry across a range of topics –
[*data science*](../glossary/#data-science),
[*natural language*](../glossary/#natural-language),
[*cloud computing*](../glossary/#cloud-computing),
[*reinforcement learning*](../glossary/#reinforcement-learning),
[*computable content*](../glossary/#computable-content),
etc. –
and through guest lectures at 
Stanford, CMU, UC&nbsp;Berkeley,
U&nbsp;da&nbsp;Coruña, U&nbsp;Manchester,
KTH, NYU, GWU,
U&nbsp;Maryland, Cal&nbsp;Poly, UT/Austin,
U&nbsp;Virginia, CU&nbsp;Boulder.


## Attribution

Please use the following BibTeX entry for citing **kglab** if you use
it in your research or software:

```
@software{kglab,
  author = {Paco Nathan},
  title = {{kglab: a simple abstraction layer in Python for building knowledge graphs}},
  year = 2020,
  publisher = {Derwen},
  doi = {10.5281/zenodo.4516509},
  url = {https://github.com/DerwenAI/kglab}
}
```


## License and Copyright

Source code for **kglab** plus its logo, documentation, and examples
have an [MIT license](https://spdx.org/licenses/MIT.html) which is
succinct and simplifies use in commercial applications.

All materials herein are Copyright &copy; 2020-2021 Derwen, Inc.

[![logo for Derwen, Inc.](https://derwen.ai/static/block_logo.png)](https://derwen.ai/)


## Production Use Cases

  * [Derwen](https://derwen.ai/) and its client projects


## Similar Projects

See also:

  * [PheKnowLator](https://github.com/callahantiff/PheKnowLator)
    * *pro:* quite similar to **kglab** in intent; well-written code; sophisticated, opinionate build of biomedical KGs
    * *con:* less integration with data science tools or distributed systems
  * [LynxKite](https://lynxkite.com/)
    * *pro:* loads of features, lots of adoption
    * *con:* complex tech stack, combines Py/Java/Go; AGPL less-than-business-friendly for production apps
  * [KGTK](https://github.com/usc-isi-i2/kgtk)
    * *pro:* many excellent examples, well-documented in Jupyter notebooks
    * *con:* mostly a CLI tool, primarily based on TSV data
  * [zincbase](https://github.com/complexdb/zincbase)
    * *pro:* probabilistic graph measures, complex simulation suite, leverages GPUs
    * *con:* lacks interchange with RDF or other standard formats
