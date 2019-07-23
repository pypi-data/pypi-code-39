import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyFission',
    # link to github page
    url='https://github.com/nishantnath/pyfission/',
    author='Nishant Nath, Aniket Shenoy',
    # author_email='',
    packages=setuptools.find_packages(),
    version='1.0',
    license='MIT',
    description='A tool to sync data across data sources',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True
)
