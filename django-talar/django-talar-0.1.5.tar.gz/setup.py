import setuptools

import talar

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-talar",
    version=".".join(str(i) for i in talar.VERSION),
    author="Talar",
    author_email="kamil.obstawski@rakki.xyz",
    description="Django app for [Talar.app](https://talar.app) service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rakki-software/django-talar/src/",
    packages=setuptools.find_packages(),
    install_requires=[
        'django >=2.1,<2.2', 'djangorestframework >=3.9,<4.0',
        'M2Crypto >=0.30,<0.40',
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
