from setuptools import Extension, setup

ext = Extension(
    name='pyprojector',
    sources=['pyprojector.cpp', 'res/pyprojector.rc', 'deps/miniz.c'],
    libraries=['Comdlg32', 'Gdi32', 'OpenGL32', 'Shell32', 'User32'],
    include_dirs=['deps'],
)

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pyprojector',
    version='1.0.0',
    description='pyprojector is an asyncronous window for rendering',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cprogrammer1994/pyprojector',
    author='Szabolcs Dombi',
    author_email='cprogrammer1994@gmail.com',
    license='MIT',
    ext_modules=[ext],
)
