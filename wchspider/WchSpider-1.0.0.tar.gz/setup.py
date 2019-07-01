from setuptools import setup,find_packages
setup(
    name = "WchSpider",
    version = "1.0.0",
    keywords = ("pip", "requests","aiohttp", "spider"), 
    description = "WchSpider",
    long_description = "Aiohttp is encapsulated to keep the speed of asynchronism, and it can be used as simple and convenient as requests.",
    url = "https://github.com/DARK1994/WchSpiders",
    author = "wch",
    author_email = "mambaout0803@163.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['aiohttp','lxml']
)