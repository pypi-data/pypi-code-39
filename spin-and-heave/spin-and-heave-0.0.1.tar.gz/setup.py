import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spin-and-heave",
    version="0.0.1",
    author="Andy Klier",
    author_email="andyklier@gmail.com",
    description="package and zip lambdas, upload to s3, then run terraform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = ['spinandheave'],
    install_requires= ['setuptools'],
    entry_points = {
        'console_scripts': ['spin-and-heave=spinandheave.main:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
