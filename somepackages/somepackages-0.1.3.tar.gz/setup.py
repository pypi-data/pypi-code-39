import setuptools
from setuptools.command.install import install as InstallCommand

setuptools.setup(

    name='somepackages',
    version='0.1.3',
    author="gelleson",
    author_email="go.gelleson@gmail.com",
    description="It is just utils",
    long_description_content_type="text/markdown",
    url="https://github.com/javatechy/dokr",
    packages=setuptools.find_packages(),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
