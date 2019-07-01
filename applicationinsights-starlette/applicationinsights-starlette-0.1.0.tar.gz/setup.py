import os
import setuptools


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='applicationinsights-starlette',
    version='0.1.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['applicationinsights_starlette'],
    install_requires=[
        'applicationinsights>=0.11,<1',
        'starlette>=0.12.0,<1',
    ]
)
