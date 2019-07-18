# coding=utf-8

import os
from setuptools import setup, find_packages

def get_version():
    """
    get version
    """
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import aifashion
    return aifashion.__version__


if __name__ == '__main__':
    setup(
        name='aifashion_sdk',
        version=get_version(),
        description=(
            'AIFashion® Python SDK',
        ),
        long_description=open('README_cn.md').read()+open('README_en.md').read(),
        long_description_content_type='text/markdown',
        author='Sky Zhang',
        author_email='sky.atomse@gmail.com',
        maintainer='Sky Zhang',
        maintainer_email='sky.atomse@gmail.com',
        license='MIT License',
        packages=find_packages(),
        platforms=["Linux", "Darwin", "Windows"],
        # url='https://github.com/atomse/aifashion',
        python_requires='>=3',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Operating System :: MacOS',
            'Operating System :: POSIX',
            'Operating System :: Microsoft',
            'Operating System :: Microsoft :: Windows :: Windows NT/2000',
            'Operating System :: POSIX :: BSD',
            'Operating System :: POSIX :: BSD :: FreeBSD',
            'Operating System :: POSIX :: BSD :: NetBSD',
            'Operating System :: POSIX :: BSD :: OpenBSD',
            'Operating System :: POSIX :: Linux',
            'Operating System :: POSIX :: SunOS/Solaris',
            # 'Intended Audience :: Science/Research',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
        install_requires=open('requirements.txt').read().split(),
        # entry_points={
        #     "console_scripts": [
        #         "aifashion=aifashion.cli:run_aifashion_cli",
        #     ],
        # },
        extras_require={
            'docs': [
                'sphinx',
                'sphinxcontrib-programoutput',
                'sphinx_rtd_theme',
                'numpydoc',
            ],
            'tests': [
                'pytest>=4.0',
                'pytest-cov'
            ],
        },
        include_package_data = True,
        # package_data = {'aifashion_test': test_files},
        zip_safe=False,
    )
