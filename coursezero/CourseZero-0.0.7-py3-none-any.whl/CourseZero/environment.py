"""
Created by 復讐者 on 7/11/19
"""
__author__ = '復讐者'


import os
import sys

############################ Locations  ############################
ROOT = os.getenv( "HOME" )

# The folder containing environment.py
PROJ_BASE = os.path.abspath(os.path.dirname(__file__))

DATA_FOLDER = "{}/data".format(PROJ_BASE)
STORAGE_FOLDER = "{}/storage".format(PROJ_BASE)

DEFAULT_CSU_ID_FILE = '{}//csu_ids.json'.format(DATA_FOLDER)

if __name__ == '__main__':
    pass