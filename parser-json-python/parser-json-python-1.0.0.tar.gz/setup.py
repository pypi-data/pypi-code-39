import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="parser-json-python",
    version="1.0.0",
    author="Eugene Mozge",
    author_email="eumozge@gmail.com",
    description="The parser which can get dict with strings and convert them to Python types like int, float, date, list etc. It can be useful for parsing request params via API.",
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
