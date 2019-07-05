"""setup.py"""
from setuptools import setup, find_packages
from asciimap import __version__


def readme():
    """Parse README.md

    : returns: README.md as string
    """
    with open("README.md") as file_handle:
        return file_handle.read()


setup(
    name="asciimap",
    version=__version__,
    description="Print countries in ASCII Art based on Natural Earth shape files.",
    long_description=readme(),
    long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
    keywords=("earth country print ascii art python spatial geo natural"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Education",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Topic :: Scientific/Engineering :: GIS",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities",
    ],
    install_requires=["numpy>=1.15.1,<2.0.0"],
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["asciimap = asciimap.__main__:main"]},
    url="https://github.com/MaelStor/asciimap",
    author="Mael Stor",
    author_email="maelstor@posteo.de",
    license="GPL-3.0-or-later",
    zip_safe=False,
)
