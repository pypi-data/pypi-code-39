import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cups",
    version="0.0.2",
    author="Xavier Mabras",
    author_email="xavier.mabras@protonmail.ch",
    description="A simple cups generator library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xafardero/cups",
    download_url = 'https://github.com/xafardero/cups/tarball/0.0.1',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
)
