import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spyprot",
    version="0.0.1.1",
    author="Borys Jastrzębski, Paweł Rubach",
    author_email="b.jastrzebski@cent.uw.edu.pl, p.rubach@cent.uw.edu.pl",
    description="Rapid protein overview from multiple databases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zedelghem/spyProt",
    packages=setuptools.find_packages(),
    install_requires=[
   'tqdm>=4.31.1',
   'lxml>=3.5.0',
   'requests>=2.20.0',
   'Bio>=0.1.0',
   'psutil>=5.6.3',
   'subprocess32>=3.5.4',
   'wget>=3.2'
],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)