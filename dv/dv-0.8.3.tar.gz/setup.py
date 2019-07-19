from setuptools import setup
import os

def get_ci_version():
      tag = os.getenv('CI_COMMIT_REF_NAME')
      if not tag:
            tag = '0.0.1'
      return tag

setup(name='dv',
      version=get_ci_version(),
      description='Library to connect to DV event based vision software',
      url='http://gitlab.com/inivation/dv-python',
      author='inivation AG',
      author_email='support@inivation.com',
      license='BSD-2',
      packages=['dv', 'dv.fb'],
      install_requires=[
        'flatbuffers',
      ],
      python_requires='>=3',
      zip_safe=False)