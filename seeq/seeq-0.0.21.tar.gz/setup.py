import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="seeq",
    version="0.0.21",
    author="Seeq Corporation",
    author_email="support@seeq.com",
    description="The Seeq SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.seeq.com",
    packages=setuptools.find_packages(),
    install_requires=[
        'ipython~=5.8.0',  # For Python 2 compatibility
        'numpy~=1.16.4',  # For Python 2 compatibility
        'pandas~=0.22.0',  # For Python 2 compatibility
        'matplotlib',
        'certifi',
        'six',
        'urllib3'
    ],
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
)
