from taskmonk.utils import urlConfig, apiCall, argumentlist, utilities
from taskmonk.utils.jsonUtils import json2obj
from datetime import datetime, timedelta


import base64
import gzip
import json
import requests
import logging
import os
import zlib
import urllib.request
from time import sleep

argsList = argumentlist.argsList
argumentVerifier = utilities.argumentVerifier

class Error(Exception):
   pass

class InvalidArguments(Error):
   pass


class TaskMonkClient:
    base_url = urlConfig.BASE_URL
    client_id = ''
    client_secret = ''
    project_id = ''
    _expires_at = None
    _access_token = None
    _refresh_token = None
    #oAuthClient

    def __init__(self, base_url, project_id, client_id = '', client_secret = ''):
        self.base_url = base_url
        #self.apiKey = api_key
        self.client_id = client_id
        self.client_secret = client_secret
        self.project_id = project_id
        self.token = self.refresh_token()
    
    def refresh_token(self):
        #token_url = "http://localhost:9000/api/oauth2/token" 
        token_url = self.base_url + '/api/oauth2/token'
        params =  {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        headers = {'accept': 'application/json'}
        response = requests.post(token_url, params= params,headers = headers)
        logging.debug(response.text)
        parsed = response.json()
        self._access_token = parsed['access_token']
        self._refresh_token = parsed['refresh_token']
        expires_in = parsed['expires_in']
        ## Keep a buffer of 120 seconds to refresh token before expiry
        self._expires_at = datetime.now() + timedelta(seconds=(expires_in - 120))

        logging.debug('_access_token %s expires at %s', self._access_token, self._expires_at)

        return

    
    def is_expired(self): 
        current_time = datetime.now()
        if (current_time > self._expires_at):
            logging.debug('token expired')
            return True
        else:
            return False

    def get_token(self):
        if self._access_token is None or self.is_expired():
            self.refresh_token()
        return self._access_token

    def get_job_progress(self, job_id):
        url = self.base_url + urlConfig.URLS['Project'] + '/' + self.project_id + '/job/' + job_id + '/status'
        response = apiCall.get(self.get_token(), url, {}, 10)
        logging.debug('response = %s', response)
        return response
    
    def get_batch_status(self, batch_id):
        url = self.base_url + urlConfig.URLS['Project'] + '/' + self.project_id + '/batch/' + batch_id + '/status'
        response = apiCall.get(self.get_token(), url, {}, 10)
        return response
    
    def get_batch(self):
        url = self.base_url + urlConfig.URLS['Project'] + '/' + self.project_id + '/batch'
        response = apiCall.get(self.get_token(), url, {}, 10)
        logging.debug(response)
        return response
    
    def upload_tasks(self, batch_id = None, input_file='', file_type = 'Excel'):

        url = self.base_url + urlConfig.URLS['Project'] + '/v2/' + self.project_id + "/batch/" + batch_id + "/tasks/import?fileType=" + file_type
    
       
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
                    'Authorization': 'Bearer ' + self.get_token()})
                logging.debug(response.json())
                parsed = response.json()
                job_id = parsed['job_id']
                logging.debug('job id = %s', job_id)
                return job_id
    
        except Exception as e: print(e)

    
    def import_tasks_url(self, file_url=None):
        try:
            if argumentVerifier([self.project_id, file_url, token]):
                raise InvalidArguments
        except InvalidArguments:
            logging.debug('invalid arguments')
            return json.dumps(argsList['importTasksUrl'])
    
        url = self.base_url + urlConfig.URLS['Project'] + '/' + self.project_id + '/import/tasks/url'
    
        data = json.dumps({
            "fileUrl": file_url,
            "batch_name": "batch_name"
        })
    
        response = apiCall.post(self.get_token(), url, data, 30)
        logging.debug(response)
        return response
    
    def is_job_complete(self, job_id):
        job_status = self.get_job_progress(job_id)
        complete = job_status['completed']
        total = job_status['total']
        if (complete == total):
            return True
        else:
            return False

    def is_batch_complete(self, batch_id):
        batch_status = self.get_batch_status(batch_id)
        complete = batch_status['completed']
        total = batch_status['total']
        if (complete == total):
            return True
        else:
            return False

    def create_batch(self, batch_name, priority = 0, comments = '', notifications = []):
        url = self.base_url + urlConfig.URLS['Project'] + '/' + self.project_id + '/batch'
        batch = {
            "batch_name": batch_name,
            "priority": priority,
            "comments": comments,
            "notifications": [
            ]
        }
        data = json.dumps(batch)
        response = apiCall.post(self.get_token(), url, data, 30)
        logging.debug(response['id'])
        return response['id']


    def wait_for_job_completion(self, job_id): 
        while (not self.is_job_complete(job_id)): 
            logging.debug("waiting for job to complete") 
            sleep(1)


    def get_batch_output(self, batch_id, local_path, output_format = 'CSV', fields = []):
        url = self.base_url + urlConfig.URLS['Project'] + '/v2/' + self.project_id + '/batch/' + batch_id + '/output?output_format=' + output_format
        data = json.dumps({'field_names': fields})
        response = apiCall.post(self.get_token(), url, data, 30)
        file_url = response['file_url']
        job_id = response['job_id']
        self.wait_for_job_completion(job_id)
        logging.debug('file_url = %s', file_url)
        urllib.request.urlretrieve(file_url, local_path)
        return local_path






