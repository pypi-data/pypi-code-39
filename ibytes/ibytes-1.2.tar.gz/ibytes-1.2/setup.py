import sys
import setuptools
from distutils.core import setup, Extension

module1 = Extension('ibytes',
                    sources=['_ibytes.c'],
                    )

setup(name='ibytes',
      version='1.2',
      description="Network stream processing tools",
      packages=["ibytes"],
      author="scp10011",
      author_email="circlelbw@hotmail.com",
      long_description=(
          "User-friendly processing of byte stream message such as SSL DNS"
      ),
      url="https://github.com/scp10011/ibytes",
      data_files=[
          (
              'shared/typehints/python{}.{}/ibytes'.format(*sys.version_info[:2]),
              ["ibytes/__init__.pyi"]
          ),
      ],
      ext_modules=[module1])
