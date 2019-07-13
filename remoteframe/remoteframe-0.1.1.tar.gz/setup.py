import setuptools

with open("README.md", "r") as d:
    a = d.read()

setuptools.setup(
        name="remoteframe",
        version="0.1.1",
        author="James M",
        author_email="jimferd@gmail.com",
        description="Wrappers for remote exec, local exec.",
        long_description=a,
        long_description_content_type="text/markdown",
        url="http://vixal.net",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            ],
        )
