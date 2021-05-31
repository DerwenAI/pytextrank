#!/bin/bash -e

## debugging the uploaded README:
# pandoc README.md --from markdown --to rst -s -o README.rst

rm -rf dist
python setup.py sdist bdist_wheel
twine upload --verbose dist/*