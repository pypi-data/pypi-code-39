from setuptools import setup


with open('README.md', 'r') as read_file:
    long_description = read_file.read()


setup(
    name='pcwvalidator',
    version='0.0.1',
    author='Alexander Isherwood',
    author_email='alexander.isherwood@ye.co.uk',
    description='price comparison batch file validator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=["pcwvalidator"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ]
)
