from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(

    name='easylogging2',

    version='2.0.1',

    description='Simple Python logging lib',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/AI35/easylogging2',

    author='ALI B OTHMAN',

    author_email='alosh.othman55@gmail.com',

    license='GNU v3.0',
    
    packages=['easylogging2'],
    
    keywords='logging logger log python',

    python_requires='>=3',

    install_requires=[
        "configparser >= 3.5.0",
    ],

    project_urls={
        'Bug Reports': 'https://github.com/AI35/easylogging2/issues',
        'Source': 'https://github.com/AI35/easylogging2',
    },
)
