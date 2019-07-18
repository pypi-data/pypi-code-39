import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="CachedFunc",
    version="0.1",
    license='MIT',
    author="Xian Wu",
    author_email="wuxian94@pku.edu.cn",
    description="A hierarchical cache system for functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['redis'],
    test_requires=['redis', 'fakeredis'],
    url="https://github.com/FireBrother/CachedFunc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)