from setuptools import setup


setup(name='powderbooking',
      version='0.3.1',
      description='Application to show the best hotels with the weather',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Database :: Database Engines/Servers',
      ],
      keywords='powderbooking powder snow booking hotel powderbooking model',
      url='http://github.com/mrasap/powderbooking-database',
      author='mrasap',
      author_email='michael.kemna@gmail.com',
      license='Apache',
      packages=['powderbooking'],
      install_requires=[
          'SQLAlchemy',
          'psycopg2-binary',
      ],
      include_package_data=True,
      zip_safe=False)
