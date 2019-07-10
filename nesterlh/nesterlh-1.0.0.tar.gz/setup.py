import setuptools

with open("README.md", "r") as fh:
    long_description =fh.read()

setuptools.setup(
        name        = 'nesterlh',
        version     = '1.0.0',
        py_modules  = ['nesterlh'],
        author      = 'leohuang',
        author_email= 'leohuang@leohuang.leohuang',
        url         = 'https://www.leohuang.top',
        description = 'A simple printer of nested lists',
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        license='MIT',
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
)