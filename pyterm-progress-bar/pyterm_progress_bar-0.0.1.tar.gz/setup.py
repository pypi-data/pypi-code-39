import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='pyterm_progress_bar',
    version='0.0.1',
    author='William Dry',
    author_email='wpbdry@gmail.com',
    description="Prints a progress bar to the terminal from python.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wpbdry/pyterm_progress_bar_pkg',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT'
)