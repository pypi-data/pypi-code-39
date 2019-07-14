import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read() # set README.md as long_description

setuptools.setup(
    name='ludoSim-jaib1',
    version='0.0.1',
    author='Jai Bhagat',
    author_email='dudecmonitsme@gmail.com',
    license='GNU General Public License v3',
    description='A small ludo simulator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jaib1/ludoSim',
    packages=setuptools.find_packages(),
    keywords='ludo simulator bet',
    python_requires='>=3',
    package_data={
        'ludoSim': ['StandardLudoBoard.png'],
        'ludoSim': ['ludoSim_env.yml'],
        'ludoSim': ['StandardLudoBoard.png'],
        'ludoSim': ['TermsOfBet.md'],
        'ludoSim': ['StandardLudoBoard.png'],
        'ludoSim': ['analysis/*.png'],
        'ludoSim': ['analysis/*.dat'],
        'ludoSim': ['analysis/*.dir'],
        'ludoSim': ['analysis/*.png'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
