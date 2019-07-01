import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yaphs",
    version="1.0",
    author="Corentin CAM",
    author_email="cam.corentin@gmail.com",
    description="Yet another python hook system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/valtrok/yaphs",
    packages=setuptools.find_packages(),
    project_urls={
        "Source Code": "https://gitlab.com/valtrok/yaphs"
    },
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)