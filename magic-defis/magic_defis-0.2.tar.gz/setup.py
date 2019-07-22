from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='magic_defis',
    url='https://magicmakers.fr/',
    author='Magic Team',
    author_email='pedagogie@magicmakers.fr',
    # Needed to actually package something
    packages=['magic_defis'],
    # Needed for dependencies
    install_requires=[
            'numpy',
            'pillow',
            'pydub',
            'colorama',
            'termcolor'
            ],
    # *strongly* suggested for sharing
    version='0.2',
    # The license can be anything you like
    license='MIT',
    description='Defis python Magic Makers',
    # We will also need a readme eventually (there will be a warning)
     long_description=open('README.txt').read(),
)
