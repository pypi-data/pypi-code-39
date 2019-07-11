from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="wxworkbot",
    version="0.0.2",
    keywords=["WxWork", "bot", "API"],
    description=["WxWork bot API client"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    author="ahui,haozi",
    author_email="ahui@qunhemail.com,haozi@qunhemail.com",
    packages=find_packages(),
    install_requires=['requests'],
    python_requires='>=3',
    scripts=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ]
)
