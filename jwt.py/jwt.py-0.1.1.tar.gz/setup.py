from distutils.core import setup


setup(
    name='jwt.py',
    version='0.1.1',
    author='iPlant Collaborative',
    author_email='atmodevs@gmail.com',
    py_modules=['jwt'],
    install_requires=[
        'pycryptodome >= 3.8.2'
    ]
)
