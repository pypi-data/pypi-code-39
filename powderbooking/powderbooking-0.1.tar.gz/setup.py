from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='powderbooking',
      version='0.1',
      description='Application to show the best hotels with the weather',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Database :: Database Engines/Servers',
      ],
      keywords='powderbooking powder snow booking hotel database model',
      url='http://github.com/mrasap/powderbooking-database',
      author='mrasap',
      author_email='michael.kemna@gmail.com',
      license='Apache',
      packages=['database'],
      install_requires=[
          'SQLAlchemy',
      ],
      include_package_data=True,
      zip_safe=False)
