import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypi_flow",
    version="19.07.4",
    author="Gabriel Rosales",
    author_email="gabriel.alejandro.rosales@gmail.com",
    description="Project Management tools for quickly creating and maintaining PYPI packages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZenosParadox/pypi-sidekick",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['grtoolkit']
)