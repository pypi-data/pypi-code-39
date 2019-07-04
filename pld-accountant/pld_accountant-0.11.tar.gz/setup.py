import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pld_accountant",
    version="0.11",
    author="Antti Koskela",
    author_email="anttik123@gmail.com",
    description="PLD accountant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DPBayes/PLD-Accountant",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
