from setuptools import setup, find_packages

setup(name="your-notes",
      version="0.1",
      description="a)",
      long_description="aa)",
      packages=['Notes'],
      package_data={'Notes': ["imgs/*"]},
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications :: GTK',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Desktop Environment',
        'Topic :: Text Processing :: Fonts'
      ],
      keywords='notes',
      url='http://github.com/5hy0w1/Notes',
      author='Artem 5hy0w1',
      author_email='5hy0w1@mail.ru',
      license='GNU',
      install_requires=[
          'PyQt5'
      ],
      include_package_data=True,
      zip_safe=False,
      entry_points={
        "console_scripts": 
            ['Notes = Notes.main:main']
        })