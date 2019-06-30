"""konfi is a config parser."""

# load built-in converters
from . import converters
from .converter import ConversionError, ConverterABC, ConverterFunc, \
    ConverterType, convert_value, has_converter, register_converter
from .field import Field, MISSING, ValueFactory, field
from .loader import Loader
from .source import SourceABC
from .sources import *
from .template import fields, get_field, is_template, is_template_like, template

__version__ = "0.0.1"
__author__ = "Giesela Inc."

default_loader = Loader()
set_sources = default_loader.set_sources
load = default_loader.load
