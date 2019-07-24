from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

# with open('HISTORY.md') as history_file:
#     HISTORY = history_file.read()

setup_args = dict(
    name='Prometer',
    version='0.1.2',
    description='Measuring Programmer Performance using some metrics from GitHub',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Susi Eva',
    author_email='susipurba2@gmail.com',
    keywords=['Programmer', 'Measuring', 'GitHub'],
    url='https://github.com/Susi-Eva/Prometer',
    # download_url='https://pypi.org/project/elastictools/'
)

install_requires = []

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)