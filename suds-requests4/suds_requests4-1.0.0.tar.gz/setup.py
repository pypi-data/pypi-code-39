from setuptools import setup


setup(
    name='suds_requests4',
    version='1.0.0',
    description='A suds transport implemented with requests using suds-py3',
    long_description=open('README.rst').read(),
    author='Jason Michalski',
    author_email='jmrosal@crosal-research.com',
    install_requires=['requests', 'suds-py3'],
    license='MIT',
    url='https://github.com/genusistimelord/suds_requests4',
	python_requires='>=3.7',
	classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
)
