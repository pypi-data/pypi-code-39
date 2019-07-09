from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='numpy-syncer',
      description='Manage a Numpy data structure using Peewee-Sync',
      long_description=long_description,
      long_description_content_type="text/markdown",
      version='0.0.1',
      url='https://github.com/hampsterx/numpy-syncer',
      author='Tim van der Hulst',
      author_email='tim.vdh@gmail.com',
      license='Apache2',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3'
      ],
      packages=['numpy_syncer'],
      install_requires=[
            'peewee-syncer>=0.2.2',
            'numpy>=1.16.4',
            'aiofiles>=0.4.0',
            'contexttimer>=0.3.3',
            'humanize>=0.5.1'
      ]
)

