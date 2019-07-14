""" Get Ready setup """

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # pylint: disable=E0611,F0401


setup(
    name='nrn',
    version=0.1,
    install_requires=[],
    packages=['nrn'],
    author='Werner Van Geit',
    author_email='werner.vangeit@gmail.com',
    description='Nrn placeholder',
    entry_points={'console_scripts': ['nrn=nrn.nrn:main'], },
    keywords=(),
    classifiers=[
        'Development Status :: 4 - Beta'])
