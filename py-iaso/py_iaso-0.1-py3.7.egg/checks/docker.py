import os
import docker
import time
from typing import List

from subprocess import check_output

from . import DefaultCheck
from ..utils import print_log

class DockerCheck(DefaultCheck):
    def __init__(self, *container_list: List[str]):
        self.containers = container_list
        self.client = docker.from_env()

    def check(self):
        for c in self.containers:
            try:
                container = self.client.containers.get(c)
                if container.status != 'running':
                    self.failure = 'Container {} is not running ({}!)'.format(c, container.status)
                    return False
            except docker.errors.NotFound:
                self.failure = 'Container {} is not found.'.format(c)
                return False
            except Exception as e:
                self.failure = str(e)
                return False

        self.failure = None
        return True