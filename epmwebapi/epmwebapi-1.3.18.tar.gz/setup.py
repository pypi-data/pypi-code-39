from setuptools import setup

setup(name = 'epmwebapi', 
      version = '1.3.18', 
      author = 'Elipse Software Ltda', 
      packages = ['epmwebapi'], 
      include_package_data=True,
      description = '', 
      long_description = '', 
      url = 'https://github.com/elipsesoftware/epmwebapi',
      python_requires='>=3.2, <4',
      install_requires=[
          'numpy',
          'requests',
          'python-dateutil',
      ],
      data_files = [("", ["LICENSE.txt"])],
      classifiers=[
      'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
      'Intended Audience :: Developers',      # Define that your audience are developers
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',   # Again, pick a license
      'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
      'Programming Language :: Python :: 3.4',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',],)

