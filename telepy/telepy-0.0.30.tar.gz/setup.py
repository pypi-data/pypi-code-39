import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="telepy",
    version="0.0.30",
    author="eliko",
    author_email="eliko2411@hi2.in",
    description="Telegram bot library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/2411eliko/tele",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],    
    python_requires="~=3.4",
    packages=setuptools.find_packages(),
    install_requires = ["requests"]
)

