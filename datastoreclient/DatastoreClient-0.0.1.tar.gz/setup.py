import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DatastoreClient",
    version="0.0.1",
    author="李彦宏",
    author_email="liyanhong@hz-health.cn",
    description="Python Client for Datastore APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)