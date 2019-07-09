from setuptools import find_packages, setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='Beads',
    version='0.1.0',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['click', 'eel', 'markdown'],
    entry_points={
          'console_scripts': [
              'beads = beads.main:beads'
          ]
      },
)
