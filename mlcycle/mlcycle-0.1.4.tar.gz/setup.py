import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
elif os.environ.get('CI_JOB_ID'):
    version = os.environ['CI_JOB_ID']
else:
    version = "0.0.1"

setuptools.setup(
    name="mlcycle",
    version=version,
    url="http://git01-ifm-min.ad.fh-bielefeld.de/pvserve2/mlcycle",
    author="Cem Basoglu",
    author_email="cem.basoglu@fh-bielefeld.de",
    description="MLCycle client library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ]
)
