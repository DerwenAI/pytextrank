#!/bin/bash -e -x

rm -rf dist build pytextrank.egg-info
python3 -m build
twine check dist/*

# this assumes the use of `~/.pypirc`
# https://packaging.python.org/en/latest/specifications/pypirc/

twine upload ./dist/* --verbose
