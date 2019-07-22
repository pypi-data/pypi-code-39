import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trpc",
    version="0.1.0",
    author="Gabriel Alves",
    author_email="itsmealves@gmail.com",
    description="dynamic Template-less RPC tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itsmealves/trpc",
    packages=setuptools.find_packages(),
    install_requires=[
        'pika'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
