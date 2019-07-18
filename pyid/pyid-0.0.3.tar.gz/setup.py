import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyid",
    version="0.0.3",
    author="Nicholas Morley",
    author_email="nick.morley111@gmail.com",
    description=" ID attributes for python objects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cyclecycle/pyid",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
