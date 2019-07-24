import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dataglove",
    version="0.0.5",
    author="BeBop Sensors",
    author_email="code@bebopsensors.com",
    description="Python Module of the DataGlove API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="",
    packages=["dataglove"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
	include_package_data=True,
	package_data={"dataglove": ['DataGloveHID.dll']},
)
