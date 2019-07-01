import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyQuASAR',
    version='0.0.1',
    author='Anthony Aylward',
    author_email='aaylward@eng.ucsd.edu',
    description='Wrap quasar for pipelines',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/anthony-aylward/pyQuASAR.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['funcgenom'],
    entry_points={
        'console_scripts': ['pyQuASAR-download=pyQuASAR.download:main',]
    },
    include_package_data=True
)
