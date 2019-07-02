import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytelematics-oasa",
    version="0.0.1",
    author="blackrose514",
    author_email="dmtri3sukuna@gmail.com",
    license='MIT',
    description="OASA Telematics API wrapper for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blackrose514/pytelematics-oasa",
    download_url = "https://github.com/blackrose514/pytelematics-oasa/releases",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    keywords = ['oasa', 'telematics', 'api', 'pytelematics-oasa'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)