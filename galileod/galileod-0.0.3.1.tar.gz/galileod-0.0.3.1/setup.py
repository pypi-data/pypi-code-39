from setuptools import setup, find_packages
from setuptools.extension import Extension

from Cython.Build import cythonize
from Cython.Distutils import build_ext

from pathlib import Path
from shutil import copy

class BuildExt(build_ext):
    def run(self):
        build_ext.run(self)
        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent

        target_dir = root_dir if self.inplace else build_dir
        copy(Path('galileo','__init__.py'), target_dir)

setup(
    name='galileod',
    version='0.0.3.1',
    ext_modules=cythonize([Extension('galileo.*', ['galileo/*.py'])],
                          build_dir='build',
                          compiler_directives={}),

    cmdclass={'build_ext': BuildExt},

    entry_points={
        'console_scripts': [
            'galileo-cli = galileo.entry:cli_main',
            'galileod = galileo.entry:daemon_main',
        ]
    },

    python_requires='>=3.6.7',

    setup_requires=[
        "pytest-runner>=4.2",
    ],

    install_requires=[
        'flask>=1.0.2',
        'flask-cors>=3.0.7',
        'docker>=3.7.0',
        'requests>=2.21.0',
        'pycryptodome>=3.7.3',
        'cryptography>=2.6.1',
        'pyopenssl>=19.0.0',
        'python-jose>=3.0.1',
    ],

    tests_require=[
        'pytest>=4.1.1',
    ],

    packages=[],
)
