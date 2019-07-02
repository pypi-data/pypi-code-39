from setuptools import setup

setup(
	name='cwbbus',
	version='0.0.1',
	packages=[''],
	package_dir={'': 'cwbbus'},
	url='https://github.com/killertux/cwbbus',
	download_url='https://github.com/killertux/cwbbus/archive/0.0.1.tar.gz',
	install_requires=[
		'aiohttp',
		'async_timeout',
		'pandas',
      ],
	license='MIT',
	author='Angelin01, killertux, Kabbah',
	author_email='',
	description='Package aimed at facilitating the use of the open data from Curitiba\'s public transport system'
)
