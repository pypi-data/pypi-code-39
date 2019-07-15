import setuptools

setuptools.setup(
    name="needle-forms",
    version="0.0.2",
    author="dmiranda",
    author_email="dmiranda@ciandt.com",
    description="Abstraction layer to GCP resources",
    url="https://github.com/ciandt-dev/needle-forms",
    packages=setuptools.find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
