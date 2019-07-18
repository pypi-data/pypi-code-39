from setuptools import setup, find_packages

setup(
    name='macroscope',
    version='0.0.6',
    py_modules=['macroscope'],
    packages=find_packages(),
    install_requires=[
        'click',
        'numpy',
        'sklearn',
        'pandas',
        'matplotlib',
        'networkx',
        'community',
        'python-louvain'
    ],
    entry_points='''
        [console_scripts]
        macroscope=macroscope:cli
    '''
)
