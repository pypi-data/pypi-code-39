from setuptools import find_packages, setup

NAME = 'flask-api-spec'
VERSION = '0.1.10'


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

with open('README.md') as f:
    long_description = f.read()


setup(
    name=NAME,
    version=VERSION,
    packages=[t for t in find_packages() if t.startswith(
        NAME.replace('-', '_'))],
    include_package_data=True,
    install_requires=[str(ir) for ir in parse_requirements(
        './requirements.txt')],
    long_description=long_description,
    long_description_content_type='text/markdown',  # This is important!
    author='laberin',
    author_email='eseom@msn.com',
    url="http://github.com/laberin/flask-api-spec/",
    license="MIT",
    description="flask api toolset",
    platforms="any",
    classifiers=[
        "Environment :: Web Environment",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    # tests_require=tests_require,
    # extras_require={
    #     'test': tests_require,
    #     },
    # test_suite='pytest',
)
