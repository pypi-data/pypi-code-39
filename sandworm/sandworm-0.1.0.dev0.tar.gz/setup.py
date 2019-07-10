from setuptools import setup
about = {}
with open("sandworm/__about__.py") as fp:
    exec(fp.read(), about)

setup(name=about["__title__"],
      version=about["__version__"],
      description=about["__summary__"],
      url="https://github.com/zcutlip/sandworm.git",
      packages=['sandworm'],
      entry_points={
          'console_scripts': ['sandworm=sandworm.cli:main'], },
      python_requires='>=3.7',
      install_requires=[],
      package_data={'sandworm': ['config/*']},
      )
