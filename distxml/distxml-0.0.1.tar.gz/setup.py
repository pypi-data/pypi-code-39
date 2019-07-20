from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name='distxml',
        version='0.0.1',
        description='Converts labeled data to xml format',
        py_modules=["distxml"],
        package_dir={'':'src'},
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License"
        ],
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/steventimberman/distxml",
        author="Steven Timberman",
        author_email="steventimberman@steventimberman.com",
    )
