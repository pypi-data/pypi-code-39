from setuptools import setup, find_packages
from pathlib import Path


project_directory = Path(__file__).resolve().parent

def load_from(file_name):
    with open(project_directory / file_name, encoding='utf-8') as f:
        return f.read()

setup(
    name='timus-sender',
    version=load_from('timus/timus-sender.version').strip(),
    url='https://github.com/kirillsulim/timus-sender',
    author='Kirill Sulim',
    author_email='kirillsulim@gmail.com',
    description='Timus console solution submitter',
    long_description=load_from('README.md'),
    long_description_content_type='text/markdown',
    packages=[
        'timus'
    ],
    package_data={
        'tapas': [
            'tapas.version',
        ]
    },
    entry_points={
        'console_scripts': [
            'timus-sender = timus.__main__:main',
        ]
    },
    install_requires=[
        'requests >= 2.19.1',
    ],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
