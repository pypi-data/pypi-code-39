import os
import codecs
import glob
from setuptools import setup, find_packages

# The directory containing this file
here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="esncli",
    version="1.4.0",
    description="ESN command line interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="LINAGORA",
    author_email="team-openpaas-saas@linagora.com",
    license="GNU AGPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    install_requires = ['argtoolbox==0.1.3',
                        'requests==2.21.0',
                        'requests-toolbelt==0.9.1'
                        ],
    scripts = glob.glob('bin/*'),
)