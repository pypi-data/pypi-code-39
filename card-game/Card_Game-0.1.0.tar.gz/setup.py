from distutils.core import setup

setup(
    # Application name:
    name="Card_Game",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Caleb Perkins",
    author_email="perkdogg08@gmail.com",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/Card_Game_v010/",

    #
    # license="LICENSE.txt",
    description="This is my very first Python project. Feel free to modify in any way and I would love feedback on how to improve the code.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "flask",
    ],
)

