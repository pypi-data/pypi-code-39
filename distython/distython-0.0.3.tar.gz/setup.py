import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="distython",
    version="0.0.3",
    author="Kacper Kubara",
    author_email="kacper.kubara.ai@gmail.com",
    description="Implementation of state-of-the-art distance metrics from research papers which can handle mixed-type data and missing values.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KacperKubara/distython",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
