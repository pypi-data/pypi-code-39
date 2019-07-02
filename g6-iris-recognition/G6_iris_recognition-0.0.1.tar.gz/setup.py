# import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

# setuptools.setup(
#     name="example-pkg-your-username",
#     version="0.0.1",
#     author="Gate6",
#     author_email="gate6.info@gate6.com",
#     description="iris recognition",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/pypa/sampleproject",
#     packages=setuptools.find_packages(),
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
# )


# from setuptools import setup

# def readme():
#     with open('README.md') as f:
#         README = f.read()
#     return README


# setup(
#     name="weather-reporter",
#     version="1.0.0",
#     description="A Python package to get weather reports for any location.",
#     long_description=readme(),
#     long_description_content_type="text/markdown",
#     url="https://github.com/nikhilkumarsingh/weather-reporter",
#     author="Nikhil Kumar Singh",
#     author_email="nikhilksingh97@gmail.com",
#     license="MIT",
#     classifiers=[
#         "License :: OSI Approved :: MIT License",
#         "Programming Language :: Python :: 3",
#         "Programming Language :: Python :: 3.7",
#     ],
#     packages=["weather_reporter"],
#     include_package_data=True,
#     install_requires=["requests"],
#     entry_points={
#         "console_scripts": [
#             "weather-reporter=weather_reporter.cli:main",
#         ]
#     },
# )


from setuptools import setup, find_packages

requirements = [
    'opencv-python',
    'opencv-contrib-python',
    'scikit-image',
    'scipy',
    'numpy',
    'matplotlib',
    'imutils',
]


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="G6_iris_recognition",
    version="0.0.1",
    description="A Python package to iris recognition.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Gate6",
    # author_email="gate6.info@gate6.com",
    author_email="vijay.bharati@gate6.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3",

    ],
    # packages=find_packages(),
    packages=["G6_iris_recognition"],
    include_package_data=True,
    install_requires=requirements,
    # install_requires=["requests"],
    entry_points={
        'console_scripts': [
            'G6_iris_recognition=G6_iris_recognition.main:main',
        ]
    },
)
