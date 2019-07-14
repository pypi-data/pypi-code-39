############################################################################################
#
# Software:      iotJumpWay MQTT Python Clients
# Author:        Adam Milton-Barker (AdamMiltonBarker.com)
# License:       Eclipse Public License 2.0
#
# Title:         iotJumpWay MQTT Python JumpWayApp Client
# Description:   An iotJumpWay MQTT Python JumpWayApp Client that allows you to connect
#                to the iotJumpWay.
# Last Modified: 2019-04-07
#
############################################################################################

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='JumpWayMQTT',
    version="0.1.4",
    author='Adam Milton-Barker',
    author_email='adammiltonbarker@gmail.com',
    url='https://github.com/AdamMiltonBarker/JumpWayMQTT',
    license='Eclipse Public License - v 2.0',
    description='Python MQTT module that allows developers to communicate with iotJumpWay MQTT PaaS',
    packages=find_packages(),
    package_data={'': ['*.pem']},
    install_requires=[
        "paho-mqtt >= 1.2",
    ],
    classifiers=[],
)
