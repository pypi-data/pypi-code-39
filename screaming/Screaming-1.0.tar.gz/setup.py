from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()


setup(
    name="Screaming",
    version="1.0",
    packages=find_packages(),
    scripts=['screaming.py'],

    # metadata to display on PyPI
    author="Barry",
    author_email="lordbasilofcsu@gmail.com",
    description="This package gives you an authentic scream string",
    license="PSF",
    keywords="screaming",
    long_description = readme,
    long_description_content_type='text/markdown',  # This is important!


    project_urls={
        "Documentation": "https://github.com/havocsupremecy209/screaming"
    }

    # could also include long_description, download_url, classifiers, etc.
)
