import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pythonUtilities",
    version="0.0.1",
    author="Gaurav Shimpi",
    author_email="shimpigaurav0@gmail.com",
    description="Python utilities which makes your work with Pandas easy and effective.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gauravshimpi/python_pandas_utilities",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)