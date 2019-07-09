import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lamdadatadwightc",
    version="0.0.2",
    author="Dwight Churchill",
    author_email="dwight.a.churchill@gmail.com",
    description="Simple package to check nulls in your Pandas DataFrame and split datetimes into separate columns!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/dwightchurchill/lambdadwight/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)