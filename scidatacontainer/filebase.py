##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# This module provides the base data conversion class FileBase and
# standard text conversion classes. All data conversion classes should
# inherit from FileBase and must provide three methods:
#
# encode(): Return data encoded as bytes string.
# decode(data): Decode and store given bytes string data.
# hash(): Return SHA256 hash from data as hex string.
#
# The hash implementation shoud make sure that semantically equivalent
# data results in the same hash.
#
##########################################################################

import hashlib
import json


##########################################################################
# Data conversion classes

class FileBase(object):

    """ Basic class for bytes data. """

    def __init__(self, data):

        """ Store data. """

        if isinstance(data, bytes):
            self.decode(data)
        else:
            self.data = data

    def hash(self):

        """ Return hex digest of SHA256 hash. """

        return hashlib.sha256(self.encode()).hexdigest()

    def encode(self):

        """ Return encoded data as bytes string. """

        return self.data

    def decode(self, data):

        """ Decode and store data from bytes string. """

        self.data = data


class TextFile(FileBase):

    """ Data conversion class for a text file. """

    charset = "utf8"

    def encode(self):

        """ Encode text to bytes string. """

        return bytes(self.data, self.charset)

    def decode(self, data):

        """ Decode text from given bytes string. """

        self.data = data.decode(self.charset)
        

class JsonFile(FileBase):

    """ Data conversion class for a JSON file represented as Python
    dictionary. """

    indent = 4
    charset = "utf8"

    def sortit(self, data):

        """ Return compact string representation with keys of all
        sub-dictionaries sorted. """

        if isinstance(data, dict):
            keys = sorted(data.keys())
            data = [k + ": " + self.sortit(data[k]) for k in keys]
            data = ", ".join(data)
            data = "{" + data + "}"
            return data
        elif isinstance(data, (list, tuple)):
            data = [self.sortit(v) for v in data]
            data = ", ".join(data)
            data = "[" + data + "]"
            return data
        return repr(data)

    def hash(self):

        """ Return hex digest of the SHA256 hash calculated from the
        sorted compact representation. This should result in the same
        hash for semantically equal data dictionaries. """

        data = bytes(self.sortit(self.data), self.charset)
        return hashlib.sha256(data).hexdigest()

    def encode(self):

        """ Convert dictionary to pretty string representation with
        indentation and return it as bytes string. """

        data = json.dumps(self.data, sort_keys=True, indent=self.indent)
        return bytes(data, self.charset)

    def decode(self, data):

        """ Decode dictionary from given bytes string. """

        self.data = json.loads(data.decode(self.charset))


register = [
    ("bin", FileBase, bytes),
    ("json", JsonFile, dict),
    ("txt", TextFile, str),
    ("log", TextFile, None),
    ("pgm", "txt", None),
    ]
    
