from setuptools import setup

requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

readme = ''
with open('README.rst') as f:
    readme = f.read()


setup(name="Star Bot utils",
    author='Nite',
    version="0.0.1a",
    packages=['starbotutils'],
    license=None,
    description='The main bots utils',
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    python_requires='>=3.5.3',
    classifiers=[
    'Intended Audience :: Developers',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7'
    ]
)