from setuptools import setup
import os
import re
import codecs
# Create new package with python setup.py sdist

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# Create new package with python setup.py sdist
setup(
    name='cryoloBM',
    version=find_version("cryoloBM", "__init__.py"),

    packages=['cryoloBM'],
    url='',
    license='MIT',
    author='Thorsten Wagner',
    install_requires=[
        "matplotlib == 2.2.3",
        "cryolo >= 1.2.2",
        "numpy == 1.14.5",
    ],
    author_email='thorsten.wagner@mpi-dortmund.mpg.de',
    description='Boxmanager to create training data for crYOLO',
    long_decription='# crYOLO Boxmanager'
                    'The crYOLO boxmanger was written to produce annotation data for [crYOLO](http://sphire.mpg.de/wiki/doku.php?id=downloads:cryolo_1), as deep learning based particle picking procedure for cryo electro microscopy.',
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'cryolo_boxmanager.py = cryoloBM.boxmanager:run']},
)