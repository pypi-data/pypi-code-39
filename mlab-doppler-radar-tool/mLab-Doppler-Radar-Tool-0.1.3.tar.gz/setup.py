from setuptools import setup

setup(name='mLab-Doppler-Radar-Tool',
      version='0.1.3',
      packages=['mLab_DopplerRadar'],
      install_requires=[
          'PyQt5','pyserial','pyqtgraph'
      ],
      include_package_data=True,
      url='', license='MIT',
      author='Alex Kuan',
      author_email='agathakuannew@gmail.com',
      description='mLab Doppler Radar UART tool and example code')