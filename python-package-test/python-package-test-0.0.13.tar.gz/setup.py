from setuptools import setup

REQUIRED_PACKAGES = ['click']
DEV_PACKAGES = ['flake8', 'wheel', 'autopep8']

LOCAL_PACKAGE_DIRECTORY_NAMES = ['lib']
MODULES = ['index']

setup(
    name='python-package-test',
    version='0.0.13',
    author='StraightOuttaCrompton',
    author_email='soc@email.com',
    description='An example click cli project that can be published to PyPI.',
    license='GNU',
    packages=LOCAL_PACKAGE_DIRECTORY_NAMES,
    py_modules=MODULES,
    install_requires=REQUIRED_PACKAGES,
    extras_require={
        'dev': DEV_PACKAGES
    },
    python_requires='>=3.0.*',
    entry_points={
        'console_scripts': [
            'test-cli=index:cli'
        ]
    },
    project_urls={
        'Source': 'https://github.com/StraightOuttaCrompton/python-package-test'
    },
)
