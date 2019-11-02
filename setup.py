from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pytextrank',
      version='2.0.0',
      description='Python implementation of TextRank for text document NLP parsing and summarization',
      long_description=readme(),
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='textrank, parsing, extractive summarization, natural language processing, nlp, knowledge graph, graph algorithms, text analytics',
      url='http://github.com/DerwenAI/pytextrank',
      author='Paco Xander Nathan',
      author_email='ceteri@gmail.com',
      license='MIT',
      packages=['pytextrank'],
      install_requires=[
          'datasketch',
          'graphviz',
          'networkx',
          'spacy',
          'statistics',
      ],
      zip_safe=False)
