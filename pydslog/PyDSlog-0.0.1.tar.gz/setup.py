import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyDSlog",
    version="0.0.1",
    author="SSV Software Systems gmbh",
    author_email="fbu@ssv-embedded.de",
    description="Python data-science logger for the IoT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fbussv/PyDSlog",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)