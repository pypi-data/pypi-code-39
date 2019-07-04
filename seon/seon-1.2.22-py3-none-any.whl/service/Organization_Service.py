from .Service_Abstract import Service_Abstract

class Organization_Service(Service_Abstract):

    def __init__(self):
        Service_Abstract.__init__(self,'organizations')

    
    def save (self, name, description):

        data = {'name': name, 
                'description': description
                }
        
        print (data)

        response = self.request_x.post(data,self.host+self.url)
        
        if response.status_code == 404:
            
            raise Exception('URL', 'NotFound')
        
        return response.json()