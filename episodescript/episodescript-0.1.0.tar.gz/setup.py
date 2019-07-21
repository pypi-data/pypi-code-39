# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='episodescript',
    version='0.1.0',
    description='Scraper for TV show episode script',
    author='Kota Mori', 
    author_email='kmori05@gmail.com',
    url='https://github.com/kota7/episodescript',
    #download_url='',

    packages=find_packages(),
    py_modules=['episodescript'],
    install_requires=['beautifulsoup4', 'html5lib<1'],
    test_require=[],
    package_data={},
    entry_points={'console_scripts': 'episode-script=episodescript:episode_script_command'},
    
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',


        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        #'Programming Language :: Python :: 2.6',
        #'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',        
        'Programming Language :: Python :: 3.7',        
    ]
)

