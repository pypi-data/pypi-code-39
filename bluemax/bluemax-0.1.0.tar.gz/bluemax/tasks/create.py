"""
    Tools to create a project
"""
import os
from pathlib import Path
from invoke import task


@task(default=True)
def project(_, name, force=False, with_config=False):
    """ Creates a project with procedures, services, settings and urls. """
    print(f"gen {name}")
    if os.path.exists(name) and force is False:
        print("that module already exists: ", name)
    else:
        if not os.path.isdir(name):
            os.makedirs(name)
        with open(os.path.join(name, "__init__.py"), "w") as file:
            file.write(
                '''""" A bluemax project """
VERSION = "0.0.1"
'''
            )
        with open(os.path.join(name, "settings.py"), "w") as file:
            if with_config is True:
                file.write(
                    '''""" add your settings here """
import os
import logging
import yaml
from bluemax.settings import merge_dict


def extend(settings):
    """ change settings """
    logging.info("extending settings")
    stage = os.getenv("STAGE", "dev")
    stage_file = f"conf/{stage}.yml"
    base_file = "conf/base.yml"
    if os.path.isfile(base_file):
        with open(base_file, "r") as file:
            loaded = yaml.safe_load(file)
            if loaded:
                merge_dict(settings, loaded)
            logging.info("loaded config: base")
    if os.path.isfile(stage_file):
        with open(stage_file, "r") as file:
            loaded = yaml.safe_load(file)
            if loaded:
                merge_dict(settings, loaded)
            logging.info("loaded config: %s ", stage)
    return settings
'''
                )
            else:
                file.write(
                    '''""" add your settings here """
import logging


def extend(settings):
    """ change settings """
    logging.info('extending settings')
    return settings
'''
                )
        with open(os.path.join(name, "urls.py"), "w") as file:
            file.write(
                '''""" add your tornado routes here """
import logging


def extend(urls):
    """ add tornado routes to urls """
    logging.info('extending urls')
    return urls
'''
            )
        with open(os.path.join(name, "procedures.py"), "w") as file:
            file.write(
                '''""" an example function and exposing it through __all__ """

__all__ = ['add']


def add(int_a: int, int_b: int) -> int:
    """ simple addition of two integers"""
    return int_a + int_b
'''
            )
        with open(os.path.join(name, "services.py"), "w") as file:
            file.write(
                '''""" an example service """
import asyncio
import time
from bluemax import context


async def clock():
    """ Will broadcast every 5 seconds """
    while True:
        context.broadcast('time', {'now': time.time()})
        await asyncio.sleep(5)
'''
            )
        with open(os.path.join(name, "log.py"), "w") as file:
            file.write(
                '''""" an example log setup """
import os
import yaml


def extend(config):  # pylint: disable=W0613
    """
    config is the existing logging configuration
    returning a dict will be used with dictConfig
    """
    if os.path.isfile("logging.yml"):
        with open("logging.yml", "r") as file:
            config = yaml.safe_load(file)
    return config
'''
            )
        if not os.path.isfile("Makefile"):
            with open(os.path.join("Makefile"), "w") as file:
                file.write(
                    f"""
SHELL := /bin/bash

lint:
\tsource venv/bin/activate && flake8 .
\tsource venv/bin/activate && pylint {name} tests

test:
\tsource venv/bin/activate && \\
\tpy.test --cov {name} --cov-report term-missing tests

check: lint test

run:
\tsource venv/bin/activate && \\
\t\tbluemax run.server -m {name}

build:
\tsource venv/bin/activate && \\
\t\tpython setup.py sdist

full: check build

setup:
\tif which python3.7 && [ ! -d venv ] ; then python3.7 -m venv venv ; fi
\tsource venv/bin/activate \\
\t\t&& python -m pip install -q -U pip \\
\t\t&& pip install -e .[dev]
"""
                )
    if with_config is True:
        config(_, name, force=force)


@task
def tests(_, name, force=False):
    """ create a config folder with dev, staging & prod yamls """
    print(f"gen test: {name}")
    test_dir = "tests"
    if os.path.exists(test_dir) and force is False:
        print("that folder already exists:", test_dir)
    else:
        if not os.path.isdir(test_dir):
            os.makedirs(test_dir)
        Path(os.path.join(test_dir, "__init__.py")).touch()
        with open(os.path.join(test_dir, "conftest.py"), "w") as file:
            file.write(
                f"""
import pytest
from bluemax.web.server import make_app
from bluemax.settings import SETTINGS

@pytest.fixture
def app(io_loop):
    SETTINGS.update(
        {{
            "procedures": "{name}.procedures",
            "tornado": {{
                "AUTH_HANDLER": None,
                "MANAGER": "bluemax:ContextRpc",
                "STATIC_DIR": None,
            }},
            "REDIS_URL": None,
        }}
    )
    result = make_app()
    return result
"""
            )
        with open(os.path.join(test_dir, f"test_web.py"), "w") as file:
            file.write(
                """
import logging
from urllib.parse import urlencode
from bluemax.web.server import BROADCASTER
from bluemax.web import json_utils
from bluemax import context

async def test_add(http_server_client):
    message = {"jsonrpc": "2.0", "id": "1a", "method": "add", "params": [2, 2]}
    response = await http_server_client.fetch(
        "/rpc", method="POST", body=json_utils.dumps(message)
    )
    assert json_utils.loads(response.body)["result"] == 4

    await context._MANAGER_.shutdown()
    await BROADCASTER.stop()
"""
            )


@task
def config(_, name, conf="conf", force=False):
    """ create a config folder with dev, staging & prod yamls """
    print(f"gen config: {conf}")
    if os.path.exists(conf) and force is False:
        print("that folder already exists: ", conf)
    else:
        if not os.path.isdir(conf):
            os.makedirs(conf)
        with open(os.path.join(conf, "base.yml"), "w") as file:
            file.write(
                """---
DEBUG: false
"""
            )
        with open(os.path.join(conf, "dev.yml"), "w") as file:
            file.write(
                f"""---
DEBUG: true
procedures: {name}.procedures
services: {name}.services
log_extend: null
settings_extend: null
urls_extend: null
tornado:
    AUTH_HANDLER: null
    MANAGER: bluemax.services:ServicesRpc
    STATIC_DIR: null
    cookie_name: null
    cookie_secret: null
    login_url: null
    cognito_oauth:
        key: null
        secret: null
        redirect_url: null
        endpoint: null
PORT: 8080
MAX_WORKERS: 4
MAX_THREADS: 4
REDIS_URL: None
redis_broadcast_q: broadcast
redis_work_q: perform
redis_services_q: services
"""
            )
        with open(os.path.join(conf, "staging.yml"), "w") as file:
            file.write(
                """---
"""
            )
        with open(os.path.join(conf, "prod.yml"), "w") as file:
            file.write(
                """---
"""
            )
