import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="jarvis-cmd",
    version="0.0.2",
    description="CLI To Make Your Life Easier",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Vijayaraghavan Sundararaman",
    author_email="vijaygenius123@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["jarvis"],
    include_package_data=True,
    install_requires=["Click", "configparser", "requests","PyInquirer"],
    entry_points={
        "console_scripts": [
            "jarvis=jarvis.__main__:main",
        ]
    },
)
