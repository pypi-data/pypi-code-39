from .Service_Abstract import Service_Abstract
from pprint import pprint
class Project_Team_Service(Service_Abstract):

    def __init__(self):
        Service_Abstract.__init__(self,'projectteams')
        
    def save (self, name, description, id_tool, url_tool):

        data = {'name': name, 
                'description': description, 
                'idtool': id_tool,
                'urltool': url_tool}
        
        return self.request_x.post(data,self.host+self.url)
    
    def get_all_by_project(self, project_url):
        result = self.request_x.get(project_url+'/projectTeams/').json()
        return result['_embedded']['projectTeam']
    
    def get_all_by_organization (self, organization_url):
        result =  self.request_x.get(organization_url+'/projectteams/').json()
        return result['_embedded']['projectTeam']

    def get_all_team_members(self, project_team_url):
        result =  self.request_x.get(project_team_url+'/teamMemberships/').json()
        result = result['_embedded']['team_membership']
        team_members = {}
        for r in result:
            team_member_url = r['_links']['teamMember']['href']
            team_member = self.request_x.get(team_member_url).json()   
            team_member_name = team_member['name']
            team_members[team_member_name] = team_member
        
        return team_members