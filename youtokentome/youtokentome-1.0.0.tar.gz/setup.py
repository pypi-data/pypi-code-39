from setuptools import setup, Extension, find_packages


extensions = [
    Extension('_youtokentome_cython',
              ['youtokentome/cpp/yttm.cpp', 'youtokentome/cpp/bpe.cpp', 'youtokentome/cpp/utils.cpp', 'youtokentome/cpp/utf8.cpp'],
              extra_compile_args=['-std=c++11', '-pthread', '-O3'],
              language='c++'
              ),
]

setup(
    name='youtokentome',
    version='1.0.0',
    packages=find_packages(),
    python_requires='>3.5.0',
    install_requires=['Click>=7.0'],
    entry_points={
        'console_scripts': [
            'yttm = youtokentome.yttm_cli:main',
        ],
    },
    author='Ivan Belonogov',
    ext_modules=extensions,
)
