import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linesample",
    version="0.1.0",
    author="Steve Matsumoto",
    author_email="stephanos.matsumoto@sporic.me",
    description="Utility to randomly sample lines from a file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/syclops/linesample",
    packages=setuptools.find_packages(),
    license="MIT",
    python_requires=">=3",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)