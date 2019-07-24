import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dataglove",
    version="0.0.2",
    author="BeBop Sensors",
    author_email="code@bebopsensors.com",
    description="Python Module of the DataGlove API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
