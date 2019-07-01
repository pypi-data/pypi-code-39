# Setup
import pathlib
from setuptools import setup


HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
    name='xlambda_helper',
    version='0.0.1',
    description='Helper library to handle warming requests from X-Lambda '
                '(more: https://bit.ly/xlambda).',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/dashbird/xlambda-helper-python/archive/0.0.1.tar.gz',
    author='Dashbird.io (Renato Byrro)',
    author_email='renato@dashbird.io',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

    ],
    packages=[
        'xlambda_helper',
    ],
    install_requires=[
        'boto3',
    ],
    include_package_data=True,
    keywords=[
        'x-lambda',
        'xlambda',
        'aws',
        'aws lambda',
        'cold start',
        'warm',
        'serverless',
        'containers',
    ],
)
