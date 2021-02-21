# Build Instructions

!!! note
    In most cases you won't need to build this package locally.

Unless you're doing development work on the **kglab** library itself,
simply install based on the instructions in
["Getting Started"](https://derwen.ai/docs/kgl/start/).


## Setup

To set up the build environment locally:
```
pip install -r requirements_build.txt
```

You will also need to download
[`ChromeDriver`](https://chromedriver.chromium.org/downloads) 
for your version of the `Chrome` brower, saved as `chromedriver` in this directory.


## Type Checking

This project uses [`typing`](https://docs.python.org/3/library/typing.html)
and [`mypy`](https://mypy.readthedocs.io/) for *type checking*.

To run type checking:
```
mypy kglab/*.py
```


## Code Checking

This project uses [`pylint`](https://www.pylint.org/) for *code checking*.

To run code checking:
```
pylint kglab/*.py
```


## Test Coverage

This project uses `unittest` and 
[`coverage`](https://coverage.readthedocs.io/)
for *unit test* coverage. 
Source for unit tests is in the 
[`test.py`](https://github.com/DerwenAI/kglab/blob/main/test.py)
module.

To run unit tests:
```
coverage run -m unittest discover
```

To generate a coverage report and (providing you have the access
token) upload it to the `codecov.io` reporting site:
```
coverage report
bash <(curl -s https://codecov.io/bash) -t @.cc_token
```

Test coverage reports can be viewed at
<https://codecov.io/gh/DerwenAI/kglab>


## Online Documentation

To generate documentation pages, this project uses:

  * [`MkDocs`](https://www.mkdocs.org/)
  * [`makedocs-material`](https://squidfunk.github.io/mkdocs-material/)
  * [`pymdown-extensions`](https://facelessuser.github.io/pymdown-extensions/)
  * [`MathJax`](https://www.mathjax.org/)
  * [`Jupyter`](https://jupyter.org/install)
  * [`nbconvert`](https://nbconvert.readthedocs.io/)
  * [`Selenium`](https://selenium-python.readthedocs.io/)
  * [`Chrome`](https://www.google.com/chrome/)
  * [`Flask`](https://flask.palletsprojects.com/)

Source for the documentation is in the 
[`docs`](https://github.com/DerwenAI/kglab/tree/main/docs)
subdirectory.

To build the documentation:
```
./bin/nb_md.sh
./pkg_doc.py docs/ref.md
mkdocs build
```

To preview the generated microsite locally:
```
./bin/preview.py
```

Then browse to <http://localhost:8000> to review the generated
documentation.

To package the generated microsite for deployment on a
Flask/WSGI server:
```
tar cvzf kgl.tgz site/
```


## Package Release

To update the [release on PyPi](https://pypi.org/project/kglab/):
```
./bin/push_pypi.sh
```
