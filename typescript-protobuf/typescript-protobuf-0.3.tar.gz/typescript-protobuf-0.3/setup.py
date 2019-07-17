from setuptools import setup

version = '0.3'

setup(
    name='typescript-protobuf',
    version=version,
    description='Generate d.ts files for JSON objects from protobuf specs',
    keywords='typescript proto',
    license='The MIT License (MIT)',
    author='Cyrille Corpet',
    author_email='cyrille@bayesimpact.org',
    py_modules=[],
    install_requires=['protobuf'],
    url='https://github.com/bayesimpact/json-ts-protobuf',
    download_url=f'https://github.com/bayesimpact/json-ts-protobuf/archive/v{version}.tar.gz',
    scripts=['src/protoc-gen-json-ts'],
)
