import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Noisemap",
    version="1.0",
    author="Proximas",
    author_email="hyperhamster534@outlook.com",
    description="A simple library to generate noisemaps.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hyperhamster535.github.io/Noisemap/",
    packages=['Noisemap'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
