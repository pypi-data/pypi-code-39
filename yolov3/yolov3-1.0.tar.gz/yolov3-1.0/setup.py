import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yolov3",
    version="1.0",
    author="qingtian",
    author_email="",
    description="Keras(TF backend) implementation of yolo v3 objects detection. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=['numpy==1.14.4', 'Tensorflow-gpu==1.5.0', 'Keras==2.1.3', 'OpenCV==3.4'],
    entry_points={
        'console_scripts': [
            'demo=demo:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)