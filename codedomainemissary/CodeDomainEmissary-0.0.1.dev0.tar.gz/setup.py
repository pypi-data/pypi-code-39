from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["mindmeld>=4.1.1"]

setup(
    name="CodeDomainEmissary",
    version="0.0.1.dev0",
    author="Colin Lacy",
    author_email="colinjlacy@gmail.com",
    description="A package to adapt text to code domain intents and entities",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
