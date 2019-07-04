#!/usr/bin/env python

import yaml
import functools

class ConfigStruct():
    def set_variable(self, key, value):
        setattr(self, key, value)


class configGenerator(ConfigStruct):
    def ingest_yaml(self, yaml_file, sections = None):
        file = open(yaml_file, 'r')
        config_dict = yaml.load(file)

        if sections and isinstance(sections, list):
            config_dicts = [config_dict[section] for section in sections]
            config_dict = functools.reduce(lambda x, y: {**x, **y}, config_dicts)
        elif sections and isinstance(sections, str):
            config_dict = config_dict[sections]
        else:
            pass

        output = """
import os
from armature import ConfigStruct
class Config(ConfigStruct):
"""
        to_insert = ""
        for key, value in config_dict.items():
            if isinstance(value, str):
                to_insert += "    {} = '{}'\n".format(key, value)
            else:
                to_insert += "    {} = {}\n".format(key, value)

        output+=to_insert
        file = open("./Config.py", "w")
        file.write(output)
        file.close()

        from Config import Config
        self.yaml = Config()

        new_attributes = [a for a in dir(self.yaml) if not a.startswith('__')]
        for attribute in new_attributes:
            try:
                self.set_variable(attribute, self.yaml.__class__.__dict__[attribute])
            except:
                pass

    def __repr__(self):
        parts = []
        if hasattr(self, 'yaml'):
            allAttr = [x for x in self.yaml.__class__.__dict__ if not x.startswith('__')]

            for attr in allAttr:
                parts.append("{0:30}: {1:30}\n".format(attr, getattr(self.yaml, attr)))
        return "".join(parts)


