from setuptools import setup
from os import path

with open(path.join(path.dirname(__file__), 'coci/README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="coci",
    version="0.1.6",
    author="Koki Fujiwara",
    author_email="koki.fujiwara@exwzd.com",
    description="Collective Observation on Causal Inference",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=["numpy", "seaborn"],
    packages=["coci"],
)