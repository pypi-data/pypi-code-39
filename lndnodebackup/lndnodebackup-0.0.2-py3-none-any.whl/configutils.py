'''
   Copyright 2019 nolim1t.co

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

import os
import toml
from os.path import expanduser
from pathlib import Path


def homedirectory():
    return expanduser("~")

def configdirectory():
    return homedirectory() + '/.lncm'

def configfile():
    return configdirectory() + '/nodebackup.toml'

def pathExists(thepath):
    return Path(thepath).exists()

def isDirectory(thepath):
    return (Path(thepath).is_dir() and Path(thepath).exists())

def canAccessForWriting(thepath):
    return os.access(os.path.dirname(os.path.realpath(thepath)), os.W_OK)

def canAccessForReading(thepath):
    return os.access(os.path.dirname(os.path.realpath(thepath)), os.R_OK)

def canAccessConfigFile():
    return canAccessForReading(configfile())

def readconfig():
    if not isDirectory(configdirectory()):
        print("Directory .lncm doesn't exist")
        return False

    # Check if config file exists
    if not canAccessConfigFile():
        print("Config file can not be accessed")
        return False


    try:
        return toml.load(configfile(), _dict=dict)
    except:
        exception = sys.exc_info()[0]
        print("Failed to load config (%s)" % exception)
        return False
    return True

if __name__ == "__main__":
    print("This file is not meant to be run directly")