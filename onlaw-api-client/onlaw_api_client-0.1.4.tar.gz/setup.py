import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="onlaw_api_client",
    version="0.1.4",
    author="Onlaw",
    author_email="jens@onlaw.dk",
    description="client for api.onlaw.dk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Onlaw/onlaw_api_client",
    packages=setuptools.find_packages(),
    install_requires=["aiohttp",
                      "async",
                      "asyncio",
                      "attrs",
                      "auth0-python",
                      "certifi",
                      "chardet",
                      "idna",
                      "multidict",
                      "requests",
                      "urllib3",
                      "yarl"],
    tests_require=["autopep8",
                   "flake8",
                   "flake8-mypy",
                   "mypy",
                   "pip-tools",
                   "pre-commit",
                   "setuptools ",
                   "twine",
                   "wheel"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
