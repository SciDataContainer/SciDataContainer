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
import time
import requests
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


##########################################################################
# Single-step container tests
##########################################################################
print(40*"-")
if servertest:
    print("Single-Step Container Tests")
else:
    print("Single-Step Container Tests (no server)")
print(40*"-")
print()

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

# Double server upload must fail
if servertest:
    cnt += 1
    print("*** Test %d: Upload container to server again" % cnt)
    try:
        dc.upload()
        raise RuntimeError("Double server upload was possible!")
    except requests.exceptions.HTTPError:
        pass
    print("Second upload failed as intended.")
    print()


##########################################################################
# Multi-Step container tests
##########################################################################
print(40*"-")
if servertest:
    print("Multi-Step Container Tests")
else:
    print("Multi-Step Container Tests (no server)")
print(40*"-")
print()

# Create a multi-step container
cnt += 1
print("*** Test %d: Create multi-step container" % cnt)
items = {
    "content.json": {
        "containerType": {"name": "myMultiImage"},
        "complete": False,
        },
    "meta.json": {
        "title": "Multi-step image datatset",
        },
    "data/parameter.json": parameter,
    "meas/image_1.png": img,
    }
dc = Container(items=items)
print(dc)
print()

# Write and read multi-step container
cnt += 1
print("*** Test %d: Local file storage of multi-step container" % cnt)
dc.write("image_multi.zdc")
dc = Container(file="image_multi.zdc")
print("Writing and reading succesful.")
print()

# Upload multi-step container
if servertest:
    cnt += 1
    print("*** Test %d: Upload multi-step container" % cnt)
    dc.upload()
    uuid = dc["content.json"]["uuid"]
    print("Upload sucessful: %s" % uuid)
    print()

# Update multi-step container
if servertest:
    cnt += 1
    print("*** Test %d: Update multi-step container after 2 seconds" % cnt)
    time.sleep(2)
    dc = Container(uuid=uuid)
    dc["meas/image_2.png"] = img
    dc.upload()
    uuid = dc["content.json"]["uuid"]
    print("Upload sucessful: %s" % uuid)
    print()

# Update and finalize multi-step container
if servertest:
    cnt += 1
    print("*** Test %d: Finalize multi-step container after 2 seconds" % cnt)
    time.sleep(2)
    dc = Container(uuid=uuid)
    dc["meas/image_3.png"] = img
    dc["content.json"]["complete"] = True
    dc.upload()
    uuid = dc["content.json"]["uuid"]
    print(dc)
    print("Upload sucessful: %s" % uuid)
    print()

# Next server upload must fail
if servertest:
    cnt += 1
    print("*** Test %d: Upload container to server again" % cnt)
    try:
        dc.upload()
        raise RuntimeError("Double server upload was possible!")
    except requests.exceptions.HTTPError:
        pass
    print("Second upload failed as intended.")
    print()


##########################################################################
# Static container tests
##########################################################################
print(40*"-")
if servertest:
    print("Static Container Tests")
else:
    print("Static Container Tests (no server)")
print(40*"-")
print()

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
    print("*** Test %d: Create same static container with new id" % cnt)
    dc = Container(items=items)
    dc.freeze()
    print(dc)
    print()

# Upload new static container
if servertest:
    cnt += 1
    print("*** Test %d: Upload static container" % cnt)
    uuid1 = dc["content.json"]["uuid"]
    dc.upload()
    uuid2 = dc["content.json"]["uuid"]
    if uuid2 == uuid1 or uuid2 != uuid:
        raise RuntimeError("Replacement of multiple static container failed!")
    print("  current:  %s" % uuid1)
    print("  replaced: %s" % uuid2)
    print("Container successfully replaced by server data.")
    print()

# Convert static to single-step container
cnt += 1
print("*** Test %d: Convert static to fresh single-step container" % cnt)
dc.release()
dc["sim/test.txt"] = "hello"
if "sim/test.txt" not in dc:
    raise RuntimeError("Adding an item failed!")
print(dc)
print()


##########################################################################
# Done
##########################################################################

print(40*"-")
if servertest:
    print("All tests finished successfully")
else:
    print("All tests finished successfully (no server)")
print(40*"-")
