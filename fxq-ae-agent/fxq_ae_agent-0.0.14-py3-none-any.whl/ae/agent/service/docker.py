import logging

from docker import DockerClient, from_env
from docker.models.containers import Container
from fxq.core.stereotype import Service

from fxq.ae.agent import constants
from fxq.ae.agent.model.run import Command

LOGGER = logging.getLogger(__name__)


@Service
class DockerService:

    def __init__(self):
        self._docker_client: DockerClient = from_env()

    def list_containers(self):
        return self._docker_client.containers.list()

    def provision(self, name: str, image: str, workspace_path: str = None) -> Container:
        name = name.replace(" ", "_")
        image = image if ":" in image else image + ":latest"
        LOGGER.info("Pulling Container Image %s" % image)
        self._docker_client.images.pull(image)
        LOGGER.info("Provisioning Container \"%s\" with Image:\"%s\"" % (name, image))
        if workspace_path is None:
            return self._provision_without_volume(name, image)
        else:
            return self._provision_with_volume(name, image, workspace_path)

    def run_command(self, container: Container, instruction: str):
        LOGGER.info("Running Container Command \"%s\"" % instruction)
        response = container.exec_run(
            ["/bin/sh", "-c", instruction],
            privileged=True,
            tty=True,
            stream=True,
            demux=True,
            workdir=constants.PIPELINE_MOUNT_TARGET
        )
        return response.output

    def teardown(self, container: Container):
        LOGGER.debug("Starting Teardown")
        container.stop(timeout=1)
        container.remove()

    def _provision_without_volume(self, name: str, image: str) -> Container:
        return self._docker_client.containers.run(
            name=name,
            image=image,
            command="tail -f /dev/stdout",
            detach=True
        )

    def _provision_with_volume(self, name: str, image: str, workspace_path: str) -> Container:
        return self._docker_client.containers.run(
            name=name,
            image=image,
            command="tail -f /dev/stdout",
            detach=True,
            volumes={
                workspace_path: {
                    'bind': constants.PIPELINE_MOUNT_TARGET,
                    'mode': 'rw'
                }
            }
        )
