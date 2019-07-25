import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="esml_module_v1",
    version="0.0.1",
    author="sahil panindre",
    author_email="sahil11panindre@gmail.com",
    description="with help of this packeg image processsing code can be written in just two lines",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ultimus11/easy_ml_module",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)