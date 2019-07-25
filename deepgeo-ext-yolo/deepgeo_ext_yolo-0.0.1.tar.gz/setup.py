from setuptools import setup, find_packages

setup(name='deepgeo_ext_yolo',
      version='0.0.1',
      url='https://github.com/Sotaneum/deepgeo_ext_yolo',
      license='MIT',
      author='Donggun LEE',
      author_email='gnyotnu39@gmail.com',
      description='deepgeo_ext_yolo',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      zip_safe=False,
      setup_requires=[],
      install_requires=['deepgeo>=0.2.0','numpy','opencv-python'],
      classifiers=[
          'License :: OSI Approved :: MIT License'
      ]
)
