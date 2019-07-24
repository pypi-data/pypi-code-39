import requests

from .apierror import ApiError
from .environment import Environment

class FragmentCollection:
    env:Environment

    def __init__(self, env):
        self.env = env

        self.url = self.env.getBaseUrl() + "/fragments"

    def getAllByJob(self, jobId):
        if not jobId:
            raise ApiError("jobId not given")

        resp = requests.get(self.url + "/job/" + jobId, verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()

    def getAllByStep(self, jobId, step):
        if not jobId:
            raise ApiError("jobId not given")

        resp = requests.get(self.url + "/job/" + jobId + "/step/" + str(step), verify=False)

        if resp.status_code != 200:
            return False

        return resp.json()


    def getLatestByJob(self, jobId, name, handle):
        if not jobId:
            raise ApiError("jobId not given")

        if not name:
            raise ApiError("name not given")

        if not handle:
            raise ApiError("name not given")

        resp = requests.get(self.url + "/job/" + jobId + "/name/" + name, verify=False)
        return self.__download__(resp, handle)


    def getLatestByProject(self, projectId, name, handle):
        if not projectId:
            raise ApiError("projectId not given")

        if not name:
            raise ApiError("name not given")

        if not handle:
            raise ApiError("file handle not given")

        resp = requests.get(self.url + "/project/" + projectId + "/name/" + name, stream=True, verify=False)
        return self.__download__(resp, handle)

    def getById(self, fragmentId, handle):
        if not fragmentId:
            raise ApiError("fragmentId not given")

        if not handle:
            raise ApiError("file handle not given")

        resp = requests.get(self.url + "/" + fragmentId, stream=True, verify=False)
        return self.__download__(resp, handle)

    def uploadEnv(self, fragment, handle):
        self.upload(self.env.job, self.env.step, fragment, handle)

    def upload(self, jobId, step, fragment, handle):
        if not jobId:
            raise ApiError("jobId not given")

        if not "name" in fragment:
            raise ApiError("name not in fragment")

        if not "filename" in fragment:
            raise ApiError("filename not in fragment")

        if not "type" in fragment:
            raise ApiError("type not in fragment")

        data = {
            "Name": fragment['name'],
            "Filename": fragment['filename'],
            "Type": fragment['type']
        }
        files = {
            "BinaryData": handle
        }

        resp = requests.post(self.url + "/job/" + jobId + "/step/" + str(step), data=data, files=files, verify=False)

        if resp.status_code != 200:
            print(resp.text)
            return False

        return resp.json()


    def __download__(self, resp, handle):
        if resp.status_code != 200:
            return False

        for chunk in resp.iter_content(chunk_size=1024):
            if not chunk:
                continue

            handle.write(chunk)
            handle.flush()

        return True
