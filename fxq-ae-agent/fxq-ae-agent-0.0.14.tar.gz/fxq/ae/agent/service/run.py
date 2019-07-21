import logging
from datetime import datetime

from docker.models.containers import Container
from fxq.core.beans.factory.annotation import Autowired
from fxq.core.stereotype import Service

from fxq.ae.agent.model.run import Run, Step, Command
from fxq.ae.agent.model.status import Status
from fxq.ae.agent.service.docker import DockerService

LOGGER = logging.getLogger(__name__)


@Service
class RunService:

    @Autowired
    def __init__(self, docker_service):
        self._docker_service: DockerService = docker_service

    def start(self, run: Run, workspace_path: str):
        LOGGER.info("Executing Run uuid %s" % run.uuid)
        try:
            self._do_run(run, workspace_path)
        except RunException:
            LOGGER.error("Run Failed, failing remaining Steps")
            self._abort_remaining_steps(run)
        LOGGER.info("Completed Executing the run %s" % run.uuid)

    def _do_run(self, run: Run, workspace_path):
        run.status = Status.IN_PROGRESS
        for step in run.steps:
            try:
                self._do_step(step, workspace_path)
            except Exception as e:
                LOGGER.error("Error occurred in Step #%s - %s, failing run, set to Debug for the full stacktrace" % (
                    step.number, step.name))
                LOGGER.debug(e)
                run.ended = datetime.now()
                run.status = Status.FAILED
                break

        if run.status == Status.IN_PROGRESS:
            run.ended = datetime.now()
            run.status = Status.SUCCESSFUL
        elif run.status == Status.FAILED:
            raise RunException("Run aborted due to Failed Run Status")

    def _do_step(self, step: Step, workspace_path):
        LOGGER.info("Setting up step %s" % step.name)
        step.status = Status.IN_PROGRESS
        container = None
        try:
            container = self._do_step_setup(step, workspace_path)
            self._do_step_work(step, container)
        except Exception as e:
            LOGGER.error(
                "Exception caught during step, marking as failed, set to Debug for the full stacktrace")
            LOGGER.debug(e)
            step.status = Status.FAILED
        finally:
            self._docker_service.teardown(container)

        if step.status == Status.IN_PROGRESS:
            step.status = Status.SUCCESSFUL
        elif step.status == Status.FAILED:
            raise StepException("Step aborted due to Failed Step Status")

    def _do_step_setup(self, step: Step, workspace_path: str):
        container = self._docker_service.provision(
            step.run.uuid,
            step.image,
            workspace_path
        )
        return container

    def _do_step_work(self, step: Step, container: Container):
        LOGGER.info("Running commands for step %s" % step.name)
        for command in step.commands:
            self._do_command(command, container)

    def _do_command(self, command: Command, container):
        LOGGER.info("Running command %s" % command.instruction)
        output = self._docker_service.run_command(container, command.instruction)
        while True:
            try:
                std_out, std_err = next(output)
                if std_out:
                    command.add_output(std_out.decode())
                if std_err:
                    command.add_error(std_err.decode())
                    raise StdErrException("Execution stopped due to command receiving stdErr")
            except StopIteration:
                break

    def _abort_remaining_steps(self, run: Run):
        for step in run.steps:
            if step.status == Status.PENDING:
                step.status = Status.ABORTED


class RunException(Exception):
    pass


class StepException(Exception):
    pass


class StdErrException(Exception):
    pass
