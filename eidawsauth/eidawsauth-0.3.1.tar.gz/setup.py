from io import open
from setuptools import setup, find_packages
from eidawsauth.version import __version__

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='eidawsauth',
    version=__version__,
    description='Implement /auth for EIDA',
    long_description=readme,
    long_description_content_type="text/markdown",
    author='Jonathan Schaeffer',
    author_email='jonathan.schaeffer@univ-grenoble-alpes.fr',
    maintainer='Jonathan Schaeffer',
    maintainer_email='jonathan.schaeffer@univ-grenoble-alpes.fr',
    url='https://gitlab.com/resif/ws-eidaauth',
    license='GPL-3.0',
    packages=find_packages(),
    install_requires=[
    'Flask==1.0.2', 'psycopg2-binary==2.7.7', 'python-gnupg==0.4.4'
    ],
    keywords=[
        '',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    tests_require=['coverage', 'pytest', 'pytest-datafiles', 'tox'],
    #entry_points='''
    #[console_scripts]
    #ringserverstats=ringserverstats:cli
    #'''
)
