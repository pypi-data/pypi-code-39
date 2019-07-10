import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unitrans-evalir",
    version="0.0.1.6",
    author="Enrique Ortiz",
    author_email="hi.evalir@gmail.com",
    description="Parses a file with a certain structure and converts to the desired metric unit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Evalir/UniversalTranslator",
    packages=setuptools.find_packages(),
    install_requires=['Click'],
    scripts=["UniversalTranslator"],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        "Operating System :: OS Independent",
    ],
)
