import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="astspy",
    version="0.0.1",
    author="Edgar Nova",
    author_email="ragnarok540@gmail.com",
    description="Abstract Syntax Tree SPY",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="ast, spy, static code analysis, abstract syntax tree",
    url="https://github.com/Ragnarok540/astspy",
    py_modules=['astspy'],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'astspy = astspy:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
