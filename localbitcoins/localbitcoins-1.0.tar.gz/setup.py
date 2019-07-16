from distutils.core import setup

setup(
    name="localbitcoins",
    version="1.0",
    packages=["localbitcoins"],
    url="https://github.com/yarfuo/localbitcoins-lib",
    license="MIT License",
    author="Ilya",
    author_email="yarfuo@protonmail.com",
    description="Simple wrapper for localbitcoins.com API",
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
        "Typing :: Typed",
    ],
    keywords=["localbitcoins", "wrapper", "cryptocurrency"],
    download_url="https://github.com/yarfuo/localbitcoins/tarball/v1.0",
)
