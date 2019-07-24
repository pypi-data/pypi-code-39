import re
from setuptools import find_packages, setup

docs_require = ["mkdocs>=1.0.4", "mkdocs-material==4.4.0"]

tests_require = [
    "coverage==4.5.3",
    "pytest==5.0.1",
    "pytest-django==3.5.1",
    # Linting
    "isort==4.2.5",
    "flake8==3.7.7",
    "flake8-blind-except==0.1.1",
    "flake8-debugger==1.4.0",
]

with open("README.md") as fh:
    long_description = re.sub(
        "<!-- start-no-pypi -->.*<!-- end-no-pypi -->\n",
        "",
        fh.read(),
        flags=re.M | re.S,
    )

setup(
    name="django-datahooks",
    version="0.0.1",
    description="Django datahooks",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/labd/django-datahooks",
    author="Lab Digital",
    author_email="opensource@labdigital.nl",
    install_requires=["Django>=1.11"],
    tests_require=tests_require,
    extras_require={"docs": docs_require, "test": tests_require},
    entry_points={},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.11",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    zip_safe=False,
)
