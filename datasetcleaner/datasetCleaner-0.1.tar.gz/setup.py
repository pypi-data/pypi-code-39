import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datasetCleaner",
    version="0.1",
    author="Félix Lopez",
    author_email="feloxlopez05@gmail.com",
    description="A dataset cleaner for pictures",
    url="https://github.com/felop/datasetCleaner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
