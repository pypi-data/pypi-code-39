# python setup.py --dry-run --verbose install

from distutils.core import setup
import os

with open(os.path.join(".", 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(
    name='cowboybike',
    version=version,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License"
    ],
    author='Samuel Dumont',
    author_email='samuel@dumont.info',
    py_modules=['cowboybike'],
    scripts=[],
    data_files=[],
    url='https://gitlab.com/samueldumont/python-cowboy-bike',
    download_url='https://gitlab.com/samueldumont/python-cowboy-bike',
    license='MIT',
    description='Simple API to access Cowboy Bike data.'
)
