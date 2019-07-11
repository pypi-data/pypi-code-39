import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fixar",
    version="1.0.0",
    author="Alexander Schlögl",
    author_email="alexander.schloegl@uibk.ac.at",
    description="Fixed-size integers for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alxshine/fixar",
    packages=['fixar'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
