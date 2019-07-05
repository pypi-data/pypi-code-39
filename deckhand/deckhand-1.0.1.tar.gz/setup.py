import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

metadata = {}
with open("deckhand/__about__.py") as fp:
    exec(fp.read(), metadata)

setuptools.setup(
    name=metadata['__name__'],
    version=metadata['__version__'],
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    description=metadata['__description__'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=metadata['__url__'],
    packages=setuptools.find_packages(),
    package_dir={
        'deckhand' : 'deckhand',
    },
    package_data={
        'deckhand' : [ 'resources' ],
    },
    classifiers=[
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Archiving :: Packaging",
        "Topic :: System :: Software Distribution",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English"
    ],
    keywords='deckhand oceanstack development',
    license='Apache License 2.0',
    python_requires='>=3.0.*, <4',
    install_requires=[
            'termcolor',
        ],
    entry_points={
        'console_scripts': [
            'deckhand=deckhand.__main__:main',
        ],
    },
)
