# Simple worked example of pip-tools

## Overview

### requirements.in and requirements.txt
initial requirements.in file
Differences from current requirements.txt - no version on networkx
Changes for comparison requirements.in
> Updated spacy version spacy >= 3.0 to spacy >= 3.1
```requirements.txt
# requirements.in
# graphviz >= 0.13
graphviz >= 0.13
# icecream >= 2.1
icecream >= 2.1
# networkx[default] >= 2.6
networkx[default]
# pygments >= 2.7.4
pygments >= 2.7.4
# scipy >= 1.7
scipy >= 1.7
# spacy >= 3.0
spacy >= 3.0
```
```requirements.txt
# requirements.in to generate new_requirements.txt for example
# As Above
# Update Spacy Version new_requirements.in
spacy >= 3.1
```
### requirements_viz.in and requirements_viz.txt
Used the requirements-vix.in file to generate the requirements_viz.txt file.
Used the layering of requirements_viz.in files to generate the requirements_viz.txt file.
I did not specify the version of altair in the requirements_viz.in file.
```requirements.txt
# requirements_viz.in
# Use requirements.txt
-c requirements.txt
#altair >= 4.1.0
altair
```

### Generating the requirements.txt and requirements_viz.txt files
#### Initial requirements.txt and requirements_viz.txt files
```bash
pip-compile --generate-hashes --output-file requirements.txt requirements.in
```
```bash
pip-compile --generate-hashes --output-file requirements_viz.txt requirements_viz.in
```

#### Generating new_requirements.txt and new_requirements_viz.txt files
```bash
pip-compile --generate-hashes --output-file new_requirements.txt new_requirements.in
```
```bash
pip-compile --generate-hashes --output-file new_requirements_viz.txt new_requirements_viz.in
```

### Comparing the requirements.txt and new_requirements.txt files
```bash
sdiff -s requirements.txt new_requirements.txt | tee check_diff_requirements.txt
```
```bash
sdiff -s requirements_viz.txt new_requirements_viz.txt | tee check_diff_requirements_viz.txt
```


