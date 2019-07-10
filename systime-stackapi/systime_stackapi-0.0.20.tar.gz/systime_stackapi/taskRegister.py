from .authenticator import Authenticator
from base64 import b64encode, b64decode
from urllib.parse import urlparse
from functools import lru_cache
import requests
import time
import json

from pprint import pprint


class TaskRegister(Authenticator):
    def __init__(self, service_url, client_key_id, shared_secret, **kwargs):
        self.service_url = service_url
        self.service_token = 'TaskRegister'
        self.timeout = kwargs.get('timeout', 5)
        super().__init__(client_key_id, shared_secret, **kwargs)

    def get_task(self, task_id):
        path = '/task/{}'.format(task_id)

        r = requests.get(self.service_url + path, headers={'Content-Type': 'application/json'}, timeout=self.timeout)
        r.raise_for_status()
        return(json.loads(r.text))

    def create_task(self, description):
        path = '/task/'

        payload = {
                   'description': description
                  }

        bearer_token = self.get_service_bearer_token(self.service_token)
        r = requests.post(self.service_url + path, data=json.dumps(payload), headers={'Content-Type': 'application/json', 'Authorization': bearer_token}, timeout=self.timeout)
        r.raise_for_status()
        return(json.loads(r.text))

    def create_subtask(self, task_id, task_key, description):
        path = '/task/{}/subtask'.format(task_id)

        payload = {
                   'description': description,
                   'task_key': task_key
                  }

        r = requests.post(self.service_url + path, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, timeout=self.timeout)
        r.raise_for_status()
        return(json.loads(r.text))

    def create_event(self, task_id, subtask_id, task_key, description):
        path = '/task/{}/subtask/{}/event'.format(task_id, subtask_id)

        payload = {
                   'description': description,
                   'task_key': task_key
                  }

        r = requests.post(self.service_url + path, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, timeout=self.timeout)
        r.raise_for_status()
        return(json.loads(r.text))

    def update_task(self, task_id, task_key, status):
        path = '/task/{}'.format(task_id)

        payload = {
                   'task_key': task_key,
                   'status': status
                  }

        r = requests.put(self.service_url + path, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, timeout=self.timeout)
        r.raise_for_status()
        return(json.loads(r.text))

    def wait_for_subtask(self, task_id, subtask_id, timeout, poll_interval=5):
        timeout_time = time.time() + timeout

        while timeout_time > time.time():
            task = self.get_task(task_id)
            subtasks = task['task']['subtasks']

            if subtask_id not in subtasks:
                raise ValueError('Subtask id does not exist in task')

            if subtasks[subtask_id]['status'] is not 'New':
                return True

            time.sleep(poll_interval)

        raise TimeoutError('Timed out waiting for task to complete.')

    def update_subtask(self, task_id, subtask_id, task_key, status):
        path = '/task/{}/subtask/{}'.format(task_id, subtask_id)

        payload = {
                   'task_key': task_key,
                   'status': status
                  }

        r = requests.put(self.service_url + path, data=json.dumps(payload), headers={'Content-Type': 'application/json'}, timeout=self.timeout)
        r.raise_for_status()
        return(json.loads(r.text))
