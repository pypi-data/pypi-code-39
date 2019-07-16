import setuptools

from setuptools.command.install import install

# https://blog.niteo.co/setuptools-run-custom-code-in-setup-py/
class CustomInstallCommand(install):
    def run(self):
        print("Hello, how are you? :)")
        install.run(self)

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

long_description_md = """
polaroidme is a simple to use command-line-tool for placing an image into a
Polaroid-like frame and optionally put a title / description on the bottom.
The default font mimics scribbled handwriting but any (ttf-)font
which suits your taste is supported. polaroidme offers basic features
like auto-scaling up-/downwards and/or cropping, using any (ttf-)font,
supports high-res output and gets the job just done well.
It is intended & mainly used as a command-line-tool but can also be used as
a python-module (means: it exports its core-function).

polaroidme is actively maintained & developed (2019).
To see if it fits your needs take a look at the project's
github-repo and check out the `examples`_

Contributions are welcome, and they are greatly appreciated!

_`examples`: https://github.com/s3h10r/polaroidme/blob/master/README.md
"""

setuptools.setup(
     name='polaroidme',
     version='0.9.2',
     scripts=['polaroidme/polaroidme'] ,
     author="Sven Hessenmüller",
     author_email="sven.hessenmueller@gmail.com",
     description="converts an image into vintage polaroid style",
     include_package_data=True,
     long_description=long_description_md,
     url="https://github.com/s3h10r/polaroidme",
     packages=setuptools.find_packages(),
     install_requires=requirements,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
         "Development Status :: 4 - Beta",
         "Environment :: Console",
         "Topic :: Multimedia :: Graphics",
         "Topic :: Utilities",
     ],
     cmdclass={
        'install': CustomInstallCommand,
     },
)
