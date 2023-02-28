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
# This module provides the function getconfig() to read the default
# configuration parameters
#
# Parameter    | key
# -------------+--------
# author name  | author
# author email | email
# server URL   | server
# server key   | key
#
# The values of these parameters are taken either from environment
# variables or a config file. Both options are optional. Data from the
# config file overides the environment variables.
#
# The name of the environment variable of key foo is DC_FOO.
#
# The name of the config file is "$HOME\scidata.cfg" (Windows) or
# "~/.scidata" (other OS). It is expected to be a text file. Leading and
# trailing white space is ignored. Lines starting with "#" are ignored.
# The parameters are taken from lines in the form "<key> = <value>".
# Optional white space before and after the equal sign is ignored. The
# keywords are case-insensitive.
#
##########################################################################

import os
import platform


def load_config():

    """ Get config data from environment variables and config file. """

    # Initialize config dictionary
    config = {"author": "", "email": "", "server": "", "key": ""}

    # Get default values from environment variables
    for key in config:
        name = "DC_%s" % key.upper()
        if name in os.environ:
            config[key] = os.environ[name]
            
    # Get default values from config file
    if platform.system() == "Windows":
        conf = os.path.join(os.path.expanduser("~"), "scidata.cfg")
    else:
        conf = os.path.join(os.path.expanduser("~"), ".scidata")
    if os.path.exists(conf):
        with open(conf, "r") as fp:
            for line in fp.readlines():
                line = line.strip()
                if line[:1] == "#":
                    continue
                line = line.split("=", 1)
                if len(line) < 2:
                    continue
                key = line[0].strip().lower()
                if key in config:
                    config[key] = line[1].strip()

    # Return config dictionary
    return config

