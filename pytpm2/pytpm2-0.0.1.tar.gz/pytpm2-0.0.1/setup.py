from setuptools import setup, Extension

module = Extension( "pytpm2",
                    sources = ['pytpm2/get_random.c'],
                    libraries = ['tss2-esys'],
                    library_dirs=['/usr/local/lib'])

setup(  name = "pytpm2",
        version = '0.0.1',
        description = 'pytpm2 makes TPM 2.0 devices accessible to python through the tpm2-tss library',
        url = 'https://github.com/trustforge/pytpm2/',
        author = 'Kevin Briggs',
        author_email = 'krb686@gmail.com',
        license = 'ISC',
        ext_modules=[module])
