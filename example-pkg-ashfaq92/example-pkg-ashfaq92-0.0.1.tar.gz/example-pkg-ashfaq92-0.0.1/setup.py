import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-ashfaq92",
    version="0.0.1",
    author="Muhammad Ashfaq",
    author_email="ashfaq92@outlook.com",
    description="A small example package",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/ashfaq92/art_framework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)