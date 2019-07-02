#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
Created on Dec 2, 2013

This setup.py script follows as much as possible the advice of Jeff Knupp in his guide
'Open Sourcing a Python Project the Right Way'
(https://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/)

In addition, to build cython extension modules it follows the guide on automatic
detection and compiling of extension files:
https://github.com/cython/cython/wiki/PackageHierarchy.

uploaded with python setup.py sdist upload 

@author: thocu
'''
from __future__ import absolute_import

import io
import re
import sys
import inspect
import warnings

import find_gsl
import glob
import os
import atexit

from setuptools import Extension
from setuptools import find_packages
from setuptools.command.test import test as TestCommand
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext


BUILD_EXTENSIONS = False if os.environ.get('READTHEDOCS') == 'True' else True

USE_CYTHON = False

try:
    # Allow installing package without any Cython available. This
    # assumes you are going to include the .c files in your sdist.
    import Cython
    import cython_gsl
    print "Cython = \t\t[OKAY]"
    USE_CYTHON = True
except ImportError:
    print "You don't seem to have Cython installed. You can get a"
    print "copy from www.cython.org and install it."
    print "Going to use pre-generated c sources instead to build extensions."

USE_SPHINX = False

try:
    import sphinx
    import sphinx_rtd_theme
    print "sphinx = \t\t[OKAY]"
    USE_SPHINX = True
except ImportError:
    print "No sphinx or sphinx_rtd_theme found. Building documentation is not available."
    print "To build documentation, install sphinx and sphinx_rtd_theme"

# try:
#     from PyQt4.Qt import PYQT_VERSION_STR
#
#     print "PyQt4 = \t\t[OKAY]"
# except ImportError:
#     print "You don't seem to have pyqt-4 installed. Please run 'pip install python-qt4'"


class build_ext(_build_ext):
    """Customize the build_ext command to get the numpy include dirs post install"""
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


def get_ext_modules():
    ext_modules = []
    if BUILD_EXTENSIONS:
        if USE_CYTHON:
            pyx_files = [ pyx for root, _, _ in os.walk('src')
                          for pyx in glob.glob(os.path.join(root, '*.pyx'))]
            ext_modules = [ Extension(
                                        os.path.splitext(os.path.relpath(path, 'src').replace(os.sep, '.'))[0],
                                        sources=[path],
                                        include_dirs=[os.path.dirname(path),cython_gsl.get_include(),
                                                      cython_gsl.get_cython_include_dir()],
                                        libraries=cython_gsl.get_libraries(),
                                        library_dirs=[cython_gsl.get_library_dir()],
                                        extra_compile_args=["-O3", "-Wall", "-fopenmp"],
                                        extra_link_args=['-g', '-fopenmp']
                                    ) for path in pyx_files
                          ]
        else:
            c_files = [ c for root, _, _ in os.walk('src')
                        for c in glob.glob(os.path.join(root, '*.c'))]
            ext_modules = [ Extension(
                                os.path.splitext(os.path.relpath(path, 'src').replace(os.sep, '.'))[0],
                                sources=[path],
                                include_dirs=([os.path.dirname(path),find_gsl.get_include()]),
                                libraries = find_gsl.get_libraries(),
                                library_dirs=[find_gsl.get_library_dir()],
                                extra_compile_args=["-O3", "-Wall", "-fopenmp"],
                                extra_link_args=['-g', '-fopenmp']
                                    ) for path in c_files
                          ]
    return ext_modules


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []
        self.test_suite = True

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def _post_install():
    """Check that graphviz is installed."""
    print('POST INSTALL')
    import graphviz
    try:
        graphviz.version()
    except Exception as e:
        warnings.warn('Graphviz binaries not found. Please install graphviz. '
                      '(e.g. apt-get install graphviz)')
        print(e)

class new_install(install):
    """Customize the install command to check for graphviz"""
    def __init__(self, *args, **kwargs):
        install.__init__(self, *args, **kwargs)
        atexit.register(_post_install)

class new_develop(develop):
    """Customize the develop command (pip install -e) to check for graphviz"""
    def __init__(self, *args, **kwargs):
        develop.__init__(self, *args, **kwargs)
        atexit.register(_post_install)

name="virtual-microbes"
version='0.3'
release='0.3.0'

cmdclass = {'test': PyTest,
            'build_ext':build_ext,
            'install': new_install,
            'develop': new_develop}

command_options=dict()

if USE_SPHINX:
    from sphinx.setup_command import BuildDoc
    cmdclass.update({'build_sphinx': BuildDoc})
    command_options.update({
                          'build_sphinx': {
                              'project': ('setup.py', name),
                              'version': ('setup.py', version),
                              'release': ('setup.py', release),
                              'source_dir': ('setup.py', 'docs')}}
    )

def do_setup(run_here=None, *args):
    if len(args):
        orig_sys_argv = sys.argv
        sys.argv = args
    curdir = os.path.abspath(os.curdir)
    if run_here is None:
        run_here = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
    print run_here
    os.chdir(run_here)
    # finally, we can pass all this to distutils
    print sys.argv
    data_files = []
    for (path, dir, fns) in os.walk('utility_files'):
        for fn in fns:
            data_files.append(os.path.join(path,fn))
    setup(
        name=name,
        version=release,
        author="Thomas D. Cuypers, Bram van Dijk",
        author_email="thomas.cuypers@gmail.com, bramvandijk88@gmail.com",
        url="https://bitbucket.org/thocu/virtual-microbes",
        packages=find_packages('src'),
        package_dir={'': 'src'},
        data_files=[('utility_files',data_files)],
        py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob.glob('src/*.py')],
        include_package_data=True,
        description='Virtual Microbe Evolutionary Simulator',
        #long_description='%s\n%s' % (
        #    re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        #    re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
        #),
        long_description='For documentation and source code see bitbucket.org/thocu/virtual-microbes/',
        setup_requires=['cython','CythonGSL','numpy'] if USE_CYTHON else ['numpy'],
        install_requires=[
            'attrdict==1.1.0',
            'blessings>=1.6',
            'graphviz>=0.8.2',
            #'ete3',
            #'pyqt',  ete3 requires pyqt, but it cannot be 'pip install'ed
            'matplotlib<=2.9',
            'numpy>=1.11',
            'networkx==1.11',
            'pydotplus',
            'pandas>=0.18',
            'psutil>=3.0',
            'errand_boy>=0.3',  # we want to get rid of this dependency eventually
            'orderedset>=2.',
            #'pyparsing==1.5.7',
            'setproctitle>=1.1',
            'sortedcontainers>=0.9'],
        tests_require=['pytest<=4.6'],
        test_suite='VirtualMicrobes.tests.test_VirtualMicrobes',
        ext_modules=get_ext_modules(),
        scripts = [os.path.join('src','VirtualMicrobes','simulation','virtualmicrobes.py'),
                   os.path.join('src','VirtualMicrobes','simulation','start.py')],
        cmdclass = cmdclass,
        command_options=command_options,
        extras_require={'testing': ['pytest<=4.6']},
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Unix',
            'Operating System :: POSIX',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Cython',
            'Topic :: Scientific/Engineering :: Artificial Life',
            'Topic :: Scientific/Engineering'
                    ],
    )
    os.chdir(curdir)
    if len(args):
        sys.argv = orig_sys_argv


if __name__ == "__main__":
    do_setup()
