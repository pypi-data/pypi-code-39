from setuptools import find_packages, setup
import plugins

setup(
    name='django-508-plugins',
    version=plugins.__version__,
    description='Installable Django app containing 508-compliant plugins.',
    author='Brad Rutten',
    author_email='ruttenb@imsweb.com',
    url='https://github.com/imsweb/django-508-plugins',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
