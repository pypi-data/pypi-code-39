from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["PyAudio==0.2.11", "SpeechRecognition==3.8.1"]

setup(
    name="vocalist",
    version="0.0.1.dev1",
    author="Colin Lacy",
    author_email="colinjlacy@gmail.com",
    description="A package to convert speech to long-form work-flows, using plugable trained NLP models",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
