#!/usr/bin/env python

from distutils.core import setup
from distutils.command.sdist import sdist as _sdist
from scidatacontainer.container import MODELVERSION
import pandoc

class sdistzip(_sdist):
    def initialize_options(self):
        _sdist.initialize_options(self)
        self.formats = "gztar,zip"

text = pandoc.read(file="README.md", format="markdown")
pandoc.write(text, file="README.rst", format="rst")
pandoc.write(text, file="README.txt", format="plain")

setup(name="SciDataContainer",
      version=MODELVERSION,
      description="Scientific Data Container",
      author="Reinhard Caspary",
      author_email="reinhard.caspary@phoenixd.uni-hannover.de",
      url="https://github.com/reincas/scidatacontainer",
      packages=["scidatacontainer"],
      keywords=["Research Data Management", "Data Container", "Meta Data"],
      license="LGPL v3",
      cmdclass={'sdist': sdistzip},
     )

