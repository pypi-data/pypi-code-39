# pylint: disable=W0621
""" Task for the running of bluemax """
import logging
import yaml
from invoke import task
from bluemax import settings
from .utils import get_module, pid_file, extend_logging

LOGGER = logging.getLogger(__name__)


@task
def config(_, module=None, config=None):
    """ displays resultant config """
    if config:
        settings.init_settings(config)
    if module is None:
        module = settings.SETTINGS["procedures"]
    mod = get_module(module)
    if mod:
        settings.SETTINGS.update(mod)
        LOGGER.info("\n---\n%s", yaml.dump(settings.SETTINGS))


@task(
    default=True,
    help={
        "pid": "/path/to/pid/file",
        "module": "module to remote",
        "services": "services module",
        "config": "path to config.yml",
    },
)
def server(_, module=None, pid="server.pid", services=None, config=None):
    """ runs a bluemax server with optional services """
    from bluemax.web import server as m_server

    if config:
        settings.init_settings(config)
    if module is None:
        module = settings.SETTINGS["procedures"]
    config = get_module(module)
    if config:
        if services:
            config["services"] = services
        settings.SETTINGS.update(config)
        extend_logging(settings.SETTINGS)
        LOGGER.debug(yaml.dump(settings.SETTINGS))
        with pid_file(pid):
            m_server.main()


@task(
    help={
        "pid": "/path/to/pid/file",
        "module": "module to remote",
        "services": "services module",
        "config": "path to config.yml",
    }
)
def worker(_, module=None, pid="worker.pid", config=None):
    """ runs a bluemax worker """
    from bluemax.work import worker as m_worker

    if config:
        settings.init_settings(config)
    if module is None:
        module = settings.SETTINGS["procedures"]
    config = get_module(module)
    if config:
        settings.SETTINGS.update(config)
        extend_logging(settings.SETTINGS)
        with pid_file(pid):
            m_worker.main()


@task(
    help={
        "pid": "/path/to/pid/file",
        "module": "services module",
        "config": "path to config.yml",
    }
)
def services(_, module=None, pid="services.pid", config=None):
    """ runs a bluemax services """
    from bluemax.services import server as s_worker

    if config:
        settings.init_settings(config)
    if module is None:
        module = settings.SETTINGS["services"]
    else:
        settings.SETTINGS.update({"services": module})
    extend_logging(settings.SETTINGS)
    with pid_file(pid):
        s_worker.main()
