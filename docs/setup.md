# Tutorial Setup

You should be able to run the notebooks for this tutorial locally on a
recent laptop.

### Clone the Git repository

First clone the Git repository and install the dependencies:
```
git clone https://github.com/DerwenAI/pytextrank.git
cd pytextrank
```

### Install Dependencies

If you're using `pip` to install libraries, it's a good practice
first to create a 
[*virtual environment*](https://docs.python.org/3/tutorial/venv.html)
and activate it:
```
python3 -m venv venv
source venv/bin/activate
```

Then install the dependencies for this tutorial:
```
python3 -m pip install -U pip
python3 -m pip install -r requirements.txt
python3 -m spacy download en_core_web_sm
```

Alternatively, to install the dependencies using `conda`:
```
conda env create -f environment.yml
conda activate pytextrank
python3 -m spacy download en_core_web_sm
```

### Install JupyterLab

Next, make sure to install
[JupyterLab](https://jupyterlab.readthedocs.io/).

If you're using `pip` then you can run:
```
python3 -m pip install jupyterlab
```

If you need to install via `pip install --user` then you must add the
user-level `bin` directory to your `PATH` environment variable in
before launching JupyterLab.
If you're using a Unix derivative (FreeBSD, GNU/Linux, OS X), you can
use the `export PATH="$HOME/.local/bin:$PATH"` command.

To install using `conda`:
```
conda install -c conda-forge jupyterlab
```

### Running Notebooks

If you're using `pip` with a virtual environment but also have `conda`
installed, be careful about one issue ... it turns out that the
`conda` installer is somewhat "overly zealous" and can munge your
environment paths.

To avoid path errors for the Python executable, when you have a
virtual environment running as described above, the best way to launch
JupyterLab is:
```
./venv/bin/jupyter-lab
```

This will cause JupyterLab to open a new tab in your browser, or
launch your default browser if it wasn't already running

At this point, open the `examples` subdirectory to launch the
notebooks featured throughout the following sections of this tutorial.
