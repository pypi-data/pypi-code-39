#!python

# PyPI Metadata (PEP 301)
SETUP_CONF = \
dict (name = "lephton",
      description = "A language library.",

      # download_url = "",

      license = "PSF",
      platforms = ['OS-independent', 'Many'],

      include_package_data = True,

      keywords = [],

      classifiers = [],
    )


def Configuration(packages):
    SETUP_CONF['version'] = ''
    SETUP_CONF['url'] = ''

    SETUP_CONF['author'] = ''
    SETUP_CONF['author_email'] = ''

    SETUP_CONF['long_description'] = ''
    SETUP_CONF['packages'] = packages

    return SETUP_CONF

def Setup():
    try: from setuptools import setup, find_packages
    except ImportError: from distutils.core import setup, find_packages

    # Invoke setup script:
    setup(**Configuration(find_packages()))

if __name__ == '__main__':
    Setup()
