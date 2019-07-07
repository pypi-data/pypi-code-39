from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
      long_description = fh.read()

setup(name='flowtest',
      version='0.2.0',
      description='Flow-based integration test framework for python',
      long_description=long_description,
      author='Klaas Mussche',
      author_email='klaasmussche@gmail.com',
      packages=find_packages(),
      # url='https://gitlab.com/Mussche/flowtest',
      url='https://flowtest.readthedocs.io/en/latest/',
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Topic :: Software Development :: Testing",
      ],
      install_requires=['networkx'])
