import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aws-cost-report",
    version="0.0.2",
    author="Andy Klier",
    author_email="andyklier@gmail.com",
    description="command line tool which will return total cost for the current month's AWS usage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rednap/aws-cost-report-pypi",
    packages = ['costreport'],
    entry_points = {
        'console_scripts': ['cost-report=costreport.main:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
