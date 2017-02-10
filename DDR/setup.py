from setuptools import setup

setup(name='ddr',
      version='0.1',
      description='Functions for implementing and exploring Distributed Dictionary Representation',
      author='Joe Hoover',
      author_email='jehoover@usc.edu',
      license='USC',
      packages=['ddr'],
      package_data = {'ddr': ['*.pdf', '*.txt']},
      zip_safe=False)

