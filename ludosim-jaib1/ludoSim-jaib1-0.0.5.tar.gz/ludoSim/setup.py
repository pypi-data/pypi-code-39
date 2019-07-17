import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read() # set README.md as long_description

setuptools.setup(
    name='ludoSim-jaib1',
    version='0.0.5',
    author='Jai Bhagat',
    author_email='dudecmonitsme@gmail.com',
    license='GNU General Public License v3',
    description='A simple ludo simulator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jaib1/ludoSim',
    packages=['ludoSim'],
    #packages=setuptools.find_packages(exclude=['docs', 'tests']),
    package_data={        
        'ludoSim': ['*.*', 'analysis/*.*', 'tests/*.*', 'LICENSE'],
    },
    keywords='ludo simulator bet',
    python_requires='>=3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
