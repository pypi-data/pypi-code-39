from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
long_description = ""
if path.exists(path.join(this_directory, "README.md")):
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

setup(
    name='jiri-gitlab',
    version='0.2.3',
    packages=['jiri_gitlab'],
    url='https://gitlab.com/tom6/jiri-gitlab',
    license='MIT',
    author='Tom Forbes',
    author_email='tom@tomforb.es',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='A tool to create a Jiri manifest file from Gitlab projects',
    install_requires=[
        'python-gitlab',
        'click',
    ],
    entry_points={
        'console_scripts': [
            'jiri-gitlab = jiri_gitlab.cli:create_manifest',
            'jiri-list = jiri_gitlab.cli:list_projects',
        ],
    }
)
