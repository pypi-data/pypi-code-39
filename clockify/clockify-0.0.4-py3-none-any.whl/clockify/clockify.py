import requests
import json
from pprint import pprint

class Task():
    def __init__(self,name, projectId):
        self.name = name
        self.projectId = projectId

class User():
    
    def __init__ (self, id = None):
        self.id = id

    def __str__(self):
        return self.id

class Clockify():

    def __init__(self,api_key):
        self.base_url = 'https://api.clockify.me/api/' 
        self.api_key = api_key
        self.header =  {'X-Api-Key': self.api_key }

    def get_all_workspaces(self):
        url = self.base_url+'workspaces/'
        r = self.__request_get(url)
        
        return r.json()
    
    def get_user (self, id):
        url = self.base_url + 'users/'+str(id)
        r = self.__request_get(url)
        return r.json()

    def get_all_projects (self, workspace_id):
        
        url = self.base_url+'workspaces/'+workspace_id+'/projects/'
        r = self.__request_get(url)
        return r.json()

    def get_all_project_users(self, workspace_id,project_id):
        url = self.base_url+'workspaces/'+workspace_id+'/projects/'+project_id+'/users/'
        r = self.__request_get(url)
        return r.json()

    def add_new_task(self, workspace_id, project_id, task_name, assigneeId = None):
        
        url = self.base_url+'workspaces/'+workspace_id+'/projects/'+project_id+'/tasks/'
        
        task = None

        if (assigneeId == None):
            task =  {'name': task_name, 'projectId': project_id }   
        else:
            task =  {'name': task_name, 'projectId': project_id, 'assigneeId': assigneeId}   
    
        r = self.__request_post(url, task)
        
        return r.json()
    
    def create_new_project(self, workspace_id, project_name):
        url = self.base_url+'workspaces/'+workspace_id+'/projects/'
        data = {'name': project_name}
        r = self.__request_post(url, data)

    def __request_get(self,url):
        return requests.get(url, headers=self.header)
    
    def __request_post(self,url,payload):
        return requests.post(url, headers=self.header,json=payload)
