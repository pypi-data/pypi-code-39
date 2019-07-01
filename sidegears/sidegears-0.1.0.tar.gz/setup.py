import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sidegears",
    version="0.1.0",
    author="john Tourtellott",
    author_email="john.turtle@gmail.com",
    description="Tools for browser-based desktop applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/john.tourtellott/sidegears",
    # packages=setuptools.find_packages(),
    packages=['sidegears'],
    package_data={'sidegears': [
        '../examples/pyside/*.*',
        '../examples/testbed/*.*',
        '../examples/webruntime/*.*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Operating System :: OS Independent",
    ],
)
