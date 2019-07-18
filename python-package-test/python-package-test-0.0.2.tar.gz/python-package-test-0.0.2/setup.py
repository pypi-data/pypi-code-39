from setuptools import setup

setup(
    name='python-package-test',
    version='0.0.2',
    maintainer='Jack',
    py_module=['index'],
    maintainer_email='Jack@email.com',
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        test-cli=index:cli
    '''
)
