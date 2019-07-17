try:
    from setuptools import setup, find_packages
    with open("README.md", "r") as readme_file:
        readme = readme_file.read()
    requirements = ['python-crfsuite>=0.7','lxml']
except ImportError :
    raise ImportError("setuptools module required, please go to https://pypi.python.org/pypi/setuptools and follow the instructions for installing setuptools")

setup(
    name="fraddress",
    version='0.0.4',
    author='Mathieu FRANCK',
    description='Library for parsing unstructured FR addresses strings into address components',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='The MIT License: http://www.opensource.org/licenses/mit-license.php',
    url='https://github.com/fahrtass/fraddress-parser',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis']
)
