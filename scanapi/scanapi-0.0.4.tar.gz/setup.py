import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scanapi",
    version="0.0.4",
    author="Camila Maia",
    author_email="cmaiacd@gmail.com",
    description="Automated Testing and Documentation for your REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/camilamaia/scanapi",
    packages=setuptools.find_packages(),
    install_requires=["requests >= 2.22.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
