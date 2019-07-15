import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="whatsmynamejx1",
    version="1.0.0",
    author="Jin Xin",
    author_email="jin.xin@accenture.com",
    description="Say my name",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jinxin07/whatsmyname",
    packages=["whatsmynamejx1"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)