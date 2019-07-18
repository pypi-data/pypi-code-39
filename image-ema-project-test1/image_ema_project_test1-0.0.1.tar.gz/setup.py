import os
import re
from setuptools import setup

regexp = re.compile(r'.*__version__ = [\'\"](.*?)[\'\"]', re.S)

base_path = os.path.dirname(__file__)

init_file = os.path.join(base_path, 'image_ema_project', '__init__.py')
with open(init_file, 'r') as f:
    module_content = f.read()

    match = regexp.match(module_content)
    if match:
        version = match.group(1)
    else:
        raise RuntimeError(
            'Cannot find __version__ in {}'.format(init_file))

with open('README.rst', 'r') as f:
    readme = f.read()


def parse_requirements(filename):
    ''' Load requirements from a pip requirements file '''
    with open(filename, 'r') as fd:
        lines = []
        for line in fd:
            line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines

requirements = parse_requirements('requirements.txt')

if __name__ == '__main__':
    setup(
        name='image_ema_project_test1',
        description='A simple example project for the 2019 High-speed Image Based Experimental Modal Analysis & Open Source Tools Summer School.',
        long_description=readme,
        license='MIT license',
        url='https://github.com/ladisk/image-ema-2019-project',
        version=version,
        author='Janko Slavič, Domen Gorjup, Klemen Zaletelj',
        author_email='janko.slavic@fs.uni-lj.si',
        maintainer='Janko Slavič, Domen Gorjup, Klemen Zaletelj',
        maintainer_email='janko.slavic@fs.uni-lj.si',
        install_requires=requirements,
        keywords=['Image-EMA Summer School'],
        packages=['image_ema_project'],
        classifiers=['Development Status :: 3 - Alpha',
                     'Intended Audience :: Developers',
                     'Programming Language :: Python :: 3.6']
    )
