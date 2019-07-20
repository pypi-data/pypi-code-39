from setuptools import setup

setup(name='compressjpg',
      version='0.2',
      description='Compressing jpg files with SVD algorithm',
      url='https://github.com/tworitdash/compressjpg',
      author='Tworit Dash',
      author_email='tworitdash@gmail.com',
      license='MIT',
      packages=['compressjpg'],
      scripts=['bin/compress-jpg'],
      install_requires=[
          'numpy', 'scipy', 'pillow',
      ],
      zip_safe=False)