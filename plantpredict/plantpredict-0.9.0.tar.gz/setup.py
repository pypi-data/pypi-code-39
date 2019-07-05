from setuptools import setup

setup(
    name='plantpredict',
    version='0.9.0',
    description='Python SDK for PlantPredict (https://ui.plantpredict.com).',
    url='https://github.com/stephenkaplan/plantpredict-python',
    author='Stephen Kaplan, Performance & Prediction Engineer at First Solar, Inc.',
    author_email='stephen.kaplan@firstsolar.com',
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    packages=['plantpredict'],
    python_requires='>=3.6, <4',
    install_requires=[
        'requests',
        'pandas',
        'certifi',
        'chardet',
        'idna',
        'numpy',
        'python-dateutil',
        'pytz',
        'six',
        'urllib3',
        'mock',
        'xlrd',
        'openpyxl'
    ]
)
