import setuptools
from os import path

here = path.abspath(path.dirname(__file__))

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()
   
setuptools.setup(
    name="ichingshifa",
    version="3.0.9",
    author="Ken Tang",
    author_email="kinyeah@gmail.com",
    description="A package of iching stalk divination in Traditional Chinese Language. Python周易筮法，起卦不求人。",
	long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kentang2017/iching_shifa",
    packages=setuptools.find_packages(),
	data_files = [('ichingshifa',['ichingshifa/sixtyfourgua.pkl']), ('ichingshifa',['ichingshifa/sixtyfourgua_description.pkl'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

