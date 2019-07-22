from setuptools import setup, find_packages, Extension

setup(name='aqtest1',
      version='0.7.2',
      description='please install samtools and minimap2 from bioconda(anaconda) in advance',
      author='HENRY TEST',
      author_email='liuyichen@std.uestc.edu.cn',
      packages=['aqtest1',],
      install_requires=[
      'pysam',
      'numpy',
      'scipy',],
      entry_points={'console_scripts':['step1=aqtest1.Aquila_step1:main','step2=aqtest1.Aquila_step2:main','assemble=aqtest1.Aquila_assembly_based_variants_call:main','phasing=aqtest1.Aquila_phasing_all_variants:main']},
      zip_safe=False)
