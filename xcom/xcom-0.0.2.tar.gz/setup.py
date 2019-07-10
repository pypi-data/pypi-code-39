from setuptools import setup

with open('version.txt') as f:
    ver = f.read().strip()

description = '''
    Schneider Electric Sepam simulator. 
    Supports: disturbance recordings, time stamped buffer.
'''

setup(
    name='xcom',
    version=ver,
    author='Vinogradov Dmitry',
    author_email='dgrapes@gmail.com',
    description=description,
    license='MIT',
    packages=['xcom', 'xcom.modbus'],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
