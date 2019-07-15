import setuptools
from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
	
extra_packages = {
'tensorflow': ['tensorflow>=1.0.1'],
'tensorflow with gpu': ['tensorflow-gpu>=1.0.1']
},

setuptools.setup(
    name="req1161",
    version="0.0.1",
    author="Last Author",
    author_email="author@example.com",
    description="A big example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
	extra_requires=extra_packages,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	install_requires=[
          'tf',
      ],
	data_files = [ ('', ['reqL1166/file62.txt']) ],
	package_data={
        '': ['*.txt'],
        'reqL1166': ['*.txt'],
    },
)