# -*- coding: utf-8 -*-

import asyncio
import importlib

class State():
    """Singleton State class
    """

    class __State():
        def __init__(self, config):
            self.conn = None
            self.config = config
    
    instance = None
    actions = {}

    def __init__(self, config):
        if State.instance is None:
            State.instance = State.__State(config)

            for key in config['ACTIONS']:
                State.actions[key] = self.import_action(
                     config['ACTIONS'][key]
                )

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def set_connection(self, connection):
        self.instance.conn = connection

    def import_action(self, lib):
        # Extract action's Class name
        className = lib.split('.')[-1]
        # Extract module path
        module = lib.replace(f'.{className}', '')
        # import the module
        imported_module = importlib.import_module(module)
        return getattr(imported_module, className)
