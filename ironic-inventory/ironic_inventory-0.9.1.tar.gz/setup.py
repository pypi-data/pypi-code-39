"""
   Copyright [2019] [Paul Sims]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf8' ) as f:
    long_description = f.read()

setup(
        name='ironic_inventory',
        version='0.9.1',
        description='Register ironic nodes via excel spreadsheet',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/rcbops/ironic_inventory',
        author='paul sims',
        author_email='paul.sims@rackspace.com',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            ],
        keywords="ironic node registration",
        packages=find_packages(exclude=['contrib', 'docs', 'tests']),
        python_requires='>=3.5',
        install_requires=[
            'pandas',
            'xlrd',
            'gevent==1.4.0',
            'python-ironicclient==2.7.2',
            'python-ironic_inspector_client==3.5.0',
            'python-keystoneclient==3.19.0',
            'python-novaclient==13.0.1',
            'python-glanceclient==2.16.0',
            ],
        data_files=[('examples', ['examples/ironic_nodes.xlsx'])],
        entry_points={
            'console_scripts': [
                'ironic_inventory=ironic_importer.inventory:main',
                ]
            }
)
