from setuptools import setup

from t7pro.version import __version__


setup(name='t7pro',
      version=__version__,
      packages=['t7pro'],
      scripts=['bin/t7pro-gui'],
      install_requires=['labjack',
                        'benutils',
                        'numpy',
                        'PyQt5'],
      data_files=[
          ('share/icons/hicolor/scalable/apps', ['data/t7pro.svg']),
          ('share/applications', ['data/t7pro.desktop'])],
      url='https://gitlab.com/bendub/t7pro',
      author='Benoit Dubois',
      author_email='benoit.dubois@femto-st.fr',
      description='Gui for the LabJack T7(Pro) DAQ board',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: X11 Applications :: Qt',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
          'Natural Language :: English',
          'Operating System :: POSIX',
          'Topic :: Scientific/Engineering'],
      include_package_data=True,
      zip_safe=False)
