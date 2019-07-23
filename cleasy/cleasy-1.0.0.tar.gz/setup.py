import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cleasy",
    version="1.0.0",
    author="Sergii Bibikov",
    author_email="sergeport@gmail.com",
    description="Simple CLI shell",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/sergeport/cleasy",
    packages=setuptools.find_packages(),
    install_requires=["PyInquirer==1.0.3"],
    extras_require={
        'prettyfy_output': ["termcolor==1.1.0", "pyfiglet==0.8.post1"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)