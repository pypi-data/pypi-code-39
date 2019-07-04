import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pegasus-installer",
    version="0.0.1",
    author="Cory Zue",
    author_email="cory@saaspegasus.com",
    description="Pegasus Installer Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.saaspegasus.com/",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'pegasus = pegasus_installer.__main__:main',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'cookiecutter>=1.6.0',
    ],
)
