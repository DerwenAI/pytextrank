import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytextrank",
    version="2.0.2",
    author="Paco Xander Nathan",
    author_email="paco@derwen.ai",
    description="Python implementation of TextRank for phrase extraction and summarization of text documents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/DerwenAI/pytextrank",
    packages=setuptools.find_packages(),
    classifiers=[
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
    python_requires=">=3.5",
    install_requires=[
          "coverage",
          "graphviz",
          "networkx",
          "spacy",
    ],
    keywords="textrank, spacy, phrase extraction, parsing, extractive summarization, natural language processing, nlp, knowledge graph, graph algorithms, text analytics",
    license="MIT",
    zip_safe=False,
)
