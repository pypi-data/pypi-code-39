import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kvs3",
    version="0.0.5",
    author="Nic Cheneweth",
    author_email="nic.cheneweth@thoughtworks.com",
    description="Command-line tool to interact with s3 bucket as a key/value store",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ncheneweth/kvs3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=['invoke', 'boto3', 'pyyaml', 'requests'],
    entry_points={
        'console_scripts': ['kvs3 = kvs3.main:program.run']
    }
)