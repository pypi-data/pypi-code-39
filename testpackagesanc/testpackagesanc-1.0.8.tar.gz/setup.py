import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testpackagesanc",
    version="1.0.8",
    author="Jin Xin",
    author_email="jin.xin@accenture.com",
    description="testConfig",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["testpackagesanc"],
    scripts=['testpackagesanc/config.py'],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    entry_points={
        "console_scripts": ["config = testpackagesanc.config:get_config",]
    },
)