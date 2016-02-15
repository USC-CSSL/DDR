from setuptools import setup

setup(name='addr',
      version='0.1',
      description='Functions for implementing Aggregate Distributed Dictionary Representation',
      #url='',
      author='Joe Hoover',
      author_email='jehoover@usc.edu',
      license='USC',
      packages=['addr'],
      install_requires=[
          'numpy',
          'scipy',
          'scikit-learn',
          'pandas',
          'gensim'
      ],
      package_data = {'addr': ['*.pdf', '*.txt']},
      zip_safe=False)

