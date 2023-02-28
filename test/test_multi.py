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
# Testing the multi-step dataset.
#
##########################################################################

import time
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
        "containerType": {"name": "myMultiImage"},
        "complete": False,  # <- multi-step!
        },
    "meta.json": {
        "title": "This is a sample multi-image dataset",
        },
    "meas/image_1.png": img,
    "data/parameter.json": parameter,
    }

# Step 1. Generate and store dataset with one image
dc = Container(items=items)
dc.write("image_multi.zdc")
print(dc)

### Upload container to server
##dc.upload()
##print("--- Container uploaded.")

# Step 2: Load step 1 dataset, add a second image and store it
time.sleep(3)
dc = Container(file="image_multi.zdc") # <- Read dataset and keep the UUID
dc["meas/image_2.png"] = img
dc.write("image_multi.zdc")
print(dc)

### Upload container to server
##dc.upload()
##print("--- Container uploaded.")

# Step 3: Load step 2 dataset, add a third image, close the dataset
time.sleep(3)
dc = Container(file="image_multi.zdc") # <- Read dataset and keep the UUID
dc["meas/image_3.png"] = img
dc["content.json"]["complete"] = True # <- final version of this dataset
dc.hash() # <- Add a SHA256 has (optional)
dc.write("image_multi.zdc")
print(dc)

### Upload container to server
##dc.upload()
##print("--- Container uploaded.")
##
### Download container from server
##uuid = dc["content.json"]["uuid"]
##dc = Container(uuid=uuid)
##print("--- Container downloaded.")
##print(dc)
