import os
from copy import copy
from time import sleep
from typing import Optional
import docker
from docker.models.containers import Container
from docker.client import DockerClient


__all__ = (
    'run_testing_database',
)


# TODO: Try and make this work with the --keep-db flag?
class DockerDatabase(object):
    """Run a database via Docker."""

    # These must be overridden in subclasses
    # --------------------------------------
    # Django Details
    ENGINE_MATCH: Optional[str] = None
    ENGINE_NAME: Optional[str] = None
    # Docker Details
    DOCKER_CONTAINER_IMAGE: Optional[str] = None
    DOCKER_CONTAINER_VERSION: Optional[str] = 'latest'
    DOCKER_CONTAINER_PORT: Optional[int] = None
    DOCKER_CONTAINER_HOST: Optional[str] = None
    # Database Details
    DATABASE: Optional[str] = None
    DATABASE_PORT: Optional[str] = None
    DATABASE_PASSWORD_ENV_VAR: Optional[str] = None
    DATABASE_USER: Optional[str] = None
    DATABASE_PASSWORD: str = 'database'  # TODO: Randomize password
    DATABASE_DATA_DIR: Optional[str] = None

    def __init__(self, version=None, engine=None):
        self.ENGINE_NAME = engine

        if version is not None:
            self.DOCKER_CONTAINER_VERSION = version

        self.client: DockerClient = docker.from_env()
        self.container: Optional[Container] = None

    @property
    def docker_container_name(self) -> str:
        return f"django_testing_database_{os.path.basename(os.getcwd())}_{self.docker_image_name.replace(':', '-')}"

    @property
    def docker_image_name(self) -> str:
        return f'{self.DOCKER_CONTAINER_IMAGE}:{self.DOCKER_CONTAINER_VERSION}'

    @property
    def django_database_config_dictionary(self):
        return {
            'ENGINE': self.ENGINE_NAME,
            'NAME': self.DATABASE,
            'USER': self.DATABASE_USER,
            'PASSWORD': self.DATABASE_PASSWORD,
            'HOST': self.DOCKER_CONTAINER_HOST,
            'PORT': self.DOCKER_CONTAINER_PORT,
        }

    def set_container_network_info(self):
        _container_port = list(self.container.attrs['NetworkSettings']['Ports'].items())[0][1][0]
        self.DOCKER_CONTAINER_HOST = 'localhost'
        self.DOCKER_CONTAINER_PORT = _container_port['HostPort']

    def clean_docker(self) -> None:
        # Always kill the container!
        # We dont want stale data persisting between test runs.
        try:
            # TODO: Should I have some fuzzy-match logic here just in case?
            self.container = self.client.containers.get(self.docker_container_name)
            self.container.stop()
            try:
                self.container.wait()
            except docker.errors.NotFound:
                pass
        except docker.errors.NotFound:
            pass
        self.container = None

    def start_docker(self) -> dict:
        """Start the database using docker."""
        self.container = self.client.containers.run(
            self.docker_image_name,
            detach=True,
            remove=True,
            environment=[f'{self.DATABASE_PASSWORD_ENV_VAR}={self.DATABASE_PASSWORD}', ],
            tmpfs={f'{self.DATABASE_DATA_DIR}': ''},
            publish_all_ports=True,
            name=self.docker_container_name
        )
        sleep(15)  # Sleep to give it a time to complete the startup.
        self.container.reload()  # Reload to make sure everything is fresh.
        self.set_container_network_info()


class PostgreSQL(DockerDatabase):
    """Run a PostgreSQL database using Docker."""
    ENGINE_MATCH = 'postgresql'
    DOCKER_CONTAINER_IMAGE = 'postgres'
    DATABASE = 'postgres'
    DATABASE_PORT = 5432
    DATABASE_USER = 'postgres'
    DATABASE_PASSWORD_ENV_VAR = 'POSTGRES_PASSWORD'
    DATABASE_DATA_DIR = '/var/lib/postgresql/data'


class MySQL(DockerDatabase):
    """Run a MySQL database using Docker."""
    ENGINE_MATCH = 'mysql'
    DOCKER_CONTAINER_IMAGE = 'mysql'
    DATABASE = 'mysql'  # TODO: is this correct?
    DATABASE_PORT = 3306
    DATABASE_USER = 'root'
    DATABASE_PASSWORD_ENV_VAR = 'MYSQL_ROOT_PASSWORD'
    DATABASE_DATA_DIR = '/var/lib/mysql'


def run_testing_database(django_db_config, version=None):
    """
    Run a database for Django testing, using docker and tmpfs.
    """
    db_engine_name = django_db_config['default']['ENGINE']
    new_db_config = copy(django_db_config)
    if PostgreSQL.ENGINE_MATCH in db_engine_name:
        postgres = PostgreSQL(version, db_engine_name)
        postgres.clean_docker()
        postgres.start_docker()
        new_db_config['default'] = postgres.django_database_config_dictionary
    elif MySQL.ENGINE_MATCH in db_engine_name:
        mysql = MySQL(version, db_engine_name)
        mysql.clean_docker()
        mysql.start_docker()
        new_db_config['default'] = mysql.django_database_config_dictionary
    return new_db_config


