import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
    name='pyFission',
    url='https://github.com/nishantnath/pyfission/',
    author='Nishant Nath, Aniket Shenoy',
    # author_email='',
    packages=setuptools.find_packages(),
    version='1.0.2',
    license='MIT',
    description='A tool to sync data across data sources',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
)
