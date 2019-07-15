from setuptools import setup

"""
with open("README.md", "r") as fh:
    long_description = fh.read()
"""

setup(
    name='DummyValidator',  ###
    version='0.0.0.1',
    description='like SocValidator',
    long_description='like SocValidator',
    long_description_content_type="text/markdown",
    url='https://www.xbox.com/en-US/',
    author='LJ',
    author_email='v-lyjen@microsoft.com',
    license='Microsoft',
    packages=['SocValidator'],
    zip_safe=False,
    install_requires=[
        'clipboard',
        'PyQt5',
        'matplotlib',
        'PySerial',
        'nidaqmx'
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'License :: OSI Approved :: Microsoft License',
        'Programming Language :: Python :: 3.7'
    ]
)

