from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="phoneNum",
    version="0.2",
    author="Anning Chen",
    author_email="anchen@milie.co.jp",
    description="get company information with phone number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pythonml/douyin_image",
    packages=find_packages(),
    #install_requires=['Pillow>=5.1.0', 'numpy==1.14.4'],
    entry_points={
        'console_scripts': [
            'phoneNum=phoneNum:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
