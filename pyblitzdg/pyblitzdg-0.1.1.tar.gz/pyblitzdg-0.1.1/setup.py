import setuptools
from distutils.core import Extension


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='pyblitzdg',  
     version='0.1.1',
     scripts=[] ,
     author="Waterloo Quantitative Consulting Group",
     author_email="dsteinmo@wqcg.ca",
     description="Discontinuous Galerkin Finite Element Library and Solvers",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/WQCG/blitzdg",
     platforms=['linux_x86_64'],
     packages=[
         'blitzdg',
         'pyblitzdg'
     ],
     package_data={
        'blitzdg': ['libblitzdg.so'],
        'pyblitzdg': ['pyblitzdg.so']
    },
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU General Public License v3 (GPLv3)", # these might be wrong
         "Operating System :: POSIX :: Linux", # ..
     ],
 )
