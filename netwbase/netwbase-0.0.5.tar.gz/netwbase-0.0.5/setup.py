import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()



setuptools.setup(
    name="netwbase",
    version="0.0.5",
    author="n0nliner",
    author_email="vkusnisaharok@gmail.com",
    description="A small network DBMS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/n0nliner/netwbase",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
