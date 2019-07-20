from setuptools import setup
from codecs import open
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sms4',
    version='0.1.0',
    description='Simple and straightforward way to send text messages',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://sms4.dev',
    author='Sergey Gaykov',
    author_email='sdgaykov@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',

        'Topic :: Communications :: Telephony',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    packages=['sms4'],
    install_requires=['requests']
)
