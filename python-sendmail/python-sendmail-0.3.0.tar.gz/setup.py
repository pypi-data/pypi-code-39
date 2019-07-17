import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "click",
]

setup(
    name="python-sendmail",
    version="0.3.0",
    description="Python版邮件客户端。通过代理服务器发送邮件。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/zencore-cn/",
    author="zencore-cn",
    author_email="info@zencore.cn",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["python-sendmail", "pysendmail", "sendmail", "pysendeml", "sendeml", "mail"],
    requires=requires,
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["sendmail"],
    entry_points={
        "console_scripts": [
            "pymail = sendmail:main",
            "pysendeml = sendmail:sendeml_cmd",
            "pysendmail = sendmail:sendmail_cmd",
            "pymakemail = sendmail:makemail_cmd",
        ]
    },
)