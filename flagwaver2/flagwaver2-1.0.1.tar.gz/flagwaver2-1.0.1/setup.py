from setuptools import find_packages, setup

setup(
    name='flagwaver2',
    version='1.0.1',
    python_requires='>=3',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)