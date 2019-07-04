
import setuptools

setuptools.setup(
    name="EMOIdentifier",
    version="1.0.2",
    author="Omkarendra Tiwari",
    author_email="omkarendra@cse.iitb.ac.in",
    description="An extract method refactoring algorithm",
   # long_description=long_description,
   # long_description_content_type="text/markdown",
    url="https://github.com/omkarendra/segmentation",
    packages=setuptools.find_packages(),
    install_requires=['numpy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


