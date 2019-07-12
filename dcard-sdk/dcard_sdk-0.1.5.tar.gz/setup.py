import setuptools

requirements = [
    'schema==0.7.0',
    'requests==2.22.0',
]

setuptools.setup(
    name="dcard_sdk",
    license='MIT',
    # download_url='https://github.com/kirillismad/dcard_wrapper/archive/0.1.2.tar.gz',
    version="0.1.5",
    author="Pech Kirill",
    author_email="pechkirill@gmail.com",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)
