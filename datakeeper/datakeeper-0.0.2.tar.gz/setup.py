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

setup(name='datakeeper',
      version='0.0.2',
      description='Generalized data privacy and consent repository generator.',
      long_description=read_md('README.md'),
      author='ClearFoundation',
      author_email='developer@clearfoundation.com',
      url='https://gitlab.com/clearos/clearfoundation/datakeeper',
      license='GPL-3.0',
      install_requires=[
          "argparse",
          "pyparsing",
          "termcolor",
          "tqdm",
          "jinja2",
          "flask",
          "flask-restful",
          "flask_restplus",
          "pyyaml",
          "attrdict"
      ],
      packages=['datakeeper'],
      scripts=['datakeeper/datakeeper_app.py'],
      package_data={'datakeeper': ['templates/*']},
      include_package_data=True,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Natural Language :: English',
          'Operating System :: MacOS',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7'
      ],
     )
