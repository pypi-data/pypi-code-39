from setuptools import setup, find_packages

def readme():
    with open("README.md") as f:
        README = f.read()
    return README

setup(
    name="reliability",
    version="0.1.5",
    description="Reliability Engineering toolkit for Python",
    author="Matthew Reid",
    author_email="m.reid854@gmail.com",
    license="MIT",
    url="https://github.com/MatthewReid854/reliability",
    keywords=["reliability","engineering","RAM","weibull","survival analysis","censored data","lifelines","probability distributions","probability","quality"],
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3',
    install_requires=["autograd>=1.2.0",
                      "scipy>=1.2.1",
                      "numpy>=1.16.2",
                      "matplotlib>=3.0.3",
                      "pandas>=0.23.4",
                      "autograd-gamma>=0.4.1",
    ],
    packages=find_packages(),
    package_data={"reliability": ["../README.md", "../LICENSE", "../MANIFEST.in"]},
)
