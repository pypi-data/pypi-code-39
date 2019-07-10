import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="touhou-ura",
    version="0.0.1",
    author="blackrose514",
    author_email="dmtri3sukuna@gmail.com",
    license='MIT',
    description="Python tool to get or/and download data from touhou-ura threads (futaba)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blackrose514/touhou-ura",
    download_url="https://github.com/blackrose514/touhou-ura/releases",
    packages=setuptools.find_packages(),
    install_requires=['requests', 'tqdm', 'beautifulsoup4'],
    include_package_data=True,
    keywords=['touhou', 'futaba', '4chan'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)