# coding=utf-8
from __future__ import absolute_import, print_function

import os

from suanpan.imports import imports

MODE = os.environ.get("SP_APP_MODE", "docker")


class StreamApp(object):
    def __init__(self):
        from suanpan.stream import Handler

        self.h = Handler

        self.stream = None
        self.handler = None
        self.arguments = []

    def __call__(self, *args, **kwargs):
        from suanpan.stream import Stream

        self.stream = Stream(*args, **kwargs)
        self.stream.call = self.handler
        return self

    def input(self, argument):
        def _dec(funcOrApp):
            funcOrApp = self.handler if isinstance(funcOrApp, StreamApp) else funcOrApp
            self.handler = self.h.input(argument)(funcOrApp)
            return self

        return _dec

    def output(self, argument):
        def _dec(funcOrApp):
            funcOrApp = self.handler if isinstance(funcOrApp, StreamApp) else funcOrApp
            self.handler = self.h.output(argument)(funcOrApp)
            return self

        return _dec

    def param(self, argument):
        def _dec(funcOrApp):  # pylint: disable=unused-argument
            self.arguments.append(argument)
            return self

        return _dec

    def column(self, argument):
        def _dec(funcOrApp):  # pylint: disable=unused-argument
            self.arguments.append(argument)
            return self

        return _dec

    def start(self, *args, **kwargs):
        self.stream.start(*args, **kwargs)


class App(object):
    MAPPING = {
        "spark": "suanpan.spark.SparkComponent",
        "docker": "suanpan.docker.DockerComponent",
        "stream": StreamApp(),
    }

    def __init__(self, mode=MODE):
        self.mode = mode
        self.app = self.MAPPING.get(self.mode)
        if isinstance(self.app, str):
            self.app = imports(self.app)
        if not self.app:
            raise Exception("Unknown App Mode: {}".format(self.mode))

    def input(self, *args, **kwargs):
        return self.app.input(*args, **kwargs)

    def output(self, *args, **kwargs):
        return self.app.output(*args, **kwargs)

    def param(self, *args, **kwargs):
        return self.app.param(*args, **kwargs)

    def column(self, *args, **kwargs):
        return self.app.column(*args, **kwargs)


app = App(MODE)
