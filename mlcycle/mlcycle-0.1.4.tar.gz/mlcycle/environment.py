class Environment:
    host = None
    project = None
    job = None
    step = None

    def __init__(self, host, project=None, job=None, step=None):
        self.host = host
        self.project = project
        self.job = job
        self.step = step

    def getBaseUrl(self):
        return self.host

    def getProject(self):
        return self.project

    def getJob(self):
        return self.job

    def getStep(self):
        return self.step


