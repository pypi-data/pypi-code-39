from setuptools import setup, find_packages 

setup(
  name="rename_ts_folder",
  version="0.1.1",
  packages=find_packages(),
  entry_points={
    "console_scripts": ["rtsf=rename_ts_folder.rename_folder:main"]
  },
  author="Yuhang (Steven) Wang",
  description="Rename a folder based on the numbering of a file's name inside that folder",
)
