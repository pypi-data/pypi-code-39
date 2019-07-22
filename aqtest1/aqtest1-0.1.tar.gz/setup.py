from setuptools import setup, find_packages, Extension

setup(name='aqtest1',
      version='0.1',
      description='this is just a test',
      author='HENRY TEST',
      author_email='liuyichen@std.uestc.edu.cn',
      packages=['aqtest1',],
      install_requires=['samtools','minimap2','pysam','numpy','scipy',],
      entry_points={'console_scripts':['step1=aqtest.Aquila_step1:main','step2=aqtest.Aquila_step2:main','assemble=aqtest.Aquila_assembly_based_variants_call:main','phasing=aqtest.Aquila_phasing_all_variants:main']},
      zip_safe=False)
