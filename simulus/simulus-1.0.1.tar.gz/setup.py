import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simulus",
    version="1.0.1",
    author="Jason Liu",
    author_email="jasonxliu2010@gmail.com",
    description="A discrete-event simulator in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://people.cis.fiu.edu/liux/research/simulus/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
