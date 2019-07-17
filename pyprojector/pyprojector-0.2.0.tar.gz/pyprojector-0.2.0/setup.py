from setuptools import Extension, setup

ext = Extension(
    name='pyprojector',
    sources=['pyprojector.cpp', 'deps/miniz.c'],
    libraries=['Comdlg32', 'Gdi32', 'OpenGL32', 'Shell32', 'User32'],
    include_dirs=['deps'],
)

setup(
    name='pyprojector',
    version='0.2.0',
    ext_modules=[ext],
)
