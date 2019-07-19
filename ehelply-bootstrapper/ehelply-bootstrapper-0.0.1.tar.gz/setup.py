from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ehelply-bootstrapper',
    packages=find_packages(),  # this must be the same as the name above
    version='0.0.1',
    description='eHelply Bootstrapper',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shawn Clake',
    author_email='shawn.clake@gmail.com',
    url='https://github.com/ehelply/Bootstrapper',
    keywords=[],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'pika',
        'librabbitmq',
        'kombu',
        'pydantic',
        'pymlconf',
        'fastapi',
        'pymongo',
        'redis',
        'python-socketio',
        'email-validator',
        'uvicorn',
        'pprint',
        'pyjwt',
        'passlib[bcrypt]',
        'pytest',
        'python-multipart',
        'requests',
        'sentry-asgi',
        'python_dateutil == 2.6.0',
        'six',
        'boto3',
        'ehelply-logger>=0.0.3',
    ],

)