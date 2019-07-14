import re

from setuptools import setup, find_packages


def get_long_description():
    with open('README.md') as f:
        return f.read()


def get_version():
    with open('monobank_client/__init__.py') as f:
        version_match = re.search(r"^__version__\s+=\s+['\"]([^'\"]*)['\"]", f.read(), re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError('Unable to find version string.')


setup(name='monobank_client',
      version=get_version(),
      description='Monobank API client',
      long_description=get_long_description(),
      long_description_content_type='text/markdown',
      author='Dmytro Brykovets',
      author_email='dmytro.brykovets@gmail.com',
      url='https://github.com/ortymid/python-monobank-client',
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
