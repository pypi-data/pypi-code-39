import os
import re
from setuptools import setup, find_packages

with open('README.rst') as fh:
    readme = fh.read()

with open(os.path.join('madx', '__init__.py')) as fh:
    version = re.search("^__version__ = '([0-9]+[.][0-9]+([.][0-9]+)?)'$", fh.read(), re.MULTILINE).group(1)

setup(
    name='madx',
    version=version,
    description='',
    long_description=readme,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Physics',
    ],
    keywords=['MADX', 'framework', 'interface', 'accelerator'],
    url='https://gitlab.com/Dominik1123/madx',
    author='Dominik Vilsmeier',
    author_email='d.vilsmeier@gsi.de',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
    python_requires='>=3.7',
)
