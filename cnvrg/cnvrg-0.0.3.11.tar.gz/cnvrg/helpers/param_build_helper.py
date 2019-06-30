import cnvrg.helpers.apis_helper as apis_helpers
import cnvrg.helpers.config_helper as config_helper
import os
## 1
ORGANIZATION = 'ORG'
## 2
PROJECT = 'PRO'
DATASET = 'DATA'
## 3
EXPERIMENT = 'EXP'
NOTEBOOK = 'NOTE'
ENDPOINT = 'ENDP'
## 4
TAG = 'TAG'
DEPLOYMENT = 'DEPL'


def type_to_depth(d_type):
    if d_type in [ORGANIZATION]: return 1
    if d_type in [PROJECT, DATASET]: return 2
    if d_type in [EXPERIMENT, NOTEBOOK, ENDPOINT]: return 3
    if d_type in [TAG, DEPLOYMENT]: return 4

def parse_params(params, type=None, working_dir=None):
    working_dir = working_dir or os.curdir
    num_of_params = len(params.split("/")) if params else 0
    splitted = params.split("/") if params else []
    if num_of_params == type_to_depth(type):
        return [*splitted]
    if num_of_params == type_to_depth(type) - 1:
        ## assuming logged in
        return [apis_helpers.credentials.owner, *splitted]
    if num_of_params == type_to_depth(type) - 2:
        ### assuming in project
        element = config_helper.get_element_slug(working_dir)
        owner = config_helper.get_element_owner(working_dir)
        return [owner, element, *splitted]
