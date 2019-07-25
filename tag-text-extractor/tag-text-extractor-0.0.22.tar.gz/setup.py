from setuptools import setup


VERSION = "0.0.22"

setup(
    name='tag-text-extractor',
    description="Extract tag texts and word count",
    version=VERSION,
    url='https://github.com/KokocGroup/tag-text-extractor',
    download_url='https://github.com/KokocGroup/tag-text-extractor/tarball/v{}'.format(VERSION),
    packages=['tag_text_extractor'],
    install_requires=['six>=1.0.0,<1.11.0', 'lxml==3.4.4']
)
