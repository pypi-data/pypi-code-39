import sys
import setuptools

if sys.version_info < (3,):
    print("Unfortunately, your python version is not supported!\n"
          + "Please upgrade at least to Python 3!")
    sys.exit(1)

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apk-cheater",
    python_requires='>=3',
    version="0.0.2",
    author="ksg97031",
    author_email="ksg97031@gmail.com",
    description="Easy to use frida gadget",
    install_requires=['frida==12.6.10'],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/ksg97031/apk-cheater",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'apk-cheater = scripts.main:run'
        ],
    },
    package_data={'scripts':
    ["loader.js"]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
