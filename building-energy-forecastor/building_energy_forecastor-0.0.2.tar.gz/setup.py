import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="building_energy_forecastor",
    version="0.0.2",
    author="Moi Je",
    author_email="arthur.feyt@kaizen-solutions.net",
    description="Pour l'instant fait pas grand chose",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/KZSLAB/building_energy_forecastor.git",
    install_requires=['sklearn', 'numpy', 'pandas', 'forestci'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
