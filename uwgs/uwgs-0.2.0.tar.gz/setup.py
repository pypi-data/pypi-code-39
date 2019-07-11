from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='uwgs',
    version='0.2.0',
    description='Flexible http client for reading UW Groups API v3.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='UW Medicine Research IT',
    url='https://github.com/uwrit/uwgs',
    packages=['uwgs'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
