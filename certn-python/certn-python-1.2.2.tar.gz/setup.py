from os.path import splitext, basename, join, abspath, dirname
from glob import glob
from setuptools import find_packages
from setuptools import setup

here = dirname(__file__)
reqs = join(here, 'requirements.txt')

print(reqs)

# get the dependencies and installs
with open(abspath(reqs)) as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]

# read the contents of your README file
this_directory = abspath(dirname(__file__))
with open(join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='certn-python',
    version='1.2.2',
    url='https://github.com/livebungalow/certn-python',
    license='MIT',
    author='Bungalow Living',
    author_email='engineering@bungalow.com',
    summary='A python client for Certn API',
    description='A python client for Certn API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages('certn-python'),
    package_dir={'': 'certn-python'},
    py_modules=[splitext(basename(path))[0] for path in glob('certn-python/*.py')],
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
