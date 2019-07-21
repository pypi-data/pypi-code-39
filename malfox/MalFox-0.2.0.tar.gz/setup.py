import setuptools

setuptools.setup(
	name = 'MalFox',
	version = '0.2.0',
	author = 'Valerio Lyndon',
	url = 'https://github.com/ValerioLyndon/MalFox',
	description = 'A locally-run cover generator for MyAnimeList.',
	long_description = open('README.md', 'r').read(),
	long_description_content_type = 'text/markdown',
	keywords = 'MyAnimeList, CSS, User Customization',
	license = 'MIT',
	
	packages = setuptools.find_packages(),
	install_requires = [
		'requests'
	],
	
	classifiers = [
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)