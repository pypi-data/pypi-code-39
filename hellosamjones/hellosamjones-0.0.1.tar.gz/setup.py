from setuptools import setup
with open("README.md","r") as fh:
    long_desription = fh.read()
setup(
    name='hellosamjones',
    version='0.0.1',
    description="Say Hello name",
    py_modules=["helloworld"],
    package_dir={'':'src'},
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent"
        ],
        long_desription=long_desription,
        long_desription_content_type="text",
        url = "https://github.com/samjones310/helloworld",
        author = "Sam Jones",
       # author_email = "samjones31098@gmail.com"
)