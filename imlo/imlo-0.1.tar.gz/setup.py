import setuptools

with open("DESCRIPTION.md", "r") as readme:
    long_description = readme.read()

with open("requirements.txt", "r") as requirements_file:
    requirements_text = requirements_file.read()

requirements = requirements_text.split()

setuptools.setup(
    name="imlo",
    version="0.1",
    description="Imlo package",
    url="https://github.com/imlouz/imlo",
    author="Imlo Developers",
    author_email="imloloyihasi@gmail.com",
    license="GPL-3.0",
    packages=setuptools.find_packages(),
    zip_safe=False,
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=requirements,
)
