import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quick-cd",
    version="1.1.1",
    author="HalfTough",
    author_email="halftough29A@gmail.com",
    description="Save working directory under label and cd into it quickly.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/halftough/quick-cd",
    packages=['quick_cd'],
    scripts=['bin/qcd'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
)