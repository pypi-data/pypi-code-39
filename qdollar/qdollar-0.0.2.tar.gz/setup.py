import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qdollar",
    version="0.0.2",
    author="Prashant Shakya",
    author_email="prashushakya@gmail.com",
    description="qdollar is the Python Implementation of $Q Super-Quick Recognizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shakyaprashant/qdollar",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)