from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
     name='indigochemo',  
     version='0.1',
     include_package_data=True,
     scripts=['indigochem/indigo.py'] ,
     author="Deepak Kumar",
     author_email="",
     description="Indigo chemoinformatics packaged for pip. Software and all rights owned by EPAM (https://lifescience.opensource.epam.com).",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="",
     packages=find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )