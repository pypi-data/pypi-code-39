from setuptools import setup, find_packages, Extension

setup(name='aqtest1',
      version='0.3',
      description='this is just a test',
      author='HENRY TEST',
      author_email='liuyichen@std.uestc.edu.cn',
      packages=['aqtest1',],
      install_requires=[
      
      'pysam',
      'numpy',
      'scipy',],
      dependency_links = [
      'https://github.com/samtools/samtools/tarball/master.tar.gz#egg=samtools-1.9',
      'https://github.com/lh3/minimap2/tarball/master.tar.gz#egg=minimap2-2.17',],
      entry_points={'console_scripts':['step1=aqtest.Aquila_step1:main','step2=aqtest.Aquila_step2:main','assemble=aqtest.Aquila_assembly_based_variants_call:main','phasing=aqtest.Aquila_phasing_all_variants:main']},
      zip_safe=False)
