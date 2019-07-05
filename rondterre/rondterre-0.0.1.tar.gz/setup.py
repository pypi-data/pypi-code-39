import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rondterre",
    version="0.0.1",
    author="theodoric008",
    author_email="liujiashu2333@qq.com",
    description="Some personal python3 snippet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Theodoric008",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
