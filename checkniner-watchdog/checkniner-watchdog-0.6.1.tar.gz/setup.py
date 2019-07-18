from setuptools import setup, find_packages

setup(
    name='checkniner-watchdog',
    version='0.6.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[line.strip() for line in open('requirements.txt.lock', 'r')],
    entry_points="""
        [console_scripts]
        watchdog=watchdog.watchdog:watchdog
    """
)
