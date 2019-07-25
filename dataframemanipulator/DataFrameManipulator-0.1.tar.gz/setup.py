from setuptools import setup


def _read_packages(requirements_file):
    """Read a package list from a requirements.txt file"""
    with open(requirements_file) as f:
        return [l.strip() for l in f.readlines()]


setup(
    name='DataFrameManipulator',  # How you named your package folder (MyLib)
    packages=['DataFrameManipulator'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Used on top of pandas',  # Give a short description about your library
    author='Ny Aina Lorenzo',  # Type in your name
    author_email='lolo.ramaromanana@gmail.com',  # Type in your E-Mail
    url='https://github.com/NyAinaLorenzo/DataFrameManipulator',
    # Provide either the link to your github or to your website
    download_url='https://github.com/NyAinaLorenzo/DataFrameManipulator/archive/v_0.1.tar.gz',
    # I explain this later on
    keywords=['Data_frame', 'Manipulation'],  # Keywords that define your package best
    install_requires=_read_packages('requirements.txt'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which python versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
