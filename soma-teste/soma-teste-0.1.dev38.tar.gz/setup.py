import setuptools
import os


def myversion():
    from setuptools_scm.version import get_local_dirty_tag
    def clean_scheme(version):
        return get_local_dirty_tag(version) if version.dirty else ''

    return {'local_scheme': clean_scheme, "root": "..", "relative_to":__file__}

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(
    name='soma-teste',
    author="Cyfer",
    author_email="luiz.costa@somagrupo.com.br",
    description="Private utility package used by SomaLabs.",
    use_scm_version=myversion,
    setup_requires=['setuptools_scm'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/somalabs/soma-tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["pandas", "mysql-connector"],

)
