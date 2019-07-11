import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="NBA-Python",
    version="0.0.1",
    author="Lucas H. Xu",
    author_email="lucasxu.pub@gmail.com",
    description="A Python Client of NBA Stats API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xuhang57/NBA-Python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
