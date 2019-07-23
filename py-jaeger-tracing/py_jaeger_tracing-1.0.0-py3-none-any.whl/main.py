import atexit
import logging
import os
import time
import typing

import requests
from jaeger_client import Config
from jaeger_client import Span
from jaeger_client import Tracer

from py_jaeger_tracing.patches.patches import TracingPatcher

DEFAULT_TRACER_CONFIG = {
    'sampler': {
        'type': 'const',
        'param': 1,
    },
    'logging': False,
}


class TracingEnvironment:
    host = os.environ.get('JAEGER_AGENT_HOST', 'localhost')
    port = int(os.environ.get('JAEGER_AGENT_PORT', '16686'))
    tracer: Tracer = None
    spans: typing.List[Span] = []


def on_shutdown():
    for span in TracingEnvironment.spans:
        span.finish()

    time.sleep(2)
    TracingEnvironment.tracer.close()


class TracingStarter:
    @classmethod
    def _check_server_exists(cls, logger):
        try:
            requests.get(f'http://{TracingEnvironment.host}:{TracingEnvironment.port}')
        except requests.exceptions.ConnectionError:
            logger.warning('Tracing server is not found')

    @classmethod
    def initialize(cls, service_name, config=None, logger=None, patches=None):
        logger = logger or logging.getLogger(__name__)
        config = config or DEFAULT_TRACER_CONFIG
        patches = patches or []
        cls._check_server_exists(logger)

        TracingEnvironment.tracer = Config(
            config=config,
            service_name=service_name,
            validate=True
        ).initialize_tracer()
        TracingPatcher.apply_patches(patches)

        atexit.register(on_shutdown)

    @classmethod
    def finish(cls):
        on_shutdown()
