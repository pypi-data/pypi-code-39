import setuptools
import brom

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="brom",
    version=brom.__version__,
    author="Anton Shaganov (ITworks Ltd.)",
    author_email="info@itworks.group",
    description="Модуль, обеспечивающий взаимодействие с расширением «Бром» для 1С:Предприятие.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://brom.itworks.group",
#    packages=setuptools.find_packages(),
    py_modules = ['brom'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'zeep'
    ],
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://brom.itworks.group/documentation/'
    }
)