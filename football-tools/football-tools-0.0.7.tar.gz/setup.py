import setuptools

setuptools.setup(
    name="football-tools",
    version="0.0.7",
    author="Tiago Vicente",
    author_email="tmavicente@gmail.com",
    description="A small football statistics tool",
    url="https://gitlab.com/tmavicente/football-tools",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        football_tools=football_tools.cli:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
)