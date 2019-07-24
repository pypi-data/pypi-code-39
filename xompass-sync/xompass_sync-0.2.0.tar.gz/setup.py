import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='xompass_sync',
    version='0.2.0',
    author="Rodolfo Castillo Mateluna",
    author_email="rodolfocastillomateluna@gmail.com",
    description="Xompass Asset/Sensor sync library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rcastill/xompass-fc-sync",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)
