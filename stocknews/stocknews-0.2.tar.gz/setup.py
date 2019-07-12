import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='stocknews',
                 version='0.2',
                 description='PoC for scraping Yahoo News with sentiment analysis',
                 url='http://github.com/primus852/stock-news.git',
                 author='Torsten Wolter',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 author_email='tow.berlin@gmail.com',
                 packages=setuptools.find_packages(),
                 license='MIT',
                 zip_safe=False)
