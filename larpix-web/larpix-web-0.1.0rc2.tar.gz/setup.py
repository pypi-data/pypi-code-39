from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()

with open(os.path.join(here, 'VERSION')) as f:
    version = f.read()


setup(
        name='larpix-web',
        version=version,
        description='LArPix DAQ Web Interface',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/larpix/larpix-webapp',
        author='Sam Kohn, LBNL Neutrino Group',
        author_email='skohn@lbl.gov',
        keywords='dune larpix',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'Programming Language :: Python',
            'Topic :: Scientific/Engineering :: Physics',
            'Topic :: Scientific/Engineering',
            ],
        packages=['larpixweb'],
        package_dir = {'larpixweb': 'server'},
        install_requires=[
            'flask >=1.0.0',
            'flask-socketio >=3.0',
            'eventlet >= 0.24',
            'requests ~= 2.18',
            'larpix-daq ~= 0.2.0',
            ],
        package_data={
            'larpixweb': ['build/*', 'build/static/*'],
            },
)
