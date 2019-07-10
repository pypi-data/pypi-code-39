import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parser-json-python",
    version="0.1.0",
    author="Eugene Mozge",
    author_email="eumozge@gmail.com",
    description="The parser which can get json and convert values to Python types.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eumozge/parser-json-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
