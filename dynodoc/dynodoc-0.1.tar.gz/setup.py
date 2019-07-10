from setuptools import setup, find_packages

setup (
    name="dynodoc",
    version="0.1",
    description='DynamoDB CLI tool that uses the document interface',
    url='http://github.com/knavsaria/dynodoc',
    author='Keeran Navsaria',
    author_email='keeran.navsaria@gmail.com',
    packages=find_packages(),
    install_requires=[
        "Click",
        "boto3"
    ],
    entry_points='''
        [console_scripts]
        dynodoc=dynodoc.dynodoc:cli
    '''
)