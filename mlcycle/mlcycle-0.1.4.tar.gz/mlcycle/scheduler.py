import requests

from .apierror import ApiError
from .environment import Environment

class Scheduler:
    env:Environment
    url = None

    def __init__(self, env):
        self.env = env
        self.url = self.env.getBaseUrl() + "/scheduler"

    def getPending(self):
        resp = requests.get(self.url, verify=False)

        if resp.status_code == 408:
            return []
        elif resp.status_code != 200:
            return False

        return resp.json()

    def claim(self, jobId, step):
        self.check(jobId, step)

        resp = requests.post(self.url + "/" + jobId + "/step/" + str(step) + "/claim", verify=False)

        return resp.status_code == 200

    def complete(self, jobId, step):
        self.check(jobId, step)

        resp = requests.post(self.url + "/" + jobId + "/step/" + str(step) + "/complete", verify=False)

        return resp.status_code == 200

    def error(self, jobId, step):
        self.check(jobId, step)

        resp = requests.post(self.url + "/" + jobId + "/step/" + str(step) + "/error", verify=False)

        return resp.status_code == 200

    def check(self, jobId, step):
        if not jobId:
            raise ApiError("jobid not set")

        if not str(step):
            raise ApiError("step not set")
