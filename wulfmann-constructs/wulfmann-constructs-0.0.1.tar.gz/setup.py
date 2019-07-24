import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wulfmann-constructs",
    version="0.0.1",
    author="Joe Snell",
    author_email="joepsnell@gmail.com",
    description="Example CDK Construct Library",
    long_description=long_description,
    url="https://github.com/wulfmann/constructs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
