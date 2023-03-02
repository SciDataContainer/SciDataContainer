#!/usr/bin/env python

import re
import setuptools  # required for command bdist_wheel
from distutils.core import setup

pkg = "scidatacontainer"
version = None
with open(pkg + "/container.py", "r") as fp:
    for line in fp.readlines():
        if line[:15] == "MODELVERSION = ":
            version = eval(line[15:].split()[0].strip())
            break
    else:
        raise RuntimeError("MODELVERSION missing in container.py!")

with open("version.txt", "w") as fp:
    fp.write(version)
    
with open("README.md", "r") as fp:
    readme = fp.read()

setup(name="SciDataContainer",
      version=version,
      description="A container class for the storage of scientific data together with meta data",
      long_description=readme,
      long_description_content_type='text/markdown',
      author="Reinhard Caspary",
      author_email="reinhard.caspary@phoenixd.uni-hannover.de",
      url="https://github.com/reincas/scidatacontainer",
      packages=[pkg],
      keywords=["Research Data Management", "Data Container", "Meta Data"],
      license="GNU Lesser General Public License (LGPL)",
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Operating System :: OS Independent",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering"],
      install_requires=["requests"],
      )

