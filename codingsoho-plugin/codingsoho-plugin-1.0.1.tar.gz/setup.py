import os
# from setuptools import find_packages, setup
import setuptools


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name='codingsoho-plugin',
    version='1.0.1',
    packages=setuptools.find_packages(),  # ['zip_url']
    include_package_data=True,
    license='BSD License',  # example license
    description='codingsoho-plugin is a mixin library to extend your CBV for quick function',
    long_description=README,
    long_description_content_type="text/markdown",
    url='http://www.codingsoho.com/',
    author='Horde Chief',
    author_email='hordechief@qq.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        # 'Framework :: Django :: 1.11',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)