
import setuptools

setuptools.setup(
    name="overseer_slave",
    py_modules=["slave"],
    version="1",
    author="Gleb Fedorov",
    author_email="vdrhtc@gmail.com",
    description="General interface for an Overseer slave",
    long_description='''In this package, an abstract class is defined to facilitate the 
                        creation of various monitoring clients. It implements the data transfer 
                        layer between the client and Overseer''',
    long_description_content_type="text/markdown",
    url="https://github.com/vdrhtc/overseer-slave",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
