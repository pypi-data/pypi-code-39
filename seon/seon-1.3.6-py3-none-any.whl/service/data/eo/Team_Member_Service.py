from .Service_Abstract import Service_Abstract

class Team_Member_Service(Service_Abstract):

    def __init__(self):
        Service_Abstract.__init__(self,'teammembers')
    
    def save (self, name, id_tool, url_tool):

        data = {'name': name, 
                'biography': '',
                'idtool': id_tool,
                'urltool': url_tool}
        
        return self.request_x.post(data,self.host+self.url)