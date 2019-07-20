import setuptools


with open('requirements.txt') as fp:
    install_requires = fp.read()

setuptools.setup(
     name='alphaj_naver_stock_cralwer',
     version='0.1.6',
     author="Alpha J",
     author_email="jaeminyx@gmail.com",
     description="A Naver Stock Cralwer",
     long_description="A Naver Stock Cralwer",
     long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     install_requires=install_requires,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )