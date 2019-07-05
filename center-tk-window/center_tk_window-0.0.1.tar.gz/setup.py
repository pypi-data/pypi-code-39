import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="center_tk_window",
    version="0.0.1",
    author="Jarik Marwede",
    author_email="jarikmarwede@zoho.eu",
    description="Functions for centering tkinter windows on parent or on screen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jarikmarwede/center-tk-window",
    packages=setuptools.find_packages(),
    py_modules=["center_tk_window"],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
