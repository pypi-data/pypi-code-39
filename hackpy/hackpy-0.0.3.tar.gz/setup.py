from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='hackpy',
      version='0.0.3',
      description='Full description here: https://github.com/LimerBoy/hackpy/blob/master/README.MD',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/LimerBoy/hackpy/blob/master/README.MD',
      author='LimerBoy',
      author_email='LimerBoyTV@gmail.com',
      license='MIT',
      packages=find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: Microsoft :: Windows",
      ],
      install_requires=[
          'wget',
          'getmac',
      ],
      include_package_data=True,
      zip_safe=False)
