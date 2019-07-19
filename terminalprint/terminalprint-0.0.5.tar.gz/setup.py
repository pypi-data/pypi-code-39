import setuptools
import codecs
import os
import re

NAME = 'terminalprint'
VERSION = '0.0.5'

def readme(path='README.rst'):
    url_prefix = 'https://raw.githubusercontent.com/xsddz/py_pkg_{name}/master/'.format(name=NAME)

    path = os.path.realpath(os.path.join(os.path.dirname(__file__), path))
    handle = codecs.open(path, encoding='utf-8')
    return handle.read().replace('.. image:: docs', '.. image:: {0}docs'.format(url_prefix))

setuptools.setup(
    name             = NAME,
    version          = VERSION,
    description      = 'a package for terminal pretty print',
    long_description = readme(),
    long_description_content_type = 'text/x-rst',
    url              = 'https://github.com/xsddz/py_pkg_terminalprint',
    author           = 'xsddz',
    author_email     = 'dingzhns@gmail.com',
    license          = 'MIT',
    classifiers      = [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
    ],
    keywords         = 'terminal print pretty table',
    packages         = setuptools.find_packages(),
    install_requires = [],
    python_requires  = '>=3',
    package_data     = {},
    data_files       = [],
    include_package_data = True,
    zip_safe         = False,
)
