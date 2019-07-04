import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="shale",
    version="0.0.1",
    author="Teguh Hofstee",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    # url="https://github.com/thofstee/shale",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
