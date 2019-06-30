import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cc-pathlib",
    version="0.0.3",
    author="Yoochan",
    author_email="yota.news@gmail.com",
    description="an extended version of pathlib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/yoochan/pypi-ccpathlib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
		"Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
		"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
)