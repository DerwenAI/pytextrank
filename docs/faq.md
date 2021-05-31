# Troubleshooting FAQ

The following items may help with troubleshooting frequently asked
questions.

First, we have a a few quick questions to check before you report any
potential bugs:

  * Which version of **PyTextRank** are you using?
  * Which version of spaCy are you using?
  * What operating system and version?
  * Did you install through which of the following methods?
    * `pip`
    * `conda`
    * direct source installation from a cloned Git repo
  * Are you using any virtual environment, such as [`venv`](https://docs.python.org/3/tutorial/venv.html)?
  * Is the code running as a script, or within a notebook such as [JupyterLab](https://jupyterlab.readthedocs.io/)?

A good way to collect this information is to run:
```
python -m spacy info
```


## Jupyter works fine, but JupyterLab fails to use the correct environment

If you are running code inside of JupyterLab, there can also be
conflicts among the path environment variables settings.

A JupyterLab kernel may be running a different Python executable than
scripts launched from the same command line as JupyterLab.
There is a known Conda problem; see
<https://github.com/explosion/spaCy/discussions/7435>
for details.

To confirm, run the following code in a notebook cell and compare
with the Python executable that you expect to find:
```
import sys
print(sys.executable)
```

Conda is overly aggressive about how it modifies Bash profiles during
installation – and not in an especially helpful way.



## AttributeError: type object 'Language' has no attribute 'factory'

This message is a spaCy 2.x error.

Somewhere, somehow, a Python environment with spaCy 2.x installed must
be getting called instead of the expected spaCy 3.x library.
Or perhaps you may be using **PyTextRank** 3.x with spaCy 2.x instead?

To confirm, run the following code in your Python script and see if it
uses the expected executable:
```
import sys
print(sys.executable)
```
