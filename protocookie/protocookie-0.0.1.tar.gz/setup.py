import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="protocookie",
    version="0.0.1",
    author="Denis Barov",
    author_email="dindin@dindin.ru",
    description="Proof of Concept for storing data in Fernet encrypted protobuffed cookies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fordindin/protocookie",
    packages=setuptools.find_packages(),
    package_data={'': ['protocookie.proto', 'config.json']},
    install_requires=[
                    'protobuf',
                    'flask',
                    'cryptography'
                    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
