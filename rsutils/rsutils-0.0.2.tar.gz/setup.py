from setuptools import setup, find_packages

__VERSION__ = '0.0.2'

setup(
    name='rsutils',
    version=__VERSION__,
    description="A bunch of utilities for Python. Built with :heart: by Reckonsys ",  # NOQA
    long_description="Core utilitties",
    url='https://github.com/reckonsys/rsutils_python',
    author='dhilipsiva',
    author_email='dhilipsiva@pm.me',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='rsutils reckonsys python',
    packages=find_packages(),
    entry_points='',
    install_requires=[]
)
