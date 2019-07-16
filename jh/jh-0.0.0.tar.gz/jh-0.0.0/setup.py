from setuptools import find_packages, setup

with open('requirements.txt') as file:
    install_requires = file.readlines()

setup(
    author='Jeff Hernandez',
    author_email='jeff@1566.33mail.com',
    install_requires=install_requires,
    include_package_data=True,
    name='jh',
    packages=find_packages(),
    version='0.0.0',
)
