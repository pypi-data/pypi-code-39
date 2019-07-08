from setuptools import setup

__VERSION__ = '0.0.1'

setup(name='sci-slacker',
      version=__VERSION__,
      description='A tiny tool for sending experiment status to Slack client.',
      long_description=open("README.md").read(),
      long_description_content_type="text/markdown",
      keywords=['slack'],
      classifiers=[
          'Intended Audience :: Science/Research',
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      url='https://github.com/Luolc/Slacker',
      author='Liangchen Luo',
      author_email='luolc.witty@gmail.com',
      license='Apache',
      packages=['slacker'],
      install_requires=[
          'slackclient>=2.1.0',
      ],
      zip_safe=False,
      python_requires='>=3.5.0')
