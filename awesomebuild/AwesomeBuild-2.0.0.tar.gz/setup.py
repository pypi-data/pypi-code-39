from setuptools import setup

setup(
    name='AwesomeBuild',
    description='Awesome build manager to replace Makefiles. It allow very fast building!',
    version='2.0.0',
    author='Raphael Jacob',
    author_email='r.jacob2002@gmail.com',
    url='https://github.com/ski7777/AwesomeBuild',
    license='GPLv3',
    packages=['AwesomeBuild'],
    entry_points={
        'console_scripts': [
            'AwesomeBuild = AwesomeBuild.__main__:main'
        ]
    }
)
