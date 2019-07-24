# coding=utf-8
from __future__ import absolute_import, print_function

import os

from suanpan.imports import imports
from suanpan.utils import functional

MODE = os.environ.get("SP_APP_MODE", "docker")


class TriggerApp(object):
    def __init__(self, streamApp):
        self.streamApp = streamApp
        self.handler = None
        self.interval = None

    def __call__(self, interval):
        def _dec(funcOrApp):  # pylint: disable=unused-argument
            self.interval = interval
            return self

        return _dec

    def output(self, argument):
        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, TriggerApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = self.streamApp.Handler.output(argument)(funcOrApp)
            return self

        return _dec

    def param(self, argument):
        def _dec(funcOrApp):  # pylint: disable=unused-argument
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, TriggerApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = self.streamApp.Handler.use(funcOrApp)
            self.streamApp.arguments.append(argument)
            return self

        return _dec

    def column(self, argument):
        def _dec(funcOrApp):  # pylint: disable=unused-argument
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, TriggerApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = self.streamApp.Handler.use(funcOrApp)
            self.streamApp.arguments.append(argument)
            return self

        return _dec


class StreamApp(object):
    def __init__(self):
        from suanpan.stream import Handler

        self.Handler = Handler

        self.trigger = TriggerApp(self)

        self.stream = None
        self.handler = None
        self.arguments = []

    def __call__(self, *args, **kwargs):
        from suanpan.stream import Stream

        ADSteam = type(
            "ADSteam",
            (Stream,),
            {
                "ARGUMENTS": self.arguments,
                "INTERVAL": self.trigger.interval,
                "call": self.handler,
                "trigger": self.trigger.handler,
            },
        )
        self.stream = ADSteam(*args, **kwargs)
        return self

    def input(self, argument):
        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, StreamApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = self.Handler.input(argument)(funcOrApp)
            return self

        return _dec

    def output(self, argument):
        def _dec(funcOrApp):
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, StreamApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = self.Handler.output(argument)(funcOrApp)
            return self

        return _dec

    def param(self, argument):
        def _dec(funcOrApp):  # pylint: disable=unused-argument
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, StreamApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = self.Handler.use(funcOrApp)
            self.arguments.append(argument)
            return self

        return _dec

    def column(self, argument):
        def _dec(funcOrApp):  # pylint: disable=unused-argument
            funcOrApp = (
                self.handler
                if isinstance(funcOrApp, StreamApp)
                else functional.instancemethod(funcOrApp)
            )
            self.handler = self.Handler.use(funcOrApp)
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

        self._app = None

    def __call__(self, *args, **kwargs):
        if not self._app:
            raise Exception("App not ready, mode {}".format(self.mode))
        return self._app(*args, **kwargs)

    def input(self, argument):
        def _dec(funcOrApp):
            self._app = self.app.input(argument)(funcOrApp)
            return self._app

        return _dec

    def output(self, argument):
        def _dec(funcOrApp):
            self._app = self.app.output(argument)(funcOrApp)
            return self._app

        return _dec

    def param(self, argument):
        def _dec(funcOrApp):
            self._app = self.app.param(argument)(funcOrApp)
            return self._app

        return _dec

    def column(self, argument):
        def _dec(funcOrApp):
            self._app = self.app.column(argument)(funcOrApp)
            return self._app

        return _dec

    @property
    def trigger(self):
        if self.mode != "stream":
            raise Exception("trigger is only for stream, but got {}".format(self.mode))
        self._app = self.app
        return self.app.trigger


app = App(MODE)
