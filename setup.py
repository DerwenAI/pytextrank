# type: ignore

import importlib.util
import pathlib
import setuptools
import typing


KEYWORDS = [
    "biased textrank",
    "entity linking",
    "extractive summarization",
    "graph algorithms",
    "knowledge graph",
    "natural language processing",
    "nlp",
    "parsing",
    "phrase extraction",
    "pipeline component",
    "positionrank",
    "spacy",
    "text analytics",
    "textgraphs",
    "textrank",
    ]


def parse_requirements_file (filename: str) -> typing.List:
    """read and parse a Python `requirements.txt` file, returning as a list of str"""
    results: list = []

    with pathlib.Path(filename).open() as f:
        for l in f.readlines():
            results.append(l.strip().replace(" ", "").split("#")[0])

    return results


if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location("pytextrank.version", "pytextrank/version.py")
    pytr_version = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pytr_version)
    pytr_version._check_version()  # pylint: disable=W0212

    base_packages = parse_requirements_file("requirements.txt")
    docs_packages = parse_requirements_file("requirements-dev.txt")
    viz_packages = parse_requirements_file("requirements-viz.txt")

    setuptools.setup(
        name="pytextrank",
        version = pytr_version.__version__,

        python_requires = ">=" + pytr_version._versify(pytr_version.MIN_PY_VERSION),  # pylint: disable=W0212
        packages = setuptools.find_packages(exclude=[ "docs", "examples" ]),
        install_requires = base_packages,
        extras_require = {
            "base": base_packages,
            "docs": docs_packages,
            "viz": viz_packages,
            },

        author="Paco Nathan",
        author_email="paco@derwen.ai",
        license="MIT",

        description="Python implementation of TextRank as a spaCy pipeline extension, for graph-based natural language work plus related knowledge graph practices; used for for phrase extraction and lightweight extractive summarization of text documents.",
        long_description = pathlib.Path("README.md").read_text(),
        long_description_content_type = "text/markdown",

        keywords = ", ".join(KEYWORDS),
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Human Machine Interfaces",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Text Processing :: General",
            "Topic :: Text Processing :: Indexing",
            "Topic :: Text Processing :: Linguistic",
            ],

        url = "https://derwen.ai/docs/ptr/",
        project_urls = {
            "Source": "http://github.com/DerwenAI/pytextrank",
            "spaCy uniVerse": "https://spacy.io/universe/project/spacy-pytextrank",
            "Issue Tracker": "https://github.com/DerwenAI/pytextrank/issues",
            "Discussion Forum": "https://www.linkedin.com/groups/6725785/",
            "StackOverflow": "https://stackoverflow.com/search?q=pytextrank",
            "Citations": "https://scholar.google.com/scholar?q=related:5tl6J4xZlCIJ:scholar.google.com/&scioq=&hl=en&as_sdt=0,5",
            },

        zip_safe=False,
        )
