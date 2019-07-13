from setuptools import setup



with open("README", "r") as fh:
    long_description = fh.read()

setup(
    name="riskcontrol",
    version="0.1.5",
    author="SimaShanhe",
    author_email="hsliu_em@126.com",
    description="risk control modeling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)