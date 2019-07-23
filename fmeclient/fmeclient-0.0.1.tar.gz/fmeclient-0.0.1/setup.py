import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fmeclient",
    version="0.0.1",
    author="Jakub Jarosz",
    author_email="jakub.jarosz@postpro.net",
    description="FME Server Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qba73/fmeclient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Environment :: Console",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
    ],
)