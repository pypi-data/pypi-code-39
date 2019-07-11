import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    'pycrypto==2.6.1'
]
setuptools.setup(
    name="gxcutil",
    version="0.1.18",
    author="Lucid",
    author_email="contact@lucid.dev",
    description="Python utility library for GXC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Game-X-Coin/gxcutil",
    packages=setuptools.find_packages(),
    install_requires=requires,
    classifiers=[
    ],
)
