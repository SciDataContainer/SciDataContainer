##########################################################################
# Copyright (c) 2023 Reinhard Caspary                                    #
# <reinhard.caspary@phoenixd.uni-hannover.de>                            #
# This program is free software under the terms of the MIT license.      #
##########################################################################
#
# Testing the Container class of scidatacontainer.
#
##########################################################################

import random
import cv2 as cv
from scidatacontainer import Container

# Set to True for testing the server connection
servertest = True

# Test counter
cnt = 0

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
cnt += 1
print("*** Test %d: Create container with hash" % cnt)
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
cnt += 1
print("*** Test %d: Write local container file" % cnt)
fn = "image.zdc"
dc.write(fn)
print("File: '%s'" % fn)
print()

# Read container from local file
cnt += 1
print("*** Test %d: Read local container file" % cnt)
dc = Container(file=fn)
print(dc)
print()

# Upload container to server
if servertest:
    cnt += 1
    print("*** Test %d: Upload container to server" % cnt)
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
    cnt += 1
    print("*** Test %d: Download container from server" % cnt)
    dc = Container(uuid=uuid)
    print(dc)
    print()

### Double server upload must fail
##cnt += 1
##print("*** Test %d: Upload container to server again" % cnt)
##dc.upload()
##try:
##    dc.upload()
##    uuid = dc["content.json"]["uuid"]
##    print("Upload sucessful: %s" % uuid)
##except ConnectionError:
##    print("Repeated upload was denied as expected.")

# Create a static container
cnt += 1
print("*** Test %d: Create static container" % cnt)
items = {
    "content.json": {
        "containerType": {"name": "myImgParam"},
        },
    "meta.json": {
        "title": "Static image parameter datatset",
        },
    "data/parameter.json": parameter,
    "data/random.json": random.random(),
    }
dc = Container(items=items)
dc.freeze()
print(dc)
try:
    dc["sim/test.txt"] = "hello"
    raise RuntimeError("Modification of static container was possible!")
except:
    pass
print("Modification of static container failed as intended.")
print()

# Upload static container
if servertest:
    cnt += 1
    print("*** Test %d: Upload static container" % cnt)
    dc.upload()
    uuid = dc["content.json"]["uuid"]
    print("Upload sucessful: %s" % uuid)
    print()

# Create same static container
if servertest:
    cnt += 1
    print("*** Test %d: Create same static container again" % cnt)
    dc = Container(items=items)
    dc.freeze()
    print(dc)

# Upload static container
if servertest:
    cnt += 1
    print("*** Test %d: Upload static container" % cnt)
    dc.upload()
    uuid = dc["content.json"]["uuid"]
    print("Upload sucessful: %s" % uuid)
    print()


# Done
print("*** Tests finished.")
