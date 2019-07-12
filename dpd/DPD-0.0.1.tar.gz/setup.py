import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DPD",
    version="0.0.1",
    author="Sergio Peignier",
    author_email="sergio.peignier@insa-lyon.fr",
    description="Dendrogram Prototypical Discourse generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'nltk',
        'gensim',
        'sklearn',
        'scipy',
        'matplotlib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
)

print(setuptools.find_packages())
