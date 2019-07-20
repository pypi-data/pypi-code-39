from distutils.core import setup, Extension
import os

version = os.environ.get('PYDINEMIC_VERSION')

pydinemic = Extension('pydinemic',
                      sources=['src/pydinemic/module.cpp',
                               'src/pydinemic/pyaction.cpp',
                               'src/pydinemic/pydfield.cpp',
                               'src/pydinemic/pydlist.cpp',
                               'src/pydinemic/pydmodel.cpp'],
                      include_dirs=['/usr/include'],
                      library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                      runtime_library_dirs=['/usr/lib/x86_64-linux-gnu/'],
                      libraries=['boost_python3', 'dinemic'])

setup(name='pydinemic',
      version='19.07.1',
      author='cloudover.io ltd.',
      description='Dinemic framework for python',
      package_dir={'': 'src'},
      packages=['pkg'],
      ext_modules=[pydinemic])
