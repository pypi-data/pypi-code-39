import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypulseq",
    version="1.0.0",
    author="Keerthi Sravan Ravi",
    author_email="ks3621@columbia.edu",
    description="Pulseq in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imr-framework/pypulseq",
    packages=setuptools.find_packages(exclude=['pypulseq.utils', 'pypulseq.examples']),
    install_requires=['numpy', 'matplotlib'],
    license='License :: OSI Approved :: GNU Affero General Public License v3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
)
