##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# This package provides the Scientific Data Container as class Container
# which may be stored as a ZIP package containing items (files). Based
# on their file extension, the following item types are supported:
#
# .bin:  Raw binary data file
# .txt:  Encoded text file (default encoding: UTF-8)
# .log:  Encoded text file (default encoding: UTF-8)
# .pgm:  Encoded text file (default encoding: UTF-8)
# .json: JSON file
# .png:  PNG image (requires Python module cv2)
#
# Users may register other file extensions to file conversion classes
# using the function register(). See package fileimage as an example for
# such a conversion class.
#
##########################################################################

import importlib
from .filebase import FileBase, TextFile, JsonFile
from .container import DataContainer, timestamp
from .container import MODELVERSION as version

suffixes = {
    "json": JsonFile,
    "bin": FileBase,
    "txt": TextFile,
    "log": TextFile,
    "pgm": TextFile,
    }

classes = {
    dict: JsonFile,
    str: TextFile,
    bytes: FileBase,
    }

formats = [
    TextFile,
    ]

import sys
if __name__ in sys.modules:
    print(__name__, "Hit!")
else:
    print(__name__, "failed")

for name in (".filenumpy", ".fileimage"):
    print(name)
    if importlib.util.find_spec(name, __name__) is None:
        print(name, "failed.")
        continue
    module = importlib.import_module(name, __name__)
    print(module.suffixes)

    
# Try to import array file formats requiring the Python module numpy
NpyFile = None
try:
    from .filenumpy import NpyFile
except:
    pass
if NpyFile is not None:
    suffixes["npy"] = NpyFile
    #classes[
    formats.append(NpyFile)


# Try to import image file formats requiring the Python module cv2
try:
    from .fileimage import PngFile
    suffixes["png"] = PngFile
    formats.append(PngFile)
except:
    pass


def register(suffix, fclass, pclass=None):

    """ Register a suffix to a conversion class. If the parameter class
    is a string, it is interpreted as known suffix and the conversion
    class of this suffix is registered also for the new one. """

    # Suffix json is immutable
    if suffix == "json":
        raise RuntimeError("Suffix 'json' is immutable!")

    # Take conversion class from a known suffix
    if pclass is None:
        if not isinstance(fclass, str):
            raise RuntimeError("Python class missing for suffix '%s'!" % suffix)
        if fclass not in suffixes:
            raise RuntimeError("Unknown suffix '%s'!" % fclass)

        # Register suffix
        suffixes[suffix] = suffixes[fclass]
        
    # Simple sanity check for the class interface
    else:
        for method in ("encode", "decode", "hash"):
            if not hasattr(fclass, method) or not callable(getattr(fclass, method)):
                raise RuntimeError("No method %s() in class for suffix '%s'!" \
                                   % (method, suffix))

        # Register unknown file format
        if fclass not in formats:
            formats.append(fclass)

        # Register Python class. Last registration becomes default.
        # Overriding the mapping dict:JsonFile is not allowed.
        if not pclass is dict:
            classes[pclass] = fclass

        # Register suffix
        suffixes[suffix] = fclass


# Inject certain known file formats into the container class
class Container(DataContainer):

    """ Scientific data container. """

    _suffixes = suffixes
    _classes = classes
    _formats = formats
