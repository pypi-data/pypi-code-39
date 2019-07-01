import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyROQ",
    version="0.0.1",
    author="Hong Qi",
    author_email="hong.qi@ligo.org",
    description="PyROQ is a Python-based software that can generate reduced basis and reduced order quadrature data of gravitational wave waveforms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qihongcat/PyROQ",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


