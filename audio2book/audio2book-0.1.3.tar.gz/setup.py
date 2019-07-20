import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="audio2book",
    version='0.1.3',
    author="Robert Hughes",
    author_email='roberts.ginger.email@gmail.com',
    install_requires=['logbook'],
    description='Converts audiobook completion into page completion',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://www.github.com/safuya/books',
    packages=['book'],
    package_dir={'book': 'book'},
    entry_points={
        'console_scripts': ['audio2book = book.__main__:main']
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Intended Audience :: End Users/Desktop'
    ])
