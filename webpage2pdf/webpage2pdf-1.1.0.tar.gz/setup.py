import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="webpage2pdf",
    version="1.1.0",
    author="chenzhun",
    author_email="863657500@qq.com",
    description="Html2pdf.Batch processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/czwchenzhun/webpage2pdf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
)
