from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='wrktools-xlsx',
      version='0.0.4',
      description='XLSX spreadsheet reports for wrktoolbox.',
      long_description=readme(),
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Operating System :: Unix'
      ],
      url='https://github.com/RobertoPrevato/wrktoolbox-xlsx',
      author='RobertoPrevato',
      author_email='roberto.prevato@gmail.com',
      keywords='wrk runner benchmarks load performance tests xlsx results',
      license='MIT',
      packages=['wrktoolboxxlsx'],
      install_requires=['wrktools',
                        'xlsxwriter'],
      include_package_data=True,
      zip_safe=False)
