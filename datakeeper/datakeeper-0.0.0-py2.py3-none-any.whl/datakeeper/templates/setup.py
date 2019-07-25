#!/usr/bin/env python
try:
    from setuptools import setup
    args = {}
except ImportError:
    from distutils.core import setup
    print("""\
*** WARNING: setuptools is not found.  Using distutils...
""")

from setuptools import setup
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(name='{{ name }}',
      version='{{ version }}',
      {%- if description %}
      description='{{ description }}',
      {%- endif %}
      {%- if readme %}
      long_description=read_md('{{ readme }}'),
      {%- endif %}
      author='datakeeper',
      url='https://gitlab.com/clear/ClearID/app-datakeeper',
      #license='MIT',
      install_requires=[
          "datakeeper"
      ],
      packages=['{{ name }}'],
      scripts=[],
      package_data={},
      #include_package_data=True,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Other Audience',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7'
      ],
     )
