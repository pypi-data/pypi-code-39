from setuptools import setup

setup(
    name='python-package-test',
    version='0.0.1',
    maintainer='Jack',
    maintainer_email='Jack@email.com',
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        test-cli=index:cli
    '''
)
