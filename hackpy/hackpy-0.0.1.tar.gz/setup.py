from setuptools import setup, find_packages

setup(name='hackpy',
      version='0.0.1',
      description='Windows hacking commands in python',
      long_description='Full description here: https://github.com/LimerBoy/nirpy/blob/master/README.md',
      url='https://github.com/LimerBoy/nirpy',
      author='LimerBoy',
      author_email='LimerBoyTV@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'wget',
          'getmac',
      ],
      include_package_data=True,
      zip_safe=False)
