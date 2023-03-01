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
from scidatacontainer import Container, register_mimetype, register_suffix
from scidatacontainer.fileimage import PngFile

# Register data conversion class for png files
register_mimetype("image/png", PngFile)
register_suffix("png", "image/png")

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
print(dc)

# Store container as local file
dc.hash()
dc.write("image.zdc")

# Read container from local file
dc = Container(file="image.zdc")
print(dc)

# Upload container to server
dc.upload()
print("--- Container uploaded.")

# Download container from server
uuid = dc["content.json"]["uuid"]
#uuid = "cb9e0243-401f-42d2-a59c-bda58d89f527"
dc = Container(uuid=uuid)
print("--- Container downloaded.")
print(dc)

### Double upload test: This must fail!
##dc.upload()
##print("--- Container uploaded twice *** ERROR ***.")
