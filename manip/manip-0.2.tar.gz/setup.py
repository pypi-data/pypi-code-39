import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='manip',  
    version='0.2',
    author="Felipe Amaral",
    author_email="costinha.fca@gmail.com",
    description="A manipulation package to change whole folders.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Flipecs/file_manip.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )