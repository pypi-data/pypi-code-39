import setuptools

from fiducialary import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fiducialary",
    version=__version__,
    author="Luke Miller",
    author_email="dodgyville@gmail.com",
    description="Module for generating circular fiducial markers for use in imaging systems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/dodgyville/fiducialary",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pycairo",
    ],
    python_requires=">=3.6",

)
