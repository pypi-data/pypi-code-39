from setuptools import setup


setup(
    name='kratos-debug',
    version='0.0.1',
    author='Keyi Zhang',
    author_email='keyi@stanford.edu',
    description='kratos-debug is a debug information viewer for kratos',
    url="https://github.com/Kuree/kratos-debug",
    scripts=["kratos-debug"],
    install_requires=[
        "pyqt5",
    ],
)
