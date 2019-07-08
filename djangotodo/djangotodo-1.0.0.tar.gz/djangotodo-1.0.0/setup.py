from setuptools import setup, find_packages
from os import path

name = 'djangotodo'

setup(
    name=name,  # Required
    version='1.0.0',  # Required
    description='A sample Python project',
    long_description=open('README.md').read(), 
    url='https://pypi.org/manage/projects/{}/'.format(name),
    author='Kenneth Mathenge',  # Optional

    # Classifiers help users find your project by categorizing it.
    #
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'amqp==1.4.9'
        'anyjson==0.3.3'
        'asn1crypto==0.24.0'
        'atomicwrites==1.3.0'
        'attrs==19.1.0'
        'bcrypt==3.1.7'
        'billiard==3.3.0.23'
        'celery==3.1.18'
        'certifi==2019.6.16'
        'cffi==1.12.3'
        'chardet==3.0.4'
        'coverage==4.5.3'
        'cryptography==2.7'
        'defusedxml==0.6.0'
        'dj-database-url==0.5.0'
        'Django==2.2.3'
        'django-allauth==0.39.1'
        'django-heroku==0.3.1'
        'django-rest-auth==0.9.5'
        'djangorestframework==3.9.4'
        'entrypoints==0.3'
        'Fabric3==1.14.post1'
        'filelock==3.0.12'
        'flake8==3.7.7'
        'gunicorn==19.9.0'
        'idna==2.8'
        'importlib-metadata==0.18'
        'ipaddress==1.0.22'
        'kombu==3.0.37'
        'mccabe==0.6.1'
        'more-itertools==7.1.0'
        'oauthlib==3.0.1'
        'packaging==19.0'
        'paramiko==2.6.0'
        'pluggy==0.12.0'
        'psycopg2==2.8.3'
        'py==1.8.0'
        'pycodestyle==2.5.0'
        'pycparser==2.19'
        'pyflakes==2.1.1'
        'PyJWT==1.7.1'
        'PyNaCl==1.3.0'
        'pyparsing==2.4.0'
        'pytest==5.0.0'
        'pytest-cov==2.7.1'
        'pytest-django==3.5.1'
        'python-dateutil==2.8.0'
        'python3-openid==3.1.0'
        'pytz==2019.1'
        'redis==3.2.1'
        'requests==2.22.0'
        'requests-oauthlib==1.2.0'
        'sentry-sdk==0.9.5'
        'six==1.12.0'
        'social-auth-app-django==3.1.0'
        'social-auth-core==3.2.0'
        'sqlparse==0.3.0'
        'toml==0.10.0'
        'tox==3.13.1'
        'urllib3==1.25.3'
        'virtualenv==16.6.1'
        'wcwidth==0.1.7'
        'whitenoise==4.1.2'
        'zipp==0.5.1'

    ],  
)
