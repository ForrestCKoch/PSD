#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='psdPy',
      version='0.1.0',
      description='Python implementation of scPSD',
      author='Forrest Koch',
      author_email='forrest.c.koch@gmail.com', #url='https://www.python.org/sigs/distutils-sig/',#packages=['distutils', 'distutils.command'],
      packages=find_packages(),
      install_requires=[
         'numpy>=1.21.0',
         'scipy>=1.7.0'
      ]
     )
