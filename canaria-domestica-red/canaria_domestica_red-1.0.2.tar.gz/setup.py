import setuptools
import sys

if sys.argv[1] != "sdist":
    print("Croak!")
    exit(1)

setuptools.setup(
    name="canaria_domestica_red",
    version="1.0.2",
    url="https://github.com/apljungquist/tox-constraints",
    license="MIT",
    author="AP Ljungquist",
    author_email="ap@ljungquist.eu",
    description="A simple package that works in some versions and is broken in others",
    classifiers=["License :: OSI Approved :: MIT License"],
    py_modules=["canaria_domestica_red"],
    entry_points={
        "console_scripts": ["canaria_domestica_red = canaria_domestica_red:main"],
    },
)
