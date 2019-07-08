from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass


setup(
    name='httpie-xsisip',
    description='Broadsoft XSI SIP auth plugin for HTTPie.',
    long_description=open('README.md').read().strip(),
    version='1.0.0',
    author='Pietro Bertera',
    author_email='pietro@bertera.it',
    license='BSD',
    url='https://github.com/pbertera/httpie-xsisip',
    download_url='https://github.com/pbertera/httpie-xsisip',
    py_modules=['httpie_xsisip'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_xsisip = httpie_xsisip:XSISIPAuthPlugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Plugins',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
