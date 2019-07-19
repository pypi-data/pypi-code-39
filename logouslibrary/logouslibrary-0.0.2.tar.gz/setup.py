from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.readlines()
    install_requires = [x.strip() for x in install_requires]

setup(
    name='logouslibrary',
    version='0.0.2',
    author="Logo",
    license='LICENSE.txt',
    url='http://en.logo.com.tr/en',
    install_requires=install_requires,
    author_email="Abdussamet.Dumankaya@logo.com.tr",
    description="LogoUS machine learning utility package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
