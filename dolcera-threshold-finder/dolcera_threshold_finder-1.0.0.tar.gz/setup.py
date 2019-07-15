from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(
    name = "dolcera_threshold_finder",
    version = "1.0.0",
    description = "Dolcera threshold finder package",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    author = "Pritom Hazarika",
    license = "MIT",
    classifiers =[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["project"],
    include_package_data = True,
    install_requires = ["requests","xml","pandas","fuzzywuzzy","psycopg2","re"],
    entry_points ={
        "console_scripts":[
            "pritom_package=project.app:main"
        ]
    }
)