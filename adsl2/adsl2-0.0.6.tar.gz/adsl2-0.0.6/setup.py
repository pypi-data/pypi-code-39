from distutils.core import setup
from setuptools import find_packages

with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read()

setup(name='adsl2',  # 包名
      version='0.0.6',  # 版本号
      description='pppoe',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='sun',
      author_email='syw1894@163.com',
      url='https://pypi.org/project/adsl2/',
      license='',
      install_requires=[],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('adsl'),  # 必填，就是包的代码主目录
      package_dir={'': 'adsl'},  # 必填
      include_package_data=True,
      )
