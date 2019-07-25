from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="aicsapi-tool-python",
    version="0.1.5",
    author="Sean (Shih-Lun) Wu",
    author_email="summer7sean@gmail.com",
    description="Toolkit for Python backend template",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/slSeanWU/aicsapi-tool-python/",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
)