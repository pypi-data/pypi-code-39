import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csv_transcriber",
    version="1.0",
    author="Jad Khalili",
    author_email="jad.khalili123@gmail.com",
    description="Breaks down a CSV file into text files containing the contents of each row.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Video-Lab/CSV-Transcriber/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)