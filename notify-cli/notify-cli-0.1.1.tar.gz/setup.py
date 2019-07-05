from setuptools import setup

setup(
    name='notify-cli',
    version='0.1.1',
    description='A python client for notify-server',
    url='https://github.com/matthewscholefield/notify-server',
    author='Matthew Scholefield',
    author_email='matthew331199@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='notify cli',
    packages=['notify_cli'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'notify-cli=notify_cli.__main__:main',
        ],
    }
)
