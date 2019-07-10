import setuptools, os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-matrixbot",
    version=os.environ["CI_COMMIT_TAG"],
    author="Brian Ó",
    author_email="blacksam@gibberfish.org",
    description="A basic bot for Matrix",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/gibberfish/python-matrixbot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Donations": "https://gibberfish.org/donate/",
        "Source": "https://gitlab.com/gibberfish/python-matrixbot",
        "Issues": "https://gitlab.com/gibberfish/python-matrixbot/issues",
    },
    python_requires="~=3.6",
    install_requires=["markdown", "matrix-client"],
    keywords="bot botscript chat matrix",
)
