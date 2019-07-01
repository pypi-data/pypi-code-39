from setuptools import setup


def _do_setup(name):
    setup(
        name=name,
        author='Elementl',
        license='Apache-2.0',
        classifiers=[
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
        ],
    )


if __name__ == '__main__':
    _do_setup('lakehouse')
