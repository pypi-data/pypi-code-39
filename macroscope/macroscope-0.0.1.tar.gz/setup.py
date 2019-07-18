from setuptools import setup

setup(
    name='macroscope',
    version='0.0.1',
    py_modules=['macroscope'],
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        macroscope=macroscope:cli
    '''
)
