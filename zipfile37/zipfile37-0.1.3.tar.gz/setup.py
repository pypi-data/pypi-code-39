from distutils.core import setup

with open("README.rst", "r") as f:
    readme = f.read()

setup(name='zipfile37',
      version='0.1.3',
      description='Read and write ZIP files - backport of the zipfile module from Python 3.7',
      long_description = readme,
      author='Markus Scheidgen, Thomas Kluyver',
      author_email='markus.scheidgen@gmail.com',
      url='https://github.com/markus1978/zipfile37',
      py_modules=['zipfile37'],
      classifiers=[
          'License :: OSI Approved :: Python Software Foundation License',
          'Programming Language :: Python :: 3',
          'Topic :: System :: Archiving :: Compression',
      ]
)
