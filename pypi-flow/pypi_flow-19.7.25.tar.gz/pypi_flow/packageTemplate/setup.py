import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="$package-name$",
    version="0.0.0",
    author="$author$",
    author_email="$email$",
    description="$description$",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="$url$",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)