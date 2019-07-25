import os

from setuptools import setup


def read(fname):
    """
    Helper to read README
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read().strip()


data_files = [
    "schemata/{}".format(i)
    for i in os.listdir("schemata")
    if os.path.isfile("schemata/{}".format(i))
]

setup(
    name="maruval",
    version="0.1.1",  # bump2version will edit this automatically!
    description="Validator for marugoto game content",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="http://github.com/uzh/maruval",
    author="Danny McDonald",
    include_package_data=True,
    zip_safe=False,
    packages=["maruval"],
    package_data={"maruval": data_files},
    data_files=[("schemata", data_files)],
    scripts=["bin/maruval", "bin/marufind", "bin/marupretty"],
    author_email="daniel.mcdonald@uzh.ch",
    license="MIT",
    keywords=[],
    install_requires=["jsonschema==3.0.1"],
    dependency_links=[],
)
