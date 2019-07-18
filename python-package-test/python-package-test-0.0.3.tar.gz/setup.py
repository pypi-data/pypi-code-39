from setuptools import setup

setup(
    name='python-package-test',
    version='0.0.3',
    maintainer='Jack',
    py_modules=['index'],
    maintainer_email='Jack@email.com',
    install_requires=[
        'Click'
    ],
    entry_points='''
        [console_scripts]
        test-cli=index:cli
    '''
)
