from typing import Dict

from sqlalchemy import Column, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from jinja2 import Template as JinjaTemplate


class MissingVariablesError(Exception):
    def __init__(self, message):
        self.message = message


class Template:
    id = Column(Integer, primary_key=True)
    template_text = Column(Text, nullable=False)
    variable_default_values = Column(JSONB)
    required_variables = Column(ARRAY(Integer))

    def render_template(self, variables: Dict) -> str:
        t = JinjaTemplate(self.template_text)
        if not set(self.required_variables).issubset(set(variables.keys())):
            missing_variables = set(self.required_variables) - set(variables.keys())
            raise MissingVariablesError(message=f"Missing variables: {' '.join(missing_variables)}")
        return t.render(**variables)
