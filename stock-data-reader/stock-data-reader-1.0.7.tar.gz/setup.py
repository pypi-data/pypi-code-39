from setuptools import setup


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="stock-data-reader",
    version="1.0.7",
    description="A Python Package to get the stock data price for a company.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/mukulkkumar/stock-data",
    author="Mukul Kumar",
    author_email="mukulkkumarr@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["stock_data_reader"],
    include_package_data=True,
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "stock-data-reader=stock_data_reader.stockreader:StockReader.read_data",
        ]
    },
)
