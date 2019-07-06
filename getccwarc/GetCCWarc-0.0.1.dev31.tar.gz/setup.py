from setuptools import setup

setup(
    setup_requires=['pbr'],
    pbr=True, install_requires=['boto3', 'botocore']
)
