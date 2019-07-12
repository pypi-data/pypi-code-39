from setuptools import setup, find_packages
from setuptools.command.install import install
import os, sys
from pathlib import Path


def read_file(filename):
    filepath = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), filename)
    if os.path.exists(filepath):
        return open(filepath).read()
    else:
        return ''

class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):

        install.run(self)
        
        _bash_profile_path = str(Path.home()) + '/.bash_profile'
        _click_completion_activation_str = 'eval "$(_DONG_COMPLETE=source dong)"'

        # Any case that user can't use bash_profile?
        if os.path.exists(_bash_profile_path):
            with open(_bash_profile_path, 'r+') as user_bashrc:
                if _click_completion_activation_str in user_bashrc.read():
                    return

        Path(_bash_profile_path).touch()
        # ToDo: exception handling and warn users that bash_profile is modified
        with open(_bash_profile_path, 'a') as user_bashrc:
            user_bashrc.write(_click_completion_activation_str)
    
setup(
    name='dong',
    version='0.2.1.8',
    description='Universal Command Line Interface for Libgirl AI Platform',
    long_description=read_file('readme.md'),
    long_description_content_type="text/markdown",
    url='https://dong.libgirl.com/',
    author='Team Libgirl',
    author_email='team@libgirl.com',
    license='Apache License 2.0',
    packages=find_packages(),

    ## Don't do auto activation for bash autocompletion for now. We need to provide installation option to do it.
    # cmdclass={
    #     'install': PostInstallCommand,
    # },
    install_requires=['requests==2.22.0', 'tinynetrc==1.3.0', 'click==7.0', 'tabulate'],
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    entry_points='''
        [console_scripts]
        dong=dong.cliapp:main
    '''
)
