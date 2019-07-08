import os
import sys
import codecs
from setuptools import setup
from setuptools.command.install import install

VERSION = '0.1.2'

# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

class VerifyVersionCommand(install):
    """Verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG', '')

        if not tag.endswith(VERSION, 1):
            info = "Git tag: {0} does not match the version of auger-cli: {1}".format(
                tag, VERSION
            )
            sys.exit(info)

install_requires = [
    'click',
    'requests',
    'shortuuid',
    'auger-hub-api-client>=0.5.6',
    'ruamel.yaml',
]

extras = {
    'testing': ['pytest', 'pytest-cov', 'pytest-xdist', 'flake8', 'mock']
}

# Meta dependency groups.
all_deps = []
for group_name in extras:
    all_deps += extras[group_name]
extras['all'] = all_deps

setup(
    name='auger.ai',
    version=VERSION,
    description='Auger python and command line interface package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Deep Learn, Inc.',
    author_email='augerai@dplrn.com',
    url='https://github.com/deeplearninc/auger-ai',
    license='MIT',
    zip_safe=False,
    platforms='any',
    test_suite='tests',
    python_requires='>=3',
    keywords='augerai auger ai machine learning automl deeplearn api sdk',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        "Intended Audience :: System Administrators",
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3 :: Only"
    ],
    install_requires=install_requires,
    extras_require=extras,
    entry_points={
        'console_scripts': [
            'augerai=auger.cli.cli:cli'
        ]
    },
    cmdclass={
        'verify': VerifyVersionCommand
    },
    packages=['auger.cli', 'auger.api']
)
