import setuptools

setuptools.setup(
    name="framewatchergui",
    version="0.0.1",
    description="",
    url="https://github.com/alberttxu/framewatchergui",
    author="Albert Xu",
    author_email="albert.t.xu@gmail.com",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["PySimpleGUI", "pexpect"],
    entry_points={
        "console_scripts": ["framewatchergui = framewatchergui.__main__:main"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
