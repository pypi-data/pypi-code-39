from requestx.RequestX import RequestX
class Key_Management_Service():

    def __init__(self):
        self.host = "http://localhost:8091/"
        self.url = "toolkeys"
        self.request_x = RequestX()
    
    def save (self, organization_id, tool,secret,url):

        data = {'organization_id': organization_id, 
                'tool': tool, 
                'secret': secret,
                'url': url}
        
        return self.request_x.post(data,self.host+self.url)
    
    def get_by_id (self, organization_id):
        
        url = self.host+self.url+'/search/findByOrganizationId?organizationId='+str(organization_id)
        
        response = self.request_x.get(url)
        
        if response.status_code == 404:
            
            raise Exception('URL', 'NotFound')
        
        return response