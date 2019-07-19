import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vkapi",
    version="1.0",
    author="VerZsuT",
    author_email="sacha3032104@gmail.com",
    description="Python library for working with the vk.com API.",
    install_requires="requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VerZsuT/vkapi",
    packages=['vkapi', 'vkapi/modules'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
