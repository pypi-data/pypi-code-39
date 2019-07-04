from setuptools import setup

setup(name='log-shipper',
      version='0.1',
      description='Simple log shipper via HTTP',
      url='https://github.com/newint33h/log-shipper',
      author='Jorge del Rio',
      author_email='jdelrios@gmail.com',
      license='MIT',
      install_requires=[
        'pycurl',
      ],
      scripts=['bin/log-shipper'],
      zip_safe=False)