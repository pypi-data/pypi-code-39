import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="setup_log",
    version="0.0.2",
    author="Wenbo Zhao",
    author_email="zhaowb@gmail.com",
    description="A simple log setup helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhaowb/simple_log.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
