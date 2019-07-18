from setuptools import setup, find_packages

longdesc = 'Current capabilities: '\
    'Radial wavefunction densities; '\
    'Spherical harmonics; '\
    'Real-space densities of hydrogenic eigenfunctions; '\
    'Real-space density of real-valued wavefunctions; '\
    'Real-space density isosurfaces and polygon data with .obj output'

setup(
    name='hwaves',
    version='0.0.4',
    url='https://github.com/lensonp/hwaves.git',
    description='Compute and plot hydrogenic wavefunctions',
    long_description=longdesc,
    author='Lenson A. Pellouchoud',
    license='MIT',
    author_email='',
    install_requires=['numpy','scipy','masstable','periodictable','matplotlib','scikit-image'],
    packages=find_packages(),
    package_data={}
    )


