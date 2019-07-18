from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name='mercurio',
      version='0.10.1',
      url='https://github.com/pietrogiuffrida/mercurio/',
      author='Pietro Giuffrida',
      author_email='pietro.giuffri@gmail.com',
      license='MIT',
      packages=['mercurio'],
      zip_safe=False,
      install_requires=[],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      description='Send email with python, my way',
      long_description=long_description,
      long_description_content_type='text/markdown',
)
