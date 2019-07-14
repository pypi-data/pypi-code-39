#!/usr/bin/env python

import os
from setuptools import setup, find_packages


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    orig_content = open(os.path.join(os.path.dirname(__file__), fname)).readlines()
    content = ""
    in_raw_directive = 0
    for line in orig_content:
        if in_raw_directive:
            if not line.strip():
                in_raw_directive = in_raw_directive - 1
            continue
        elif line.strip() == '.. raw:: latex':
            in_raw_directive = 2
            continue
        content += line
    return content


core_dependencies = [
    'pysamloader',
    'cython',
    'kivy'
]

install_requires = core_dependencies + ['wheel']

setup_requires = ['setuptools_scm']

doc_requires = setup_requires + ['sphinx', 'sphinx-argparse', 'sphinxcontrib-documentedlist', 'alabaster']

test_requires = doc_requires + ['pytest', 'pytest-cov', 'coveralls[yaml]']

build_requires = test_requires + ['doit', 'pyinstaller']

publish_requires = build_requires + ['twine', 'pygithub']

setup(
    name="pysamloader-gui",
    use_scm_version={"root": ".", "relative_to": __file__},
    author="Chintalagiri Shashank",
    author_email="shashank@chintal.in",
    description="Kivy GUI for pysamloader",
    keywords="utilities",
    url="https://github.com/ebs-universe/pysamloader-gui",
    project_urls={
        'Source Repository': 'https://github.com/ebs-universe/pysamloader-gui/',
        'Documentation': 'https://pysamloader-gui.readthedocs.io/en/latest/index.html',
        'Issue Tracker': 'https://github.com/ebs-universe/pysamloader-gui/issues',
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Embedded Systems",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Environment :: Console",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    python_requires='>=3.4',
    install_requires=install_requires,
    setup_requires=setup_requires,
    extras_require={
        'docs': doc_requires,
        'tests': test_requires,
        'build': build_requires,
        'publish': publish_requires,
        'dev': build_requires,
    },
    platforms='any',
    entry_points={
        'console_scripts': [
            'pysamloader-gui=pysamloader_gui.app:main',
        ],
    },
    include_package_data=True,
)
