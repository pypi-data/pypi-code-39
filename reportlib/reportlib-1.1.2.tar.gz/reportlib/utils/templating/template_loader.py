import os
from os.path import dirname, join, exists

import pandas as pd
from jinja2 import Environment, FileSystemLoader

__all__ = ['template_loader']


class TemplateLoader:
    def __init__(self):
        template_dirs = {
            join(dirname(__file__), 'templates'),
            join(os.getcwd(), 'templates'),
            join(dirname(pd.__file__), 'io', 'formats', 'templates'),
        }
        loader = FileSystemLoader(template_dirs)
        self.env = Environment(loader=loader, trim_blocks=True)

    def get_template(self, template_name):
        return self.env.get_template(template_name)


template_loader = TemplateLoader()
