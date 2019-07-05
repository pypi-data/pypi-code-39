from setuptools import setup

setup(
    name='notify-server',
    version='0.1.2',
    description='A tool to broadcast notifications across various interfaces',
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
    keywords='notify server',
    packages=['notify_server'],
    install_requires=[
        'Flask',
        'flask-resto',
        'ruko',
        'flask-ruko',
        'gunicorn',
        'prettyparse',
        'notify-cli'
    ],
    entry_points={
        'console_scripts': [
            'notify-server=notify_server.__main__:main',
        ],
    }
)
