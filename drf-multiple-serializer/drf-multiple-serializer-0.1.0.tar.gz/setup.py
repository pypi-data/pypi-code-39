import os
from setuptools import setup, find_packages


def get_version():
    with open(os.path.join('drf_multiple_serializer', '__init__.py')) as f:
        for line in f:
            if line.startswith('__version__ ='):
                return line.split('=')[1].strip().strip('"\'')


setup(
    name='drf-multiple-serializer',
    version=get_version(),
    license="MIT",
    description='Django REST framework serializer utility',
    author='jay kim',
    author_email='jaykim1361@gmail.com',
    url='https://github.com/qpfmtlcp/drf-multiple-serializer',
    packages=find_packages(),
    install_requires=['Django>=1.11'],
    keywords=['django', 'drf', 'serializer'],
    python_requires='>=3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
