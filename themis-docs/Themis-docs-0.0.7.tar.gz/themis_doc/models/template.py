from typing import Dict

from sqlalchemy import Column, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from jinja2 import Template as JinjaTemplate
from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import relationship


class MissingVariablesError(Exception):
    def __init__(self, message):
        self.message = message


class Template:
    id = Column(Integer, primary_key=True)
    template_text = Column(Text, nullable=False)
    variable_default_values = Column(JSONB)
    required_variables = Column(ARRAY(Text))

    @declared_attr
    def documents(self):
        return relationship('Document', back_populates="template")

    def render_template(self, variables: Dict) -> str:
        all_vars = {**self.variable_default_values, **variables}
        t = JinjaTemplate(self.template_text)
        if not set(self.required_variables).issubset(set(all_vars.keys())):
            missing_variables = set(self.required_variables) - set(all_vars.keys())
            raise MissingVariablesError(message=f"Missing variables: {' '.join(missing_variables)}")
        return t.render(**all_vars)

