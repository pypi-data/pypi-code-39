from setuptools import setup, find_packages
#from distutils.core import setup

setup(
    name = 'pipeloyus',
    packages = ['pipeloyus'],
    include_package_data=True,
    version = '2.0',
    description = 'Librerias creadas para interactuar con los servicios de AWS.',
    author='Eloy Barahona',
    author_email="eloy.barahona@gmail.com",
    license="GPLv3",
    url="",
    classifiers = ["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                   "Development Status :: 4 - Beta", "Intended Audience :: Developers",
                   "Operating System :: OS Independent"],
)
