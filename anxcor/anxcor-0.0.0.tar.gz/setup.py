import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anxcor",
    version="0.0.0",
    author="Kevin Mendoza",
    author_email='kevinmendoza@icloud.com',
    description="ANXCOR is a python library for performing seismic ambient noise crosscorrelations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uofuseismo/anxcor.git",
    packages=setuptools.find_packages(),
    install_requires = [
    'obspy>=1.1',
    'xarray>=0.12',
    'numpy>=1.16',
    'scipy>=1.0',
    'pandas>=0.24',
    'bottleneck>=1.2'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
print(setuptools.find_packages())