import os
import setuptools
import jt64common

here = os.path.dirname(os.path.abspath(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=jt64common.__title__,
    version=jt64common.__version__,
    author=jt64common.__author__,
    license=jt64common.__license__,
    author_email=jt64common.__email__,
    long_description=long_description,
    long_description_content_type="text/markdown",

    python_requires='>=3.5.*',
    project_urls={
        'Documentation': 'https://ki7mt.github.io/jtsdk-tools/',
    },
    packages=setuptools.find_packages(),
    py_modules=['help', 'messages', 'utils'],
    install_requires=['colorconsole'],
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        ],
    url='https://github.com/KI7MT/jtsdk64-tools/tree/master/src/python/jtsdk64-common',
)
