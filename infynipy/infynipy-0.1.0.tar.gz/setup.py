import os
from setuptools import find_packages, setup

from codecs import open

here = os.path.abspath(os.path.dirname(__file__))

with open('README.md', 'r') as fh:
    long_description = fh.read()

about = {}
with open(os.path.join(here, 'infynipy', '__version__.py'), 'r', 'utf-8') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=about['__url__'],
    license=about['__license__'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'requests==2.20.0',
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    setup_requires=['pytest-runner'],
    tests_require=[
        "pytest >=5.0.1",
        "python-dotenv >=0.10.3",
        "vcrpy >=2.0.1",
    ],
    test_suite="tests",
)
