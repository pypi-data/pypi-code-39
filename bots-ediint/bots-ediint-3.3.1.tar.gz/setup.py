# -*- coding: utf-8 -*-

"""
Setup for Bots open source EDI translator
"""
import os
import platform
import setuptools
import sys


setup_dir = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(setup_dir, 'bots', '__about__.py')) as f:
    exec(f.read(), about)

long_description = """Bots is complete software for edi (Electronic Data Interchange):
    - translate:
        All major edi data formats are supported: edifact, x12, tradacoms, xml, json, flat
    - communicate:
        http, ftp, email and custom made
"""
test_suite = 'tests.run_unitests'

setup_requires = [
    'setuptools',
]

if len(sys.argv) > 1 and 'pytest' in sys.argv[1:]:
    setup_requires.append('pytest-runner')

install_requires = [
    'Django>=1.10',
    'cheroot',
    'Cherrypy',
]

tests_require = [
    'pytest',
    'pytest-cov',
    'pytest-django',
]

extras_require = {
    'docs': [
        'sphinx',
        'sphinx_rtd_theme',
    ],
    'tools': [
        'Genshi',    # for using templates/mapping to HTML)
        'paramiko',  # SFTP
        'pdfminer',  # parse pdf-files
        'xlrd',      # parse excel-files
    ],

    # Tests
    'testing': tests_require,

    ':python_version <= "3.4"': ['Cherrypy==16.0.3'],
    ':python_version == "3.4"': ['django<2.1'],
    # OS dependencies
    ':sys_platform == "linux" or sys_platform == "linux2"': ['pyinotify'],
    ':sys_platform == "win32" and python_version != "3.4"': ['pywin32'],
    ':sys_platform == "win32" and python_version == "3.4"': ['pypiwin32==219'],
}

scripts = []

python_requires = '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4'

# Add specific bdist_
if len(sys.argv) > 1 and 'bdist_wininst' in sys.argv[1:] or 'bdist_msi' in sys.argv[1:]:
    scripts.append('postinstall-bots-win.py')


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Topic :: Office/Business',
    'Topic :: Office/Business :: Financial',
    'Topic :: Other/Nonlisted Topic',
    'Topic :: Communications',
    'Environment :: Console',
    'Environment :: Web Environment',
]

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__url__'],
    long_description=long_description,
    platforms='OS Independent (Written in an interpreted language)',
    license=about['__license__'],
    keywords='edi edifact x12 tradacoms xml fixedfile csv',
    packages=setuptools.find_packages(where='.', exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    python_requires=python_requires,
    classifiers=classifiers,
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite=test_suite,
    extras_require=extras_require,
    scripts=scripts,
    entry_points={
        'console_scripts': [
            'bots-dirmonitor = bots.dirmonitor:start',
            'bots-engine = bots.engine:start',
            'bots-engine2 = bots.engine:start',
            'bots-grammarcheck = bots.grammarcheck:start',
            'bots-job2queue = bots.job2queue:start',
            'bots-jobqueueserver = bots.jobqueueserver:start',
            'bots-plugoutindex = bots.plugoutindex:start',
            'bots-updatedb = bots.updatedb:start',
            'bots-webserver = bots.webserver:start',
            'bots-xml2botsgrammar = bots.xml2botsgrammar:start',
        ]
    },
    project_urls={
        'Bug Reports': 'https://gitlab.com/bots-ediint/bots/issues',
        # 'Funding': '',
        # 'Say Thanks!': '',
        'Source': about['__url__'],
    },
)
