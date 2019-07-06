import os
import sys

sys.path.insert(0, os.path.abspath(os.pardir))

project = 'cavy'
copyright = '2019, Dave Shawley'
author = 'Dave Shawley'
release = '0.0.0'
extensions = []
html_static_path = ['.']
html_theme = 'alabaster'
html_theme_options = {'sidebar_width': '0'}

# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
extensions.append('sphinx.ext.autodoc')

# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
extensions.append('sphinx.ext.intersphinx')
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
