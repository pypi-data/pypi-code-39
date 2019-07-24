import atexit
import functools
import logging
import os
import time
import traceback
import typing

import requests
from jaeger_client import Config
from jaeger_client import Span
from jaeger_client import Tracer
from opentracing import tags

from py_jaeger_tracing.patches.patches import TracingPatcher

FINISH_TIMEOUT = 2  # require for clean buffer

DEFAULT_SERVICE_NAME = 'UnknownService'

DEFAULT_TRACER_CONFIG = {
    'sampler': {
        'type': 'const',
        'param': 1,
    },
    'logging': False,
}


class MpTracingEnvironment:
    parent_span = None


class TracingEnvironment:
    host = os.environ.get('JAEGER_AGENT_HOST', 'localhost')
    port = int(os.environ.get('JAEGER_AGENT_PORT', '16686'))
    service_name = None
    config = None
    logger = None
    patches = None
    tracer: Tracer = None
    spans: typing.List[Span] = []


def on_shutdown():
    if MpTracingEnvironment.parent_span is None:
        for span in TracingEnvironment.spans:
            span.finish()
    else:
        for span in TracingEnvironment.spans:
            if span != MpTracingEnvironment.parent_span:
                span.finish()
            else:
                break

    time.sleep(FINISH_TIMEOUT)
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

        if TracingEnvironment.tracer is not None and len(TracingEnvironment.spans) > 0:
            MpTracingEnvironment.parent_span = TracingEnvironment.spans[-1]

        TracingEnvironment.service_name = service_name
        TracingEnvironment.config = config
        TracingEnvironment.logger = logger
        TracingEnvironment.patches = patches

        Config._initialized = None
        TracingEnvironment.tracer = Config(
            config=config,
            service_name=service_name,
            validate=True
        ).initialize_tracer()
        TracingPatcher.apply_patches(patches)

        atexit.register(on_shutdown)

    @classmethod
    def initialize_subprocess(cls, f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            TracingStarter.initialize(
                TracingEnvironment.service_name or DEFAULT_SERVICE_NAME,
                TracingEnvironment.config or DEFAULT_TRACER_CONFIG,
                TracingEnvironment.logger,
                TracingEnvironment.patches
            )

            label = f'{f.__module__}.{f.__name__}'

            if len(TracingEnvironment.spans) > 0:
                span = TracingEnvironment.tracer.start_span(label,
                                                            child_of=TracingEnvironment.spans[-1])
            else:
                span = TracingEnvironment.tracer.start_span(label)

            TracingEnvironment.spans.append(span)
            try:
                return f(*args, **kwargs)
            except Exception as e:
                span.set_tag(tags.ERROR, True)
                span.log_kv({
                    'event': tags.ERROR,
                    'error.object': e,
                    'error.traceback': traceback.format_exc()
                })
                raise e
            finally:
                h_span = None
                while h_span != span:
                    h_span = TracingEnvironment.spans.pop()
                span.finish()
                TracingStarter.finish()

        return wrapper

    @classmethod
    def finish(cls):
        on_shutdown()
