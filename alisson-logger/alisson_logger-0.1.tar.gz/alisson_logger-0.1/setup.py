import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='alisson_logger',  
     version='0.1',
     author="Alisson Machado",
     author_email="alisson.machado@gmail.com",
     description="pacote criado para demonstrar o pypi",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/AlissonMMenezes/alisson_cli",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )