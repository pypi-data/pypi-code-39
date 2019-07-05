import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='falconx-py',
     version='0.2',
     author="FalconX",
     author_email="support@falconx.io",
     description="The official client for the FalconX API",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/falconxio/falconx-py",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
