import setuptools

setuptools.setup(
    name='univarfem',
    version='0.0.1',
    author='Daniel Tait',
    author_email='tait.djk@gmail.com',
    description='FEM solver for univariate PDEs',
    url='https://github.com/danieljtait/funicular-expert-machine',
    packages=setuptools.find_packages(exclude=('docs',)),
)