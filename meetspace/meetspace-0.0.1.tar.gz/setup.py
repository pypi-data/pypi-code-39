import io
from setuptools import setup, find_packages

readme_file = io.open('README.md', encoding='utf-8')

with readme_file:
    long_description = readme_file.read()

setup(
    name="meetspace",
    version="0.0.1",
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/marcidy/meetspace',
    author="Matt Arcidy",
    author_email="marcidy@gmail.com",
    description="web app for unifying meeting and event entry",
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    keywords="meeting meetings event events",
)
