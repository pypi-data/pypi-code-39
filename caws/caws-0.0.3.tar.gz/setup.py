import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="caws",
    version="0.0.3",
    author="Andy Klier",
    author_email="andyklier@gmail.com",
    description="configure AWS responsibly using profile names.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/rednap/caws",
    packages = ['caws'],
    entry_points = {
        'console_scripts': ['caws=caws.main:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
