from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='show-contests',
    version='1.0',
    py_modules=['cli'],
    author = 'singlamohit1',
    author_email = 'singlamohit98@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/singlamohit1/show-contests',
    license = 'Apache 2.0',
    description = 'A basic command line tool to show the upcoming competitive programming contests',
    install_requires=[
        'Click','requests','tabulate'
    ],
    entry_points='''
        [console_scripts]
        show-contests=cli:cli
    ''',
)