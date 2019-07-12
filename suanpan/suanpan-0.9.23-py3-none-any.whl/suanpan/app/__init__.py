# coding=utf-8
from __future__ import absolute_import, print_function

import os

from suanpan.imports import imports

MODE = os.environ.get("SP_APP_MODE", "docker")


class StreamApp(object):
    def __init__(self, *args, **kwargs):
        from suanpan.stream import Stream, Handler

        self.stream = Stream(*args, **kwargs)
        self.h = Handler

    def input(self, argument):
        def _dec(funcOrApp):
            funcOrApp = (
                self.stream.call if isinstance(funcOrApp, StreamApp) else funcOrApp
            )
            self.stream.call = self.h.input(argument)(funcOrApp)
            return self

        return _dec

    def output(self, argument):
        def _dec(funcOrApp):
            funcOrApp = (
                self.stream.call if isinstance(funcOrApp, StreamApp) else funcOrApp
            )
            self.stream.call = self.h.output(argument)(funcOrApp)
            return self

        return _dec

    def param(self, argument):
        def _dec(funcOrApp):  # pylint: disable=unused-argument
            self.stream.ARGUMENTS.append(argument)
            return self

        return _dec

    def column(self, argument):
        def _dec(funcOrApp):  # pylint: disable=unused-argument
            self.stream.ARGUMENTS.append(argument)
            return self

        return _dec

    def start(self, *args, **kwargs):
        self.stream.start(*args, **kwargs)


class App(object):
    MAPPING = {
        "spark": "suanpan.spark.SparkComponent",
        "docker": "suanpan.spark.DockerComponent",
        "stream": StreamApp,
    }

    def __init__(self, mode=MODE):
        self.mode = mode
        self.app = self.MAPPING.get(self.mode)
        if isinstance(self.app, str):
            self.app = imports(self.app)
        if not self.app:
            raise Exception("Unknown App Mode: {}".format(self.mode))

        self.input = self.app.input
        self.output = self.app.output
        self.param = self.app.param
        self.column = self.app.column


app = App(MODE)
