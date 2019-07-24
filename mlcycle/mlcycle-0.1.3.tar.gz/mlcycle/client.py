import requests

from .environment import Environment

from .worker import WorkerCollection
from .project import ProjectCollection
from .job import JobCollection
from .scheduler import Scheduler
from .fragment import FragmentCollection

requests.packages.urllib3.disable_warnings()

def from_env():
    host = os.environ.get('MLCYCLE_HOST')
    project = os.environ.get('MLCYCLE_PROJECT')
    job = os.environ.get('MLCYCLE_JOB')
    step = os.environ.get('MLCYCLE_STEP')

    env = Environment(host, project, job, step)

    return Client(env)

def init_with(host):
    env = Environment(host)

    return Client(env)

class Client:
    env:Environment

    Workers:WorkerCollection
    Projects:ProjectCollection
    Jobs:JobCollection
    Scheduler:Scheduler
    Fragments:FragmentCollection

    def __init__(self, environment):
        self.env = environment

        self.Workers = WorkerCollection(environment)
        self.Projects = ProjectCollection(environment)
        self.Jobs = JobCollection(environment)
        self.Scheduler = Scheduler(environment)
        self.Fragments = FragmentCollection(environment)
