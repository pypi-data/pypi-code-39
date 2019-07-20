import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
name='simple-plugin2',
version='1.0',
license='BSD',
author='John Doe',
author_email='john@example.org',
platforms=['any'],
py_modules=['simple_plugin'],
entry_points="""
[segno.plugin.converter]
simple = simple_plugin:write
""",
install_requires=['segno'],
)