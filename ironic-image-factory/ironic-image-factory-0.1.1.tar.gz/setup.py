from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf8' ) as f:
    long_description = f.read()

setup(
        name='ironic-image-factory',
        version='0.1.1',
        description='Updates/Adds Glance Images',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/cjloader/ironic-image-factory',
        author='cam loader',
        author_email='cam.loader@rackspace.com',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            ],
        keywords="ironic image factory",
        packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        python_requires='>=3.5',
        install_requires=[
            'wget',
            'urllib3',
            'python-ironicclient',
            'python-ironic_inspector_client',
            'python-keystoneclient',
            'python-novaclient',
            'python-glanceclient',
            ],
        entry_points={
            'console_scripts': [
                'ironic-image-factory=ironic_image_factory.images:main',
                ]
            }
)
