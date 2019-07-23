import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zabbi",
    version="0.2",
    author="Vipul Sharma",
    author_email="sharma.vips5512@gmail.com",
    description="Zabbix Python API Module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VipsSharma/Zabbix.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
