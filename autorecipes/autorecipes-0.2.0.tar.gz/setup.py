# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['autorecipes']

package_data = \
{'': ['*'],
 'autorecipes': ['data/configure/*', 'data/install/*', 'stubs/conans/*']}

install_requires = \
['conan>=1.14,<2.0', 'toml>=0.10.0,<0.11.0', 'typing_extensions>=3.7,<4.0']

extras_require = \
{'docs': ['sphinx>=1.8,<2.0', 'sphinx_rtd_theme>=0.4.3,<0.5.0']}

setup_kwargs = {
    'name': 'autorecipes',
    'version': '0.2.0',
    'description': 'Generic Conan recipes for CMake and Python projects.',
    'long_description': ".. start-include\n\n===========\nautorecipes\n===========\n\nGeneric Conan_ recipes for C/C++ and Python projects.\n\n.. _Conan: https://docs.conan.io/\n\n.. image:: https://api.bintray.com/packages/jfreeman/jfreeman/autorecipes%3Ajfreeman/images/download.svg\n   :target: https://bintray.com/jfreeman/jfreeman/autorecipes%3Ajfreeman/_latestVersion\n   :alt: Latest Bintray version\n\n.. .. image:: https://readthedocs.org/projects/autorecipes/badge/?version=latest\n   :target: https://autorecipes.readthedocs.io/\n   :alt: Documentation status\n\n.. image:: https://travis-ci.org/thejohnfreeman/autorecipes.svg?branch=master\n   :target: https://travis-ci.org/thejohnfreeman/autorecipes\n   :alt: Build status: Linux and OSX\n\n.. image:: https://ci.appveyor.com/api/projects/status/github/thejohnfreeman/autorecipes?branch=master&svg=true\n   :target: https://ci.appveyor.com/project/thejohnfreeman/autorecipes\n   :alt: Build status: Windows\n\n\nC/C++\n=====\n\nIf your project\n\n- uses CMake_,\n- and installs a `package configuration file`__\n- that defines the variable ``<PACKAGE_NAME>_COMPONENTS``\n- with a list of components,\n- and for each of them defines a target ``<package_name>::<component>``,\n\nthen you should be able to copy this recipe to package it for Conan:\n\n.. _CMake: https://cmake.org/cmake/help/latest/\n.. __: https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html#package-configuration-file\n\n.. code-block:: python\n\n   from conans import python_requires\n\n   CMakeConanFile = python_requires('autorecipes/[*]@jfreeman/testing').cmake()\n\n   class Recipe(CMakeConanFile):\n       name = CMakeConanFile.__dict__['name']\n       version = CMakeConanFile.__dict__['version']\n\n\nPython\n======\n\nIf your project\n\n- uses Poetry_,\n- with a ``pyproject.toml`` package metadata file as defined in `PEP 518`_,\n\n.. _Poetry: https://poetry.eustace.io/docs/\n.. _PEP 518: https://www.python.org/dev/peps/pep-0518/\n\nthen you should be able to copy this recipe to package it for Conan:\n\n.. code-block:: python\n\n   from conans import python_requires\n\n   PythonConanFile = python_requires('autorecipes/[*]@jfreeman/testing').python()\n\n   class Recipe(PythonConanFile):\n       name = PythonConanFile.__dict__['name']\n       version = PythonConanFile.__dict__['version']\n\n\nFAQ\n===\n\n.. Look at this fucking joke of a syntax. Just let me nest!\n\n- **Why do I need to copy the** ``name`` **and** ``version`` **attributes from\n  the base class?**\n\n  Conan parses the recipe looking for the ``name`` and ``version`` attributes,\n  instead of just executing it. Thus, we must copy the attributes to move past\n  that check.\n\n  Further, these attributes are descriptors_. Accessing them with dot\n  notation, like ``CMakeConanFile.name``, evaluates them against the class\n  ``CMakeConanFile`` instead of your recipe, but they need the most derived\n  type to work correctly.\n\n  .. _descriptors: https://docs.python.org/3/howto/descriptor.html\n\n- **Can I override some attributes?**\n\n  Yes. These base classes just provide default values.\n\n.. end-include\n",
    'author': 'John Freeman',
    'author_email': 'jfreeman08@gmail.com',
    'url': 'https://github.com/thejohnfreeman/autorecipes/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6-dev,<4.0',
}


setup(**setup_kwargs)
