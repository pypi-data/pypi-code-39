from setuptools import setup

setup(
    name='macroscope',
    version='0.0.4',
    py_modules=['macroscope', 'lib'],
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
