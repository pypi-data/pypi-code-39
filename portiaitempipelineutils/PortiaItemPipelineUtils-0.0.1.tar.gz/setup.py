import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PortiaItemPipelineUtils",
    version="0.0.1",
    license='MIT License',
    author="Asiel Lara",
    author_email="asiel.lb@gmail.com",
    description="Scrapy portia pipeline which allow you to do items related stuff.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asiellb/portia-item-pipeline-utils.git",
    download_url='https://github.com/asiellb/portia-item-pipeline-utils/tarball/master',
    keywords='scrapy portia item pipeline utils',
    packages=setuptools.find_packages(),
    platforms=['Any'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: No Input/Output (Daemon)",
    ],
)