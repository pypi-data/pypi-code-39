from setuptools import setup, find_packages

setup(
name='iqyocr',
packages=['iqyocr'],
version="0.0.2",
py_modules=['iqyocr'],
install_requires=[
"uiautomator2==0.3.3",
"requests==2.18.4",
"six==1.11.0"
],
author='yuyinweiliao',
author_email='yuyinweiliao@163.com',
url='http://www.iqiyi.com',
description='iqy ocr for uiautomaotr2'
)
# setup(
#     name='iqyocr',
#     version="0.0.1",
#     packages=find_packages(),
#     entry_points={
#         "console_scripts": ['GFICLEE = predict.main:main']
#     },
#     install_requires=[
#         "uiautomator2==0.3.3",
#         "requests==2.18.4",
#         "six==1.11.0"
#     ],
#     url='https://github.com/yuyinweiliao',
#     license='GNU General Public License v3.0',
#     author='yuyinweiliao',
#     author_email='yuyinweiliao@163.com',
#     description='iqy ocr for uiautomaotr2'
# )