#!/usr/bin/env python

# Usage:
#   del dist\*.*
#   python setup.py sdist bdist_wheel
#   python -m twine upload --repository testpypi dist/*

import setuptools
from distutils.core import setup
#from distutils.command.sdist import sdist as _sdist
from scidatacontainer.container import MODELVERSION
#import pandoc

#class sdistzip(_sdist):
#    def initialize_options(self):
#        _sdist.initialize_options(self)
#        self.formats = "gztar,zip"

#text = pandoc.read(file="README.md", format="markdown")
#pandoc.write(text, file="README.rst", format="rst")
#pandoc.write(text, file="README.txt", format="plain")
with open("README.md", "r") as fp:
    readme = fp.read()

setup(name="SciDataContainer",
      version=MODELVERSION,
      description="A container class for the storage of scientific data together with meta data",
      long_description=readme,
      long_description_content_type='text/markdown',
      author="Reinhard Caspary",
      author_email="reinhard.caspary@phoenixd.uni-hannover.de",
      url="https://github.com/reincas/scidatacontainer",
      packages=["scidatacontainer"],
      keywords=["Research Data Management", "Data Container", "Meta Data"],
      license="GNU Lesser General Public License (LGPL)",
      #cmdclass={'sdist': sdistzip},
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Operating System :: OS Independent",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering"],
      )

