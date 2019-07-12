from setuptools import setup

setup(
		name = 'loopie',
		packages = ['loopie'],
		version = '0.1',
		license = "GPLv3",
		description = 'A simple looper framework',
		long_description = 'A simple looper framework for python3 with multiple features',
		author = 'Yaztown',
		author_email = 'yaztown@gmail.com',
		url = 'https://github.com/yaztown/loopie',
		download_url = 'https://github.com/yaztown/loopie/archive/v0.1.tar.gz',
		keywords = ['loopie', 'looping', 'mainloop', 'thread', 'threading', 'Pi', 'Raspberry Pi', 'RPi'],
		install_requires = [
	        'flask',
	        'flask_cors',
	        'flask_jsonrpc',
	        'wsgiserver',
	        'pytz',
      	],
		classifiers = [
		    'Development Status :: 5 - Production/Stable',
		    'Intended Audience :: Developers',
		    'Topic :: Software Development :: Build Tools',
		    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		    'Programming Language :: Python :: 3',
		    'Programming Language :: Python :: 3.4',
		    'Programming Language :: Python :: 3.5',
		    'Programming Language :: Python :: 3.6',
		    'Programming Language :: Python :: 3.7',
		 ],
)
