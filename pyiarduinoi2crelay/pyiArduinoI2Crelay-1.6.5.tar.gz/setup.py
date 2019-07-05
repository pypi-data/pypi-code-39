from distutils.core import setup
from distutils.extension import Extension
#from Cython.Build import cythonize
#from Cython.Distutils import build_ext

def readme():
	with open('README.md') as readme:
		return readme.read()

setup(name='pyiArduinoI2Crelay',
	version='1.6.5',
	description='iarduino.ru module for Raspberry Pi',
	long_description=readme(),
	classifiers=[
		'Programming Language :: Python :: 3',
	],
	url='http://github.com/tremaru/pyiArduinoI2Crelay',
	author='iarduino.ru',
	author_email='shop@iarduino.ru',
	license='MIT',
	package=['pyiArduinoI2Crelay'],
	ext_modules = [Extension(
		name="pyiArduinoI2Crelay",
		sources=["pyiArduinoI2Crelay/pyiArduinoI2Crelay.cpp"])],
	include_package_data=True,
        zip_safe=False,
	python_requires='>=3',
)
