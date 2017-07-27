DDR README
===================

This package implements the distributed dictionary representation (DDR) algorithm,
which allows users to estimate the loading of the documents in a corpus on a set of latent
constructs. For more details see: https://link.springer.com/article/10.3758/s13428-017-0875-9.


Installation Guidelines
---------------------------------

Currently, this package requires an installation of python 2.7+, as well as the following
dependencies:

* numpy
* pandas
* cython
* gensim==2.1.0


Guidelines for installing python and these dependencies can be found here: https://packaging.python.org/installing/

Users who are new to python, may find the Anaconda platform easier to work with. Installation
information can be found here: https://docs.continuum.io/anaconda/install.

To install DDR you can use the following steps:

1. Download this repository
2. Open a terminal session and navigate to the downloaded DDR directory that contains 'setup.py'.
3. Run:


    $ python setup.py install


After installing DDR, you can import the packages into a python environment and use it
as directed in the DDR-Introduction and DDR-Tutorial documentation.





