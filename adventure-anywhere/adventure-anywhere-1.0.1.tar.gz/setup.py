from setuptools import find_packages, setup

with open("README.md", "r") as readme:
    long_description = readme.read()

setup(
    name="adventure-anywhere",
    version="1.0.1",
    description="Port of the 1977 ADVENTURE game that supports long-running sessions amongst multiple players.",
    url="https://github.com/zhammer/adventure-anywhere",
    author="Zach Hammer",
    author_email="zach.the.hammer@gmail.com",
    license="MIT License",
    packages=find_packages(),
    install_requires=["adventure"],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
