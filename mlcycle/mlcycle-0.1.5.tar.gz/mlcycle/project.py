import requests

from .apierror import ApiError
from .environment import Environment

class ProjectCollection:
    env:Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.getBaseUrl() + "/projects"

    def getAll(self):
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def getById(self, projectId):
        if not projectId:
            raise ApiError("project not given")

        resp = requests.get(self.url + "/" + projectId, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def add(self, project):
        self.check(project)

        resp = requests.post(self.url, json=project, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def update(self, projectId, project):
        if not projectId:
            raise ApiError("project id not given")

        self.check(project)

        resp = requests.put(self.url + "/" + projectId, json=project, verify=False)
        if resp.status_code != 200:
            return False

        return resp.json()

    def delete(self, projectId):
        if not projectId:
            raise ApiError("project id ist not given")

        resp = requests.delete(self.url + "/" + projectId, verify=False)

        return resp.status_code == 200

    def check(self, project):
        if not project:
            raise ApiError("project not set")

        if 'name' not in project or project['name'] == "":
            raise ApiError("project name not set")

        if 'gitRepository' not in project or project['gitRepository'] == "":
            raise ApiError('git repository not set')

