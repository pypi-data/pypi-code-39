from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()

setup_args = dict(
    name='HandlerAPI',
    version='0.4.3',
    description='Parsing PR, Issue, Commit, and LOC data from GitHub REST API',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Susi Eva',
    author_email='susipurba2@gmail.com',
    keywords=['Handler', 'API', 'GitHub'],
    url='https://github.com/Susi-Eva/Parser',
    # download_url='https://pypi.org/project/elastictools/'
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)