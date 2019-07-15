from setuptools import setup

with open ('README.md', 'r') as fh:
    long_description = fh.read()

setup(
      long_description = long_description,
      long_description_content_type='text/markdown',
      name='hamble',
      version='0.0.5',
      packages=['hamble'],
      description="Package for handling parameters from an ini file to configuration files.",
      author='nathan mikkelsen',
      author_email="nathan.mikkelsen@corteva.com",
      install_requires=[
            'Click~=7.0',
            'configparser~=3.7.4',
            'Jinja2~=2.10.1',
            'boto3~=1.9.187',
      ],
      entry_points=''' 
        [console_scripts]
        hamble=hamble.command:cli 
      '''
      )
