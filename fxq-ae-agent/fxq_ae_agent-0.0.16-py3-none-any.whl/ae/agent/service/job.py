import logging
import os
import shutil
import threading
import uuid

from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Service
from git import Repo

from fxq.ae.agent import constants
from fxq.ae.agent.factory.run import RunFactory
from fxq.ae.agent.model.job import Job
from fxq.ae.agent.model.run import Run
from fxq.ae.agent.service.docker import DockerService
from fxq.ae.agent.service.run import RunService

LOGGER = logging.getLogger(__name__)


@Service
class JobService:

    @Autowired
    def __init__(self, run_service, docker_service):
        self.run_service: RunService = run_service
        self.docker_service: DockerService = docker_service
        LOGGER.info("System Pipeline Base set to %s" % constants.PIPELINE_BASE)

    def process_request(self, job: Job) -> Run:
        LOGGER.info("Processing Request %s" % job.name)
        run = RunFactory.prepare(job)
        t = threading.Thread(target=self._run, args=(run,))
        t.start()
        return run

    def _run(self, run: Run):
        workspace_path = JobService._get_workspace_path()
        JobService._clone_repo(run.job.git_url, workspace_path)
        LOGGER.debug("Cloned Repo into Workspace %s" % workspace_path)
        RunFactory.configure_from_yml_file(run, "%s/%s" % (workspace_path, constants.PIPELINE_YML_NAME))
        LOGGER.info("Starting a new run thread for uuid %s" % run.uuid)
        self.run_service.start(run, workspace_path)
        shutil.rmtree(workspace_path)
        LOGGER.info("Finishing run thread for uuid %s" % run.uuid)

    @staticmethod
    def _get_workspace_path() -> str:
        return "%s/%s/%s" % (
            constants.PIPELINE_BASE,
            constants.PROJECTS_FOLDER,
            uuid.uuid4()
        )

    @staticmethod
    def _clone_repo(url: str, workspace_path: str) -> Repo:
        if os.path.exists(workspace_path): shutil.rmtree(workspace_path)
        return Repo.clone_from(url, workspace_path)
