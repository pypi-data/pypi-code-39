import setuptools

def readme():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description

setuptools.setup(
    name="dyna-gsm-module",
    version="0.0.4",
    author="John D. Geliberte",
    author_email="gelibertejohn@gmail.com",
    description="GSM modules required for dynaslope 3 project",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/jgeliberte/dyna-gsm-module",
    packages=setuptools.find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=["serial","RPi.GPIO","python-gsmmodem-new","configparser"],
    entry_points={
        "console_scripts": [
            "dyna-gsm-module=dyna_gsm_module.runner:main"
        ]
    }
)