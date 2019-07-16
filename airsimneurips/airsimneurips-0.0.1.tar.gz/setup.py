import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="airsimneurips",
    version="0.0.1",
    author="Ratnesh Madaan, Matthew Brown, Nicholas Gyde, Shital Shah",
    author_email="ramadaan@microsoft.com, v-mattbr@microsoft.com, v-nigyde@microsoft.com, shitals@microsoft.com",
    description="Python package for Game of Drones - A NeurIPS 2019 Competition, built on Microsoft AirSim - an open source simulator based on Unreal Engine for autonomous vehicles from Microsoft AI & Research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microsoft/AirSim-NeurIPS2019-Drone-Racing",
    packages=setuptools.find_packages(),
	license='MIT',
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
          'msgpack-rpc-python', 'numpy'
    ]
)
