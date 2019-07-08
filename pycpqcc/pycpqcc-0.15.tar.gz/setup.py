from setuptools import setup

setup(name='pycpqcc',
    version='0.15',
    description='Python package for CPQCC',
    author='Daniel Helkey',
    author_email='dhelkey@stanford.edu',
    license='MIT',
    packages=['pycpqcc'],
    zip_safe = False,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'])