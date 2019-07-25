import requests

from .apierror import ApiError
from .environment import Environment

class JobCollection:
    env:Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.getBaseUrl() + "/jobs"

    def getAll(self):
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def getById(self, jobId):
        if not jobId:
            raise ApiError("jobId not given")

        resp = requests.get(self.url + "/" + jobId, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def addSteps(self, jobId, steps):
        if not jobId:
            raise ApiError("jobId not given")

        if not steps or len(steps) == 0:
            raise ApiError("No steps given")

        for step in steps:
            if "name" not in step:
                raise ApiError("step name not set")
            if "docker" not in step:
                raise ApiError("docker configuration not set")

            docker = step['docker']

            if "image" not in docker:
                if "buildConfiguration" not in docker:
                    raise ApiError("neither an image nor a build configuration is set")

                build = docker['buildConfiguration']

                if "dockerfile" not in build:
                    raise ApiError("dockerfile for build configuraiton not set")

        resp = requests.post(self.url + "/" + jobId + "/steps", json=steps, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def addMetrics(self, metrics, jobId=None, step=None):
        if not jobId and not step:
            jobId = self.env.getJob()
            step = self.env.getStep()

        if not jobId:
            raise ApiError("jobId not given")

        if not str(step):
            raise ApiError("step not given")

        if not metrics or len(metrics) == 0:
            raise ApiError("No steps given")

        resp = requests.post(self.url + "/" + jobId + "/step/" + str(step) + "/metrics", json=metrics, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def trigger(self, projectId):
        if not projectId:
            raise ApiError("projectId not given")

        resp = requests.post(self.url + "/project/" + projectId + "/trigger", verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()




