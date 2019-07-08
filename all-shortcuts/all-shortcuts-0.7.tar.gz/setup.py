from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='all-shortcuts',
    version='0.7',
    author="Wilson Hernández Ortiz",
    author_email="who@whooami.me",
    description="a app that simplify our shape of write orders",
    scripts=['go','get','send'],
    packages=['shortcuts','shortcuts.services','shortcuts.services.libs'],
    url="https://github.com/whohe/shortcuts",
    long_description=long_description,
    long_description_content_type="text/markdown"
)

