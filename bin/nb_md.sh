#!/bin/bash -e

for notebook_path in examples/*.ipynb; do
    [ -e "$notebook_path" ] || continue

    notebook=`basename $notebook_path`
    stem=`basename $notebook_path .ipynb`

    cp $notebook_path docs/$notebook
    jupyter nbconvert docs/$notebook --to markdown
    python bin/vis_doc.py docs/"$stem".md
    rm docs/$notebook
done