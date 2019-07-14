import setuptools

with open("README.md","r") as fh:
	long_descritiption = fh.read()
	

setuptools.setup(
	name='wyb',
	version='0.0.1',
	author='wyb',
	author_email='1770841968@qq.com',
	description="pip install test",
	long_descritiption=long_descritiption,
	long_descritiption_content_type='text/markdown',
	url='https://github.com/wengyinbing/Rangomaster',
	packages=setuptools.find_packages(),
	classifiers=(
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ),
)