import setuptools

with open('requirements.txt') as f:
    requirements = f.readlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pvault",
    version="1.0.0a",
    author="oluwafenyi",
    author_email="o.enyioma@gmail.com",
    description="A password manager package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oluwafenyi/password-vault",
    license="MIT",
    package_name=["assets"],
    scripts=["pv.py", "assets/generate.py", "assets/management.py",
             "assets/password.py"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements
)
