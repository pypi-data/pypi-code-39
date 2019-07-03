import setuptools

with open("README", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='softheap',
    version='0.2',
    url='https://github.com/alex-michael17/softheap',
    author="Alex Michael",
    author_email="mr17state@gmail.com",
    description="Python Soft Heap Implementation",
    packages=setuptools.find_packages(),
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
 )
