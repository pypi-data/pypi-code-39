import setuptools
from setuptools import find_packages

with open("bedrock_client/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bdrk",
    version="0.0.1",
    author="basis-ai.com",
    author_email="contact@basis-ai.com",
    description="Client library for Bedrock platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/basisai/span",
    install_requires=["requests", "pyhcl"],
    extras_require={
        "cli": ["Click", "docker", "jsonschema"],
        "fs": ["redis", "fakeredis", "msgpack"],
    },
    packages=find_packages(".", include=["bedrock_client.*", "spanlib.*"]),
    package_data={"": ["*.hcl"], "bedrock_client": ["*.md"]},
    exclude_package_data={"bedrock_client": ["*.md"]},
    classifiers=["Programming Language :: Python :: 3"],
    entry_points={"console_scripts": ["bedrock = bedrock_client.bedrock.main:main [cli]"]},
)
