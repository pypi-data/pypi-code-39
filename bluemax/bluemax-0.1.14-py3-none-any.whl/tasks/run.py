# pylint: disable=W0621
"""
    Task for the running of bluemax
    The load order:
        if module:
            load module
            load settings
            extend setting
            load logging
            run target
        else
            load settings
            load module
            extend settings
            load logging
            run target
"""
import logging
import yaml
from invoke import task
from bluemax import settings
from .utils import get_module, pid_file, extend_logging

LOGGER = logging.getLogger(__name__)


def bring_up(module=None, config=None):
    """ the standard bring up order """
    if config:
        settings.init_settings(config)
    if module is None:
        module = settings.SETTINGS["procedures"]
    assert module, "module required"
    mod = get_module(module)
    if mod:
        settings.SETTINGS.update(mod)
    extend_settings = settings.get_settings("settings_extend")
    if extend_settings:
        settings.extend(extend_settings, settings.SETTINGS)
    extend_logging(settings.SETTINGS)


@task
def config(_, module=None, config=None):
    """ displays resultant config """
    bring_up(module, config)
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

    bring_up(module, config)
    if services:
        settings.SETTINGS["services"] = services
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

    bring_up(module, config)
    with pid_file(pid):
        m_worker.main()


@task(
    help={
        "pid": "/path/to/pid/file",
        "module": "services module",
        "config": "path to config.yml",
    }
)
def services(_, module=None, pid="services.pid", services=None, config=None):
    """ runs a bluemax services """
    from bluemax.services import server as s_worker

    bring_up(module, config)
    if services:
        settings.SETTINGS["services"] = services
    with pid_file(pid):
        s_worker.main()
