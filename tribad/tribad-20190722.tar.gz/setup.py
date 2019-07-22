from setuptools import setup, Extension

#Read version number
with open("tribad/version.py") as f:
    exec(f.read())

define_macros = [
    ('VOID', 'int'),
    ('REAL', 'double'),
    ('NO_TIMER', 1),
    ('TRILIBRARY', 1),
    ('ANSI_DECLARATORS', 1),
]

setup(name='tribad',
      packages=['tribad'],
      package_dir={'tribad': 'tribad'},
      package_data={'tribad': [
          'data/*.node',
          'data/*.ele',
          'data/*.poly',
          'data/*.area',
          'data/*.edge',
          'data/*.neigh',
          'c_triangle.pxd'
      ]},
      version=__version__,
      description='Python binding to the triangle library',
      author='Dzhelil Rufat',
      author_email='drufat@caltech.edu',
      license='GNU LGPL',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ],
      url='http://dzhelil.info/triangle',
      setup_requires=[
          'setuptools>=18.0',
          'Cython>=0.18'
      ],
      install_requires=[
          'numpy>=1.7.0',
          'Cython>=0.18'
      ],
      ext_modules=[
          Extension('tribad.core',
                    [
                        'c/triangle.c',
                        'tribad/core.pyx'
                    ],
                    include_dirs=['c'],
                    define_macros=define_macros)
      ]
      )
