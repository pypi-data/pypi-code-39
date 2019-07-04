import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drsip-common",
    version="0.5",
    author="Justin Chan",
    author_email="capslockwizard@gmail.com",
    description="Common helper functions for DR-SIP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/capslockwizard/drsip-common",
    packages=['drsip_common'],
    install_requires=['biopython', 'numpy'],
    classifiers=[
        "Environment :: Plugins",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
)
