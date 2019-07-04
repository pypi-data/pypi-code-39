from requestx.RequestX import RequestX
from pprint import pprint
import json
from collections import namedtuple
from urllib.error import HTTPError

class Service_Abstract (object):

    def __init__(self, url = None):
        self.host = 'https://enterprise-ontology-service.azurewebsites.net/'
        self.url = url
        self.request_x = RequestX()

    def exists(self, id_tool):
        
        try:

            self.get_by_id_tool(id_tool)
        
            return True
        
        except Exception:
            return False

    def get_by_id_tool(self, id_tool):
        url = self.host+self.url+'/search/findByIdtool?idtool='+id_tool
        
        response = self.request_x.get(url)
        
        if response.status_code == 404:
            
            raise Exception('URL', 'NotFound')
        
        return response.json()
        
        
    def connect(self, target_url, from_url):
        return self.request_x.put_uri_list(target_url, from_url).json()
    
    def update (self, url, data):
        return self.request_x.patch(data, url).json()

    