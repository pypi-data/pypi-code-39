from setuptools import setup, find_packages

setup(
    name='python-package-test',
    version='0.0.10',
    maintainer='Jack',
    # py_modules=['index', 'fact'],
    packages=find_packages(),
    maintainer_email='Jack@email.com',
    install_requires=[
        'Click'
    ],
    python_requires='>=3.0.*',
    entry_points={
        'console_scripts': [
            'test-cli=lib.index:cli'
        ]
    }
)


# setup(
#     name='python-package-test',
#     version='0.0.6',
#     maintainer='Jack',
#     # py_modules=['index', 'fact'],
#     packages=find_packages(),
#     maintainer_email='Jack@email.com',
#     install_requires=[
#         'Click'
#     ],
#     entry_points='''
#         [console_scripts]
#         test-cli=index:cli
#     '''
# )
