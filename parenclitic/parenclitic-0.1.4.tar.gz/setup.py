from setuptools import setup

setup(name='parenclitic',
      version='0.1.4',
      description='Parenclitic approach with kernels inside',
      url='https://github.com/mike-live/parenclitic',
      author='Mikhail Krivonosov',
      author_email='mike_live@mail.ru',
      license='MIT',
      packages=['parenclitic'],
      install_requires=[
          'numpy',
          'python-igraph',
          'pandas',
          'sklearn',
          'scipy'
      ],
      classifiers=[ # https://pypi.org/pypi?%3Aaction=list_classifiers
          'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      zip_safe=False
)