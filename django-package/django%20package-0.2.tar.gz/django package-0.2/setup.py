from setuptools import setup, find_packages
from os import path

from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django package',
    version='0.2',
    description='django blog packaging',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/KathurimaKimathi/DjangoAWS',
    author='Kathurima Kimathi',
    author_email='kathurimakimathi415@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    install_requires=['gunicorn', 'psycopg2',
                      'django-prometheus', 'sentry-sd'],
    extras_require={
        'test': ['coverage'],
    },
)
