from setuptools import setup, find_packages

__version__   = "1.0.2"

CLASSIFIERS = [
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
]

setup(name='pykural',
      entry_points={
          'console_scripts': [
              'pykural=pykural:main'
          ]
      },
      version=__version__,
      url='https://github.com/coderganesh/pykural',
      license='MIT',
      author='Ganesh Kumar T K',
      author_email='ganeshkumartk@outlook.com',
      description='Thirukkural for Python. பைதானில் திருக்குறள் !',
      packages=find_packages(),
      include_package_data=True,
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False,
      classifiers=CLASSIFIERS,
      keywords = ['Tamil', 'Thirukkural', 'pykural','திருக்குறள்'],
 )
