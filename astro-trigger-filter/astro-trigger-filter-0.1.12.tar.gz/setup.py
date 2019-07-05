import setuptools

with open("README.md", "r") as fh:
    README = fh.read()

# This call to setup() does all the work
setuptools.setup(
    name="astro-trigger-filter",
    version="0.1.12",
    description="A package for filtering triggers from radio astronomical matched template pulse searches.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=['astronomy','filter'],
    url="https://github.com/sitmo/astro-trigger-filter",
    author="Thijs van den Berg",
    author_email="thijs@sitmo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    #packages=["astro-trigger-cluster"],
    packages=setuptools.find_packages(exclude=["tests", "examples", "test*", "private"]),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)