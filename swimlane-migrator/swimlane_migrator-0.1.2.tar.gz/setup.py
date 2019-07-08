from setuptools import setup

def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()


with open('.\\README.md') as f:
    long_description = f.read()

setup(
    name='swimlane_migrator',
    version='0.1.2',
    packages=['swimlane_migrator'],
    url='https://swimlane.com',
    license='',
    author='Swimlane',
    author_email='info@swimlane.com',
    description='Swimlane Content Migration Package',
    long_description=long_description,
    install_requires=parse_requirements('.\\requirements.txt')
)
