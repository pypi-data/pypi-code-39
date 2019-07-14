import io
import pathlib
import re
import setuptools

# version load courtesy:
# https://stackoverflow.com/questions/17583443/what-is-the-correct-way-to-share-package-version-with-setup-py-and-the-package
here = pathlib.Path(__file__).parent
__version__ = re.search(
    r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
    io.open(here / 'fiducialary' / '__init__.py', encoding='utf_8_sig').read()
    ).group(1)


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
