from setuptools import setup

setup(
    name='smart-integration-utils',
    version='1.0',
    install_requires = [
        'Django>=2.0.7',
            'djangorestframework>=3.8.2',
            'psycopg2-binary>=2.7.4',
            'pytz==2018.4',
            'requests>=2.18.2',
            'six==1.11.0',
            'boto==2.49.0',
            'boto3==1.7.54',
            'django-storages==1.6.6',
            'django-cors-headers==2.4.0',
            'eventmonitoring-client',
    ],
)