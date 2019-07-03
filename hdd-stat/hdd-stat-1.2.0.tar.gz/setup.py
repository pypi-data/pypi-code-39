from setuptools import setup, find_packages

setup(
    name = "hdd-stat",
    description = "",
    version = "1.2.0",
    author = 'Lajos Santa',
    author_email = 'santa.lajos@gmail.com',
    url = 'https://github.com/voidpp/hdd-stat',
    install_requires = [
        "prettytable~=0.7",
        "psutil~=5.6",
        "Flask~=1.0",
    ],
    scripts = [
        "bin/hdd-stat"
    ],
    packages = find_packages(),
)

