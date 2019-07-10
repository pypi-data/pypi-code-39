from setuptools import setup

setup(name='riminder',
      version='1.4.2',
      description='python riminder riminder api package',
      url='https://github.com/Riminder/python-riminder-api',
      author='mnouayti',
      author_email='contact@rimider.net',
      license='MIT',
      packages=['riminder'],
      install_requires=[
          'requests',
          'python-magic'
      ],
      python_requires='>=3.5',
      zip_safe=False)
