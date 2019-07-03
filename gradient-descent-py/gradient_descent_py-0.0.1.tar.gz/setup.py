
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gradient_descent_py",
    version="0.0.1",
    author="Jesus Edel Cereceres Delgado",
    author_email="jesus.edelcereceres@gmail.com",
    description="A gradient descent to python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cereceres/gradient-descent-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
