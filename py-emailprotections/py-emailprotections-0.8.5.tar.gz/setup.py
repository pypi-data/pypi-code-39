import os
from setuptools import setup

def get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, 'rb') as f:
            return f.read().decode('utf8')
    except IOError:
        pass
    return ''

def get_readme():
    return get_file(os.path.dirname(__file__), 'README.md')

setup(
    name="py-emailprotections",
    packages=["emailprotectionslib"],
    version="0.8.5",
    description="Python library to interact with SPF and DMARC",
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    author="poipoii",
    author_email="earth.sama@gmail.com",
    url="https://github.com/poipoii/pyemailprotectionslib",
    install_requires=['dnslib', 'tldextract', 'future'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ]
)