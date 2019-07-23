import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="falcon_json_rpc",
    version="1.0.0",
    author="Sergii Bibikov",
    author_email="sergeport@gmail.com",
    description="JsonRpc extension for Falcon",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/sergeport/falcon_json_rpc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)