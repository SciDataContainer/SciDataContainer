##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
##########################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##########################################################################
#
# Testing the normal single-step dataset.
#
##########################################################################

import cv2 as cv
from scidatacontainer import Container

# Set to True for testing the server connection
servertest = False

# Dummy data: an image
img = cv.imread("image.png")
img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Dummy parameters: a dict
parameter = {
    "acquisition": {
        "acquisitionMode": "SingleFrame",
        "exposureAuto": "Off",
        "exposureMode": "Timed",
        "exposureTime": 19605.0,
        "gain": 0.0,
        "gainAuto": "Off",
        "gainMode": "Default",
        "gainSelector": "AnalogAll"
    },
    "device": {
        "family": "mvBlueFOX3",
        "id": 0,
        "product": "mvBlueFOX3-2032aG",
        "serial": "FF008343"
    },
    "format": {
        "height": 1544,
        "offsetX": 0,
        "offsetY": 0,
        "width": 2064
    }
}

# Create the scientific data container
print("*** Test 1: Create container with hash")
items = {
    "content.json": {
        "containerType": {"name": "myImage"},
        },
    "meta.json": {
        "title": "This is a sample image dataset",
        },
    "meas/image.png": img,
    "data/parameter.json": parameter,
    }
dc = Container(items=items)
dc.hash()
print(dc)
print()

# Store container as local file
print("*** Test 2: Write local container file")
fn = "image.zdc"
dc.write(fn)
print("File: '%s'" % fn)
print()

# Read container from local file
print("*** Test 3: Read local container file")
dc = Container(file=fn)
print(dc)
print()

# Upload container to server
if servertest:
    print("*** Test 4: Upload container to server")
    try:
        dc.upload()
        uuid = dc["content.json"]["uuid"]
        print("Upload sucessful: %s" % uuid)
    except ConnectionError:
        print("Server connection failed - skipping server tests.")
        servertest = False
    print()

# Download container from server
if servertest:
    print("*** Test 5: Upload container to server")
    dc = Container(uuid=uuid)
    print(dc)
    print()

print("*** Test 6: New file format")
import io
import numpy as np
from scidatacontainer import FileBase, register

class NpyFile(FileBase):
    allow_pickle = False
    def encode(self):
        with io.BytesIO() as fp:
            np.save(fp, self.data, allow_pickle=self.allow_pickle)
            fp.seek(0)
            data = fp.read()
        return data
    def decode(self, data):
        with io.BytesIO() as fp:
            fp.write(data)
            fp.seek(0)
            self.data = np.load(fp, allow_pickle=self.allow_pickle)

register("npy", NpyFile, np.ndarray)

data = np.random.rand(7,5)

items = {
    "content.json": {
        "containerType": {"name": "myTest"},
        },
    "meta.json": {
        "title": "This is a sample test dataset",
        },
    "sim/random.apy": data,
    "data/parameter.json": parameter,
    }
dc = Container(items=items)
print(dc)
print(dc["sim/random.apy"])
dc.write("random.zdc")
dc = Container(file="random.zdc")
print(dc["sim/random.apy"])
print()
print(dc._classes)
