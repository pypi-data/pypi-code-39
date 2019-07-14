from setuptools import setup, find_packages


with open('README.md') as f:
    long_description = f.read()


setup(name='monobank_client',
      version='0.1.1',
      description='Monobank API client',
      long_description=long_description,
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
