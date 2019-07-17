from __future__ import absolute_import
from .pi import PicatMagics, check_picat

from IPython.core.display import display, HTML, Javascript
from os import path

__version__ = '0.1.1'

with open(path.join(path.abspath(path.dirname(__file__)), 'static/picat.js')) as f:
    initHighlighter = f.read()


def load_ipython_extension(ipython):
    """
    Load ipicat extension using `%load_ext ipicat`
    Can be configured to be autoloaded by IPython at startup time.
    """
    # You can register the class itself without instantiating it. IPython will
    # call the default constructor on it.    
    display(Javascript(initHighlighter))
    if check_picat():
        ipython.register_magics(PicatMagics)
