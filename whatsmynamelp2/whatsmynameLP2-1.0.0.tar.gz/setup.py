import setuptools

with open ("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup (
    name = 'whatsmynameLP2',
    version = '1.0.0',  
    author = "Lourenço Pestana",
    author_email = "luis.pestana@accenture.com",
    url = "https://github.com/loupestana/repo1.git",
    description = 'Say my name',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = ["whatsmynameLP2"],
    license = "MIT",

    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    include_package_data = True,
    
)