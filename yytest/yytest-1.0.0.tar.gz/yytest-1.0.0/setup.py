from setuptools import setup, find_packages

setup(
    name = "yytest",
    version = "1.0.0",
    keywords = ("pathtool","timetool", "magetool", "mage"),
    description = "time and path tool",
    long_description = "time and path tool",
    license = "MIT Licence",

    url = "https://github.com/wooyoung1029/test",
    author = "wooyoung",
    author_email = "1021218480@qq.com",

    packages = find_packages('yytest'),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)