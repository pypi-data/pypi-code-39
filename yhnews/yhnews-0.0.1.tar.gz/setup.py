import setuptools
 
with open('README.md', "r") as fh:
    long_description = fh.read()
 
with open('LICENSE') as fp:
    license = fp.read()
 
setuptools.setup(
    name="yhnews",
    version="0.0.1",
    description='news for event clustering.',
    long_description=long_description,
    author='geodgechen',
    author_email='geodge831012@163.com',
    maintainer='geodgechen',
    maintainer_email='geodge831012@163.com',
    url='https://github.com/geodge831012',
    packages=setuptools.find_packages(),
    license=license,
    platforms=['any'],
    classifiers=[]
)
