from setuptools import setup

setup(
    name="brevis",
    version="0.6.0",
    description="Python client for the Brevis URL shortener API",
    url="http://github.com/admiralobvious/brevis-python-client",
    author="Alexandre Ferland",
    author_email="aferlandqc@gmail.com",
    license="MIT",
    packages=["brevis"],
    zip_safe=False,
    install_requires=["requests>=2.22"],
    tests_require=[
        "pytest==5.0.1",
        "requests-mock==1.6.0"
    ],
    setup_requires=["pytest-runner==5.1"],
    platforms="any",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
