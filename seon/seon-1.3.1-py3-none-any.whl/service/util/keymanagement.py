from requestx.RequestX import RequestX
class Key_Management_Service():

    def __init__(self):
        self.host = "http://localhost:8081/"
        self.url = "toolkeys"
        self.request_x = RequestX()
    
    def save (self, organization_id, tool,secret,url):

        data = {'organization_id': organization_id, 
                'tool': tool, 
                'secret': secret,
                'url': url}
        
        return self.request_x.post(data,self.host+self.url)