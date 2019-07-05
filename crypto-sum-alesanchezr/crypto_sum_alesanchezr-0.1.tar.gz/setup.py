from setuptools import setup, find_packages

setup(
    name='crypto_sum_alesanchezr',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='An example python package',
    long_description=open('README.md').read(),
    install_requires=['numpy'],
    url='https://github.com/BillMills/python-package-example',
    author='Alejandro Sanchez',
    author_email='aalejo@gmail.com'
)