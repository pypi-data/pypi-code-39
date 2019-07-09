import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DatastoreClient",
    version="0.0.4",
    author="TaylorHere",
    author_email="liyanhong@hz-health.cn",
    description="Python Client for Datastore APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TaylorHere",
    packages=setuptools.find_packages(),
    package_data={'DatastoreClient.graphql': ['*.graphql']},
    include_package_data=True,
    install_requires=['graphqlclient', 'minio', 'jinja2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)