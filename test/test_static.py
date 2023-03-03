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
# Testing the static dataset.
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
        "width": 2064,
    },
    "dummy": 9,
}

# Create the scientific data container
items = {
    "content.json": {
        "containerType": {"name": "myImgParam"},
        },
    "meta.json": {
        "title": "Static image parameter datatset",
        },
    "data/parameter.json": parameter,
    }
dc = Container(items=items)
dc["sim/test.txt"] = "hello"
dc.freeze() # <- This makes the dataset static and immutable
print(dc)
dc.release()
dc["sim/test.txt"] = "hello"
print(dc)

# Store container as local file
del dc["sim/test.txt"]
dc.write("image_static.zdc")
print("content.json" in dc)

### Upload container to server
##dc.upload()
##print("Container uploaded.")
##
### Download container from server
##uuid = dc["content.json"]["uuid"]
##dc = Container(uuid=uuid)
##print("Container downloaded.")
##print(dc)
