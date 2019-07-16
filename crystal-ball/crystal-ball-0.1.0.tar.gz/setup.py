
import setuptools

setuptools.setup(
    name='crystal-ball',
    version='0.1.0',
    author='Winn Y Cui',
    author_email='winn.yc@berkeley.edu',
    packages=setuptools.find_packages(),
    scripts=[],
    url='http://pypi.python.org/pypi/crystal-ball/',
    license='LICENSE.txt',
    description='Useful crystal-ball-related stuff.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        # "Django >= 1.1.1",
        # "caldav == 0.1.4",
        "pandas",
        "seaborn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)