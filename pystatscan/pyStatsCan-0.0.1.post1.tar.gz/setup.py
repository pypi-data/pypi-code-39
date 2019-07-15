import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyStatsCan",
    version="0.0.1.post1",
    author="Philippe Allard-Rousse",
    author_email="philrousse@gmail.com",
    description="A python wrapper for Statistics Canada Web Data Services API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DelBiss/pyStatsCan",
    packages=setuptools.find_packages(),
    license= "Apache 2.0",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)