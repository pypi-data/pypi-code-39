import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reqREST",
    version="0.0.1",
    author="Rory Murdock",
    author_email="rory@itmatic.com.au",
    description="A REST API wrapper for requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rorymurdock/reqREST",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
          'requests',
    ],
)