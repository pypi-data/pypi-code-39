"""
Workspace connection for dask-yarn

Dask-yarn does not really benefit from any sql magics. It's included here
due to being a common analytic pattern for distributed analytics using 
yarn.
"""

#import pandas as pd
#from dsws.util import pretty
#from dsws.util import sp
#from dsws.util import standard_sess_qry
#from os import environ as env
#import re
#from ast import literal_eval

from dask_yarn import YarnCluster
from dask.distributed import Client

class Daskyarn:
    def __init__(self,kwargs,command=None):
        self.conf=kwargs
        self._cluster = None
        self._client = None


    def init(self):
        if self._client is None:
            self._client = Client(YarnCluster(**self.conf))
        return(self._client)