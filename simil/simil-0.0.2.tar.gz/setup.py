import setuptools

with open("README.md", "r") as readme:
    LONG_DESCRIPTION = readme.read()

setuptools.setup(
    name="simil",
    version="0.0.2",
    author="Benjamin Fox",
    author_email="foxbenjaminfox@gmail.com",
    description="CLI for semantic string similarity",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/foxbenjaminfox/string-similarity-cli",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    install_requires=[
        "rpyc",
        "spacy",
    ],
    entry_points={"console_scripts": ["simil=simil:main"]},
)
