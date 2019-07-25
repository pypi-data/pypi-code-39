# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

from distutils.core import setup

with open("README.txt", "r") as fh:
    long_description = fh.read()
setup(
    name='PermutationImportancePhysics',
    version='0.1',
    packages=['permutationimportancephysics',],
    license='MIT License',
    long_description=long_description,
    url='https://github.com/aghoshpub/permutationImportancePhysics',
    author='A Ghosh'
)
