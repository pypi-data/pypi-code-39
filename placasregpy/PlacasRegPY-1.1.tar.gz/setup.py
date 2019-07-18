import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PlacasRegPY",
    version="1.1",
    author="Eyvar García",
    author_email="eyvar.0823@gmail.com",
    description="Este es un pequeño código de un programa para hacer identificación de matrículas vehiculares, para conocer a que tipo de vehículo/entidad le pertenece dicha matricula.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LightKnight23/RegMatriculasPy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
