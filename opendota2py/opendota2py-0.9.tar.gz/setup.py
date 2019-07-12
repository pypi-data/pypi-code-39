from setuptools import setup

setup(name='opendota2py',
      version='0.9',
      description='OpenDota API Interface',
      url='https://gitlab.com/avalonparton/opendota2py',
      author='Avalon Parton',
      author_email='avalonlee@gmail.com',
      license='MIT',
      packages=['opendota2py'],
      install_requires=['requests'],
      zip_safe=False)