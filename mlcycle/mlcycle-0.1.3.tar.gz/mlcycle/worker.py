import requests

from .apierror import ApiError
from .environment import Environment

class WorkerCollection:
    env:Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.getBaseUrl() + "/workers"

    def getAll(self):
        resp = requests.get(self.url, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def getById(self, workerId):
        if not workerId:
            raise ApiError("workerId not given")

        resp = requests.get(self.url + "/" + workerId, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def add(self, worker):
        self.check(worker)

        resp = requests.post(self.url, json=worker, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def update(self, workerId, worker):
        if not workerId:
            raise ApiError("workerId not given")

        self.check(worker)

        resp = requests.put(self.url + "/" + workerId, json=worker, verify=False)
        if resp.status_code != 200:
            return False

        return resp.json()

    def delete(self, workerId):
        if not workerId:
            raise ApiError("workerId is not given")

        resp = requests.delete(self.url + "/" + workerId, verify=False)

        return resp.status_code == 200

    def check(self, worker):
        if not worker:
            raise ApiError("worker not set")

        if 'name' not in worker or worker['name'] == "":
            raise ApiError("worker name not set")

