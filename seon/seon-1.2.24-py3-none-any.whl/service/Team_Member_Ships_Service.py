from .Service_Abstract import Service_Abstract

class Team_Member_Ships_Service(Service_Abstract):

    def __init__(self):
        Service_Abstract.__init__(self,'teammemberships')
    
    def save (self, team_member_url):

        data = {'name': team_member_url }
        
        return self.request_x.post(data,self.host+self.url)