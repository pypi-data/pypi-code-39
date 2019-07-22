from distutils.core import setup
setup(
  name = 'OWLPy',
  version = '0.02.1',
  license='MIT',
  description = 'Python Driver and Models for the OWL API',
  author = 'Nathaniel Vala',
  author_email = 'nathanielvala@hotmail.com',
  url = 'https://github.com/spydernaz/OWLPy.py',
  download_url = 'https://github.com/Spydernaz/OWLPy.py/archive/0.02.1.tar.gz',
  keywords = ['API', 'OWL', 'Overwatch', 'Overwatch League'],
  install_requires=[
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)