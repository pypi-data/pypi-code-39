import setuptools

setuptools.setup(
    name="SimpleHTMLBuilder",
    version="1.0.0",
    author="Kyle Beauregard",
    author_email="kylembeauregard@gmail.com",
    description="A simple HTML builder for when you don't want to touch JavaScript.",
    url='https://github.com/kbeauregard/HTMLBuilder',
    packages=setuptools.find_packages(
        include=[
            'HTMLBuilder/',
        ]
    ),
    py_modules=[
        'SimpleHTMLBuilder.__init__',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
