import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="read-me-dot-py",
    version="v0.0.1",
    author="ronald",
    author_email="ronald-farias@outlook.com",
    description="My Awesome project!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ronald-TR/read-me-dot-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
