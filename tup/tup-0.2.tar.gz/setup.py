from setuptools import setup
from tup import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='tup',
    version=__version__,
    author="Oliver Duce",
    author_email="oliver_duce@live.co.uk",
    description="CLI Telegram file uploder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Qwerty-Space/tup",
    packages=['tup'],
    install_requires=['Telethon>=1.7'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": [
                    "tup=tup.tup:main"
                    ]
                },
)