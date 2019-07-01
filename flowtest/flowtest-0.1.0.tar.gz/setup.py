from setuptools import setup, find_packages

setup(name='flowtest',
      version='0.1.0',
      description='Flow test framework for python',
      author='Klaas Mussche',
      author_email='klaasmussche@gmail.com',
      packages=find_packages(),
      url='https://gitlab.com/Mussche/flowtest',
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      install_requires=['networkx'])
