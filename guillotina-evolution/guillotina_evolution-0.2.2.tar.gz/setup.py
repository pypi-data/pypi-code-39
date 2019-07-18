from setuptools import find_packages
from setuptools import setup


try:
    README = open('README.rst').read()
except IOError:
    README = None

setup(
    name='guillotina_evolution',
    version="0.2.2",
    description=' ',
    long_description=README,
    install_requires=[
        'guillotina>=4.4.5,<5',
    ],
    author='Jordi Masip',
    author_email='jmasip@vinissimus.com',
    url='https://github.com/vinissimus/guillotina_evolution',
    packages=find_packages(exclude=['demo']),
    include_package_data=True,
    tests_require=[
        'pytest',
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-asyncio',
            'pytest-cov',
            'coverage',
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
    }
)
