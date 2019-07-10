try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='UZ SDK',
    version='0.0.1',
    author='Oleh Rybalchenko',
    author_email='rv.oleg.ua@gmail.com',
    url='https://github.com/oryba/uz-sdk',
    description='UZ API wrapper',
    download_url='https://github.com/oryba/uz-sdk/archive/master.zip',
    license='MIT',

    packages=['uz_sdk'],
    install_requires=['requests'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ]
)