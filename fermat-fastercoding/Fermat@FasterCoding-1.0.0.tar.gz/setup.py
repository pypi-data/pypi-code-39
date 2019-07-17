import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Fermat@FasterCoding",
    version="1.0.0",
    author="FasterCoding",
    author_email="fastercodingtutorial@gmail.com",
    description="Example code for the Fermats-Little-Theorem modular inverse algorithm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FasterCoding/Fermats-Little-Theorem",
    packages=setuptools.find_packages(),
    install_requires=[
        'Euclid-FasterCoding',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)