import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytextrank",
    version="2.0.0",
    description="Python implementation of TextRank for phrase extraction and summarization of text documents",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="textrank, parsing, extractive summarization, natural language processing, nlp, knowledge graph, graph algorithms, text analytics",
    url="http://github.com/DerwenAI/pytextrank",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
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
    author="Paco Xander Nathan",
    author_email="ceteri@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[
          "graphviz",
          "networkx",
          "spacy",
    ],
    python_requires=">=3.0",
    zip_safe=False,
)
