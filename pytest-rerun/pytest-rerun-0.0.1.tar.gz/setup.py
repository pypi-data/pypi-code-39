from setuptools import setup


def read_file(fname):
    with open(fname) as f:
        return f.read()


setup(
    name='pytest-rerun',
    description='Re-run only changed files in specified branch',
    long_description=read_file('readme.md'),
    version='0.0.1',
    author='Parviz Khavari',
    author_email='me@parviz.pw',
    url='http://github.com/zeburek/pytest-rerun/',
    packages=[
        'pytest_rerun',
    ],
    package_dir={'pytest_rerun': 'pytest_rerun'},
    install_requires=[
        'pytest>=3.6',
        'gitpython',
    ],
    include_package_data=True,
    entry_points={'pytest11': ['pytest-rerun = pytest_rerun.conftest']},
)