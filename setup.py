#!/usr/bin/env python

import setuptools
from distutils.core import setup
from scidatacontainer.container import MODELVERSION
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
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Operating System :: OS Independent",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering"],
      )

