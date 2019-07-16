# setup.py
# Usage: ``python _setup_for_tifffile_C_extension.py build_ext --inplace``
from distutils.core import setup, Extension
import numpy
setup(name='_tifffile',
      ext_modules=[Extension('_tifffile', ['tifffile.c'],
                             include_dirs=[numpy.get_include()])])
