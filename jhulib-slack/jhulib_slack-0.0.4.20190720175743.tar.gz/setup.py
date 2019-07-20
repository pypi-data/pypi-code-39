import setuptools
import datetime
import os

now = datetime.datetime.now()
datestring = now.strftime("%Y%m%d%H%M%S")
version_file = open(os.path.join("slack_api", 'VERSION'))
version = version_file.read().strip()

setuptools.setup(
    name="jhulib_slack",
    version=f"{version}.{datestring}",
    author="Derek Belrose",
    author_email="dbelrose@jhu.edu",
    description=("A python implementation of the slack API including SCIM"),
    license="Apache",
    keywords="slack api scim",
    url="https://github.com/jhu-sheridan-libraries/python_slack_api",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ]
)
