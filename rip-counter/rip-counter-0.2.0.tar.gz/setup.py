from setuptools import setup
from setuptools import find_packages


setup(name='rip-counter',
      version='0.2.0',
      author='Hadrien Mary',
      author_email='hadrien.mary@gmail.com',
      url='https://github.com/hadim/rip-counter/',
      description='A vote counter for french RIP.',
      long_description_content_type='text/markdown',
      packages=find_packages(),
      entry_points={'console_scripts': ['scrap-my-rip = rip_counter.scrap:main',
                                        'scrap-my-rip-bot = rip_counter.bot:start_bot']},
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Natural Language :: English',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
      ])
