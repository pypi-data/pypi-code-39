"""
USAGE: 
   o install in develop mode: navigate to the folder containing this file,
                              and type 'python setup.py develop --user'.
                              (ommit '--user' if you want to install for 
                               all users)                           
"""


from setuptools import setup
# HOME=os.path.expanduser("~")


## use setup to install SDF package and executable scripts
setup(name='sdformat',
      version='0.23.2',
      description='Python Interface of a Standard Data Format',
      url='',
      author='Burkhard Geil, Filip Savic, Ilyas Kuhlemann',
      author_email='ilyasp.ku@gmail.com',
      license='GNU GPLv3',
      packages=['SDF',
                "SDF.convert",
                "SDF.file_io",
                "SDF.GUI",
                "SDF.GUI.controller",
                "SDF.GUI.model",
                "SDF.GUI.view",
                "SDF.CLI",
                "SDF.sdf_wrapper",
                "SDF.extern"],
      entry_points={
          "console_scripts": [
              "sdf-convert-mfp2sdf=SDF.CLI.sdf_convert_mfp2sdf:main",
              "sdf-convert-lsm2sdf=SDF.CLI.sdf_convert_lsm2sdf:main",
              "sdf-convert-oif2sdf=SDF.CLI.sdf_convert_oif2sdf:main",
              "sdf-convert-oib2sdf=SDF.CLI.sdf_convert_oib2sdf:main",
              "sdf-convert-jpk2sdf=SDF.CLI.sdf_convert_jpk2sdf:main",
              "sdf-convert-sdf2forcesdf=SDF.CLI.sdf_convert_sdf2forcesdf:main"
          ],
          "gui_scripts": [
              "sdf-browser = SDF.GUI.sdf_browser:main"
          ]
      },
      install_requires=['numpy',
                        "Pillow",
                        "scipy",
                        'igor==0.3',  # For ibw files. This is so far the only external package
                        # (== not single module file) that is required.
                        # Maybe we can make it optional, for users who are
                        # interested in converting ibw files.                                                
                        "nose",
                        "click",
                        "python-dateutil"],
      zip_safe=False)

print("="*80)
print("SDF ships its own copies of the following packages, to increase the chance")
print("of working even if those packages are not available via pypi.org or if")
print("major changes are done to these packages:")
print(" - mfpfile")
print(" - jpkfile")
print(" - tifffile")
print(" - oiffile")
print("Per default, SDF will use its own copies of these. If you rather want to use ")
print("Your system's versions of these packages, you can change SDF's config in:")
print("   ~/.sdf/config.json (will be generated during first usage of SDF)")
print("")
print("="*80)
print("If you want to use the GUI, you need to have matplotlib and PyQt5 installed!")
print("You can do that e.g. with the command `$ pip install --user matplotlib PyQt5` .")
print("="*80)
