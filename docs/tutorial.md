# Tutorial Setup

The coding samples in the following notebooks help illustrate the use
of **pytextrank** and related libraries in Python.


## Prerequisites

  * Some coding experience in Python (you can read a 20-line program)
  * Interest in use cases that need to use *natural language processing*


## Audience

  * You are a Python programmer who needs to learn how to use available NLP packages
  * You work on a data science team and have some Python experience, and now you need to leverage NLP and text mining
  * You have interests in chatbots, deep learning, and related AI work, and want to understand the basics for handling text data in those use cases


## Key Takeaways

  * Hands-on experience with popular open source libraries in Python for natural language
  * Coding examples that can be used as starting points for your own NLP projects
  * Ways to integration natural language work with other aspects of graph-based data science


## Installation

You can run the notebooks locally on a recent laptop.
First clone the Git repository and install the dependencies:
```
git clone https://github.com/DerwenAI/pytextrank.git
cd pytextrank

pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Also make sure to install
[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/).
To install using `conda`:
```
conda install -c conda-forge jupyterlab
```

Or if you use `pip` you can install it with:
```
pip install jupyterlab
```

For installing via `pip install --user` you must add the user-level
bin directory to your `PATH` environment variable in order to launch
JupyterLab.
If you're using a Unix derivative (FreeBSD, GNU/Linux, OS X), you can 
achieve this by using the `export PATH="$HOME/.local/bin:$PATH"` command.

Once installed, launch JupyterLab with:
```
jupyter-lab
```

Then open the `examples` subdirectory to launch the notebooks featured
in the following sections of this tutorial.
