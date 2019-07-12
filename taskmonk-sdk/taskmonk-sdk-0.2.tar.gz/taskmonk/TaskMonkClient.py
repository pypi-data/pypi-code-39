from utils import urlConfig, apiCall, argumentlist, utilities
from utils.jsonUtils import json2obj
import base64
import gzip
import json
import requests
import logging
import os
import zlib

argsList = argumentlist.argsList
argumentVerifier = utilities.argumentVerifier

class Error(Exception):
   pass

class InvalidArguments(Error):
   pass


class TaskMonkClient:
    baseURL = urlConfig.BASE_URL
    token = None
    clientId = ''
    clientSecret = ''
    project_id = ''
    #oAuthClient

    def __init__(self, base_url, project_id, client_id = '', client_secret = ''):
        self.baseURL = base_url
        #self.apiKey = api_key
        self.clientId = client_id
        self.clientSecret = client_secret
        self.project_id = project_id
        self.token = self.refreshToken()
    
    def refreshToken(self):
        #token_url = "http://localhost:9000/api/oauth2/token" 
        token_url = self.baseURL + '/api/oauth2/token'
        params =  {
            'grant_type': 'client_credentials',
            'client_id': self.clientId,
            'client_secret': self.clientSecret
        }
        headers = {'accept': 'application/json'}
        access_token_response = requests.post(token_url, params= params,headers = headers)
        #logging.debug(access_token_response.text)
        parsed = access_token_response.json()
        accessToken = parsed['access_token']
        logging.debug(accessToken)
        #logging.debug(access_token_response.status_code)
        return accessToken
    
    def getTokenResponse(self):
        if self.token is None:
            self.token = self.refreshToken
        #logging.debug(self.token)
        return self.token

    def getProjectInfoByID(self):
        try:
            if argumentVerifier([self.project_id, self.apiKey]):
                raise InvalidArguments
        except InvalidArguments:
            logging.debug('invalid arguments')
            return json.dumps(argsList['getProjectInfoByID'])
    
        url = self.baseURL + urlConfig.URLS['Project'] + '/' + self.project_id
        response = apiCall.get(self.token,url, {}, 10)
    
        return json2obj(response).response
    
    def getProjectUsers(self):
        url = self.baseURL + urlConfig.URLS['Project'] + '/' + self.project_id + '/users'
        response = apiCall.get(url, {}, 10)
        return response
    
    # def uploadTasksWithBatchId(self,self.project_id, batch_id, files=None):
    #      url = self.baseURL + urlConfig.URLS['Project'] + self.project_id + "/batch/" + batch_id + "/tasks/import"
    #     # files = {'files': open('/Users/prashanth/Downloads/2095.14_Input.xls', 'rb')}
    #     # content = "encoded", batch_name = batchName, priority = Some(priority), comments = Some(comments))
    #     response = apiCall.fileUpload(self.apiKey, url, files , 30)
    #     return response
    
    def get_job_progress(self, job_id):
        url = self.baseURL + urlConfig.URLS['Project'] + '/' + self.project_id + '/job/' + job_id + '/status'
        response = apiCall.get(self.token,url, {}, 10)
        return json2obj(response).response
    
    def getBatchStatus(self, batch_id):
        url = self.baseURL + urlConfig.URLS['Project'] + '/' + self.project_id + '/batch/' + batch_id + '/status'
        response = apiCall.get(self.token, url, {}, 10)
        return response
    
    def get_batch(self):
        url = self.baseURL + urlConfig.URLS['Project'] + '/' + self.project_id + '/batch'
        response = apiCall.get(self.token, url, {}, 10)
        logging.debug(response)
        return response
    
    def upload_tasks(self, batch_id = None, input_file='', file_type = 'Excel'):

        url = self.baseURL + urlConfig.URLS['Project'] + '/v2/' + self.project_id + "/batch/" + batch_id + "/tasks/import?fileType=" + file_type
    
       
        try:   
            if input_file.endswith('.gz'):
                fileContent = open(input_file, 'rb').read()
                encoded = base64.b64encode(fileContent)
            else:
                fileContent = open(input_file, 'rb').read()
                with gzip.open('file.txt.gz', 'wb') as f:
                    f.write(fileContent)
                fileContent = open('file.txt.gz', 'rb').read()
                encoded = base64.b64encode(fileContent)
                os.remove('file.txt.gz')
                response = requests.post(url, encoded, headers = {
                    'Content-Type': 'text/plain',
                    'Authorization': 'Bearer ' + self.token})
                logging.debug(response.json())
                parsed = response.json()
                job_id = parsed['job_id']
                logging.debug('job id = %s', job_id)
                return job_id
    
        except Exception as e: print(e)

    
    # def uploadTasksWithoutBatchId(self, batch_name = '', input_file='', file_type = 'Excel'):

    #     url = self.baseURL + urlConfig.URLS['Project'] + '/' + self.project_id + "/batch/" + batch_id + "/tasks/import?file_type=" + file_type
        
    #     try:

    #         if input_file.endswith('.gz'):
    #             fileContent = open(input_file, 'rb').read()
    #             encoded = base64.b64encode(fileContent)
    #         else:
    #             fileContent = open(input_file, 'rb').read()
    #             with gzip.open('file.txt.gz', 'wb') as f:
    #                 f.write(fileContent)
    #             fileContent = open('file.txt.gz', 'rb').read()
    #             encoded = base64.b64encode(fileContent)
    #             response = requests.post(url, encoded, headers = {
    #                 'Content-Type': 'text/plain',
    #                 'Authorization': 'Bearer ' + self.token})
    #             return response
    
    #     except Exception as e: print(e)
    
    def importTasksUrl(self, fileUrl=None):
        try:
            if argumentVerifier([self.project_id, fileUrl, token]):
                raise InvalidArguments
        except InvalidArguments:
            logging.debug('invalid arguments')
            return json.dumps(argsList['importTasksUrl'])
    
        url = self.baseURL + urlConfig.URLS['Project'] + '/' + self.project_id + '/import/tasks/url'
    
        data = json.dumps({
            "fileUrl": fileUrl,
            "batch_name": "batch_name"
        })
    
        response = apiCall.post(self.token,url, data , 30)
        logging.debug(response)
        return response
    

    def create_batch(self,batchName=''):

        url = self.baseURL + urlConfig.URLS['Project'] + '/' + self.project_id + '/batch'
        batch = {
            "batch_name": "string",
            "priority": 0,
            "comments": "string",
            "notifications": [
                {
                "notification_type": "Email",
                "metadata": {}
                }
            ]
        }
        data = json.dumps(batch)
        response = apiCall.post(self.token,url,data,30)
        logging.debug(response['id'])
        return response['id']







