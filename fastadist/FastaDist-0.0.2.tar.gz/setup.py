import setuptools

setuptools.setup(
    name='FastaDist',
    version='0.0.2',
    description='Package to calculate a distance matrix from a multiple sequence file',
    author='Anthony Underwood',
    author_email='au3@sanger.ac.uk',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'fastadist = fastadist.run_fastadist:main'
        ]
    },
    python_requires='>=3',
    install_requires=['biopython', 'bitarray'],
    test_suite='nose.collector',
    tests_require=['nose'],
    classifiers=[ 
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: Science/Research', 
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)