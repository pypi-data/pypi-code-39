import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biliget",
    version="1.3.9",
    author="lixiaobai",
    author_email="18108274905@163.com",
    description="Help with bilibili.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lixiaobai468/biliget",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests',
        'matplotlib',
    ],
)
