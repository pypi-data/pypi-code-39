from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="thunk_dict",
    version="0.1.1",
    description="Memoized dictionaries",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="kevalii",
    author_email="alexrankine@college.harvard.edu",
    packages=["thunk_dict", ],
    license="MIT",
    url="https://github.com/kevalii/thunk-dict",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License'
    ],

)
