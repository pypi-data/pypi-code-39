import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='minelert-utils',
    version='1.0.0',
    author="Niel Venter",
    author_email="support@minelert.com",
    description="Minelert utility package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dpventer/minelert_utils",
    license='MIT',
    packages=['minelert_utils'],
    include_package_data=True,
    install_requires=[
          'pySerial',
      ],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
)