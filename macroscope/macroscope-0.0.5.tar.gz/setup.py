from setuptools import setup

setup(
    name='macroscope',
    version='0.0.5',
    py_modules=['macroscope', 'lib.enums'],
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
