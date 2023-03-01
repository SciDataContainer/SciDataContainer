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
# This module provides the Scientific Data Container as class
# DataContainer which may be stored or uploaded as a ZIP package
# containing items (files). Do not use this class directly! Use the
# class Container provided by the package scidatacontainer instead.
#
##########################################################################

import copy
import hashlib
import io
import json
import requests
import time
import uuid
from zipfile import ZipFile
import cv2 as cv
import numpy as np

from .filebase import FileBase, JsonFile
from .config import load_config
config = load_config()


# Version of the implemented data model
MODELVERSION = "0.3.3"


##########################################################################
# Timestamp function

def timestamp():

    """ Timestamp function. """

    return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(time.time()))


##########################################################################
# Data container class

class DataContainer(object):

    """ Scientific data container with minimal file support. """

    _config = config
    _suffixes = {"json": "application/json"}
    _mimetypes = {"application/json": JsonFile}


    def __init__(self, items=None, file=None, uuid=None, server=None, key=None):

        # Store all items in the container
        if items is not None:
            self.store(items)

        # Load local container file
        elif file is not None:
            self.read(fn=file)

        # Download container from server
        elif uuid is not None:
            self.download(uuid=uuid, server=server, key=key)

        # No data source
        else:
            raise RuntimeError("No data!")


    def store(self, items, strict=True):

        """ Store all items in the container. """

        # Add all items in the container
        self._items = {}
        self.static = False
        for path, data in items.items():
            self[path] = data

        # Make sure that the items content.json and meta.json exist and
        # contain all required attributes
        self.validate_content()
        self.validate_meta()

        # Check validity of hash
        if strict and self["content.json"]["hash"]:
            oldhash = self["content.json"]["hash"]
            self.hash()
            if self["content.json"]["hash"] != oldhash:
                raise RuntimeError("Wrong hash!")

        # Set static flag
        self.static = self["content.json"]["static"]


    def __contains__(self, path):

        """ Return true, if the given path matches an item in this
        container. """

        return path in self._items
    
        
    def __setitem__(self, path, data):

        """ Store data as a container item. """

        # Static container must not be modified
        if self.static:
            raise RuntimeError("Static container!")
        
        # Get file extension, default is FileBase
        ext = path.rsplit(".", 1)[1]
        if not ext in self._suffixes:
            print("*** Warning: Using FileBase class for unknown suffix '%s'! ***" % ext)
            cls = FileBase
            #raise RuntimeError("Unknown file extension '%s'!" % ext)
        else:
            cls = self._mimetypes[self._suffixes[ext]]

        # Initialize conversion object according to the file extension
        self._items[path] = cls(data)


    def __getitem__(self, path):

        """ Get the data content of a container item. """

        if path in self:
            return self._items[path].data
        raise KeyError("Unknown item '%s'!" % path)


    def validate_content(self):

        """ Make sure that the item "content.json" exists and contains
        all required attributes. """
        
        # Item content.json is required
        if "content.json" not in self:
            raise RuntimeError("Item 'content.json' is missing!")
        content = self["content.json"]

        # Keep UUID of a multi-step container and create a new one otherwise
        if "uuid" not in content or not content["uuid"]:
            content["uuid"] = str(uuid.uuid4())

        # The optional attribute 'replace' contains the UUID of the
        # predecessor of this container. It replaces the former one,
        # which must have the same containerType and owner and a smaller
        # or equal creation time. The replacement feature should only be
        # used for minor data modifications (e.g. additional keywords or
        # comment in meta.json). The server returns always the latest
        # version.
        if "replaces" not in content:
            content["replaces"] = None

        # The attribute 'containerType' is a dictionary which must at
        # least contain the type of the container as short string
        # without spaces. If the container type is standardized, it must
        # also contain a type id and a version string.
        if "containerType" not in content:
            raise RuntimeError("Attribute 'containerType' is missing!")
        ptype = content["containerType"]
        if not isinstance(ptype, dict):
            raise RuntimeError("Attribute containerType is no dictionary!")
        if "name" not in ptype:
            raise RuntimeError("Name of containerType is missing!")
        if "id" in ptype and not "version" in ptype:
            raise RuntimeError("Version of containerType is missing!")

        # The boolean attribute 'static' is required. Default is False.
        if "static" in content:
            content["static"] = bool(content["static"])
        else:
            content["static"] = False

        # The boolean attribute 'complete' is required. Default is True.
        if not content["static"] and "complete" in content:
            content["complete"] = bool(content["complete"])
        else:
            content["complete"] = True

        # Current time
        ts = timestamp()

        # The attribute 'created' is required. It is created
        # automatically for a new dataset.
        if "created" not in content or not content["created"]:
            content["created"] = ts

        # The attribute 'modified' is updated automatically for a
        # multi-step dataset
        if "modified" not in content or not content["complete"]:
            content["modified"] = ts

        # The attribute 'hash' is optional
        if "hash" not in content or not content["hash"]:
            content["hash"] = None

        # The attribute 'usedSoftware' is a list of dictionaries, which
        # may be empty. Each dictionary must contain atleast the items
        # "name" and "version" specifying name and version of a
        # software. It may also contain the items "id" and "idType"
        # specifying a reference id (e.g. GitHub-URL) and its type.
        if "usedSoftware" not in content or not content["usedSoftware"]:
            content["usedSoftware"] = []
        for sw in content["usedSoftware"]:
            if not "name" in sw:
                raise RuntimeError("Software name is missing!")
            if not "version" in sw:
                raise RuntimeError("Software version is missing!")
            if "id" in sw and not "idType" in sw:
                raise RuntimeError("Type of software reference id is missing!")

        # Version of the data model provided by this package
        if "modelVersion" not in content:
            content["modelVersion"] = MODELVERSION
        

    def validate_meta(self):
        
        """ Make sure that the item "meta.json" exists and contains
        all required attributes. """

        # Item meta.json is required
        if "meta.json" not in self:
            raise RuntimeError("Item 'meta.json' is missing!")
        meta = self["meta.json"]

        # Author name is required
        if "author" not in meta:
            meta["author"] = self._config["author"]
        if not meta["author"]:
            raise RuntimeError("Author name is missing!")

        # Author email address is required
        if "email" not in meta:
            meta["email"] = self._config["email"]

        # Comment on dataset is required, but may be empty
        if "comment" not in meta:
            meta["comment"] = ""

        # Title of dataset is required
        if "title" not in meta:
            meta["title"] = ""
        if not meta["title"]:
            raise RuntimeError("Data title is missing!")

        # List of keywords is required, but may be empty
        if "keywords" not in meta:
            meta["keywords"] = []

        # Description of dataset is required, but may be empty
        if "description" not in meta:
            meta["description"] = ""


    def delpath(self, path):

        """ Delete the given item. """

        # Static container must not be modified
        if self.static:
            raise RuntimeError("Static container!")

        # Delete item        
        if path in self:
            del self._items[path]
            

    def paths(self):

        """ Return all container item paths. """

        return sorted(self._items.keys())


    def hash(self):

        """ Calculate hash value of this container. """

        # Some attributes of content.json are excluded from the hash
        # calculation
        save = ("uuid", "created", "modified")
        save = {k: self["content.json"][k] for k in save}
        for key in save:
            self["content.json"][key] = None
        self["content.json"]["hash"] = None

        # Calculate and store hash of this container
        hashes = [self._items[p].hash() for p in sorted(self.paths())]
        myhash = hashlib.sha256(" ".join(hashes).encode("ascii")).hexdigest()
        self["content.json"]["hash"] = myhash

        # Restore excluded attributes
        for key, value in save.items():
            self["content.json"][key] = value


    def freeze(self):

        """ Calculate the hash value of this container and make it
        static. The container cannot be modified any more when this
        method was called once. """

        self.hash()
        self["content.json"]["static"] = True
        self["content.json"]["complete"] = True


    def encode(self):

        """ Encode container as ZIP package. Return package as binary
        string. """

        items = {p: self._items[p].encode() for p in self.paths()}
        with io.BytesIO() as f:
            with ZipFile(f, "w") as fp:
                for path, value in items.items():
                    fp.writestr(path, value)
            f.seek(0)
            data = f.read()
        return data
    

    def decode(self, data, strict=True):

        """ Take ZIP package as binary string. Read items from the
        package and store them in this object. """
        
        with io.BytesIO() as f:
            f.write(data)
            with ZipFile(f, "r") as fp:
                items = {p: fp.read(p) for p in fp.namelist()}
        self.store(items, strict)

        
    def write(self, fn, data=None):

        """ Write the container to a ZIP package file. """

        if data is None:
            data = self.encode()
        with open(fn, "wb") as fp:
            fp.write(data)


    def read(self, fn, strict=True):

        """ Read a ZIP package file and store it as container in this
        object. """

        with open(fn, "rb") as fp:
            data = fp.read()
        self.decode(data, strict)


    def upload(self, data=None, server=None, key=None):

        if server is None:
            server = self._config["server"]
        if not server:
            raise RuntimeError("Server URL is missing!")
        
        if key is None:
            key = self._config["key"]
        if not key:
            raise RuntimeError("Server API key is missing!")

        if data is None:
            data = self.encode()
        response = requests.post(server + "/api/upload/",
                                 files={"uploadfile": data},
                                 headers={"Authorization": "Token " + key})
        response.raise_for_status()


    def download(self, uuid, strict=True, server=None, key=None):

        if server is None:
            server = self._config["server"]
        if not server:
            raise RuntimeError("Server URL is missing!")
        
        if key is None:
            key = self._config["key"]
        if not key:
            raise RuntimeError("Server API key is missing!")

        response = requests.get(server + "/api/download/uuid=" + uuid,
                                headers={"Authorization": "Token " + key})
        response.raise_for_status()
        assert response.ok, response.reason

        self.decode(response.content, strict)


    def __str__(self):

        content = self["content.json"]
        meta = self["meta.json"]

        if content["static"]:
            ctype = "Static Container"
        elif content["complete"]:
            if content["created"] == content["modified"]:
                ctype = "Single-Step Container"
            else:
                ctype = "Closed Multi-Step Container"
        else:
            ctype = "Open Multi-Step Container"

        s = [ctype]
        ptype = content["containerType"]
        name = ptype["name"]
        if "id" in ptype:
            name = "%s %s (%s)" % (name, ptype["version"], ptype["id"])
        s.append("  type:     " + name)
        s.append("  uuid:     " + content["uuid"])
        if content["replaces"]:
            s.append("  replaces: " + content["replaces"])
        if content["hash"]:
            s.append("  hash:     " + content["hash"])
        s.append("  created:  " + content["created"])
        if "Multi" in ctype:
            s.append("  modified: " + content["modified"])
        s.append("  author:   " + meta["author"])

        return "\n".join(s)        
