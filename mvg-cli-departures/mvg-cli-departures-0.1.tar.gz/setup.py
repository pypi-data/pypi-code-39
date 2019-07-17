from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='mvg-cli-departures',
        version='0.1',
        description='Command line departure monitor for the MVG - munich\'s public transport',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://gitlab.com/maternusherold/mvg-command-line-departure-monitor',
        author='Turnman H',
        # TODO: change email
        author_email='turnmanh@gmail.com',
        license='MIT',
        packages=['app'],
        # scripts=['bin/funniest-joke'],
        entry_points={
            'console_scripts': ['mvg-depart=app.interface:main']
        },
        zip_safe=False)
