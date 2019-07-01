import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jlight-jochenj",
    version="0.0.1",
    author="Jochen Jägers",
    author_email="",
    description="classes for accessing JLight lamps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jochenjagers/jlight",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)