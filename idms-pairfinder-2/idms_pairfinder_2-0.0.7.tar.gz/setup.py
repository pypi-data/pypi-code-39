

######################################################################################
#
# YOU CAN / SHOULD EDIT THE FOLLOWING SETTING
#
######################################################################################

PKG_NAME = 'idms_pairfinder_2'

VERSION = (0, 0, 7)

# list all required packages here:

REQUIRED_PACKAGES = ['wtbox>=0.0.53']


### install package as emzed extension ? #############################################
#   -> package will appear in emzed.ext namespace after installation

IS_EXTENSION = True


### install package as emzed app ?  ##################################################
#   -> can be started as app.idms_pairfinder_2()
#   set this variable to None if this is a pure extension and not an emzed app

APP_MAIN = "idms_pairfinder_2.app:run"


### author information ###############################################################

AUTHOR = 'Patrick Kiefer'
AUTHOR_EMAIL = 'pkiefer@ethz.ch'
AUTHOR_URL = ''


### package descriptions #############################################################

DESCRIPTION = "An APP for untargeted feature extraction from isotope dilution metabolomics data."
LONG_DESCRIPTION = """
An emzed2 application for LC-MS data acquired with Orbitrap high mass resolution instruments.\n
The application allows untargeted extraction of metabolites based on isotope dilution 
mass spectrometry (IDMS) method. For each metabolite a pair of an natural labeled [12C] and an 
uniformly 13C labeled [13C] isotopologue is present in the same sample, since the sample is a 
mixture of respective cell extracts. 
As unlabeled and labeled isotopologues have the same physicochemical properties, the corresponding 
LC-MS peaks will co-elute and the m/z difference equals \n
n* (mz.C13 - mz.C12)*z \n 
where n corresponds to the number of the metabolite carbon atoms,
mz.c12 is the m/z of the 12C isotope, mz.C13 equals the m/z of the correpsonding 13C isotope, 
and z is the charge state of the ions. 
In addition, untargeted metabolite extraction is not only based on analysis of an IDMS sample, 
but also on individual LC-MS measurements of the corresponding [12C] and the [13C] extracts, 
respectively. Separate analysis allows direct assignment of isotopologue identity ([12C], [13C]) 
in the IDMS sample. 
Overall, this approach significantly reduces the number of false positive metabolites 
and enhances metabolite annotation as the number carbon atoms can be determined from the 
isotopologue mass distances.
"""

LICENSE = "http://opensource.org/licenses/GPL-3.0"


######################################################################################
#                                                                                    #
# DO NOT TOUCH THE CODE BELOW UNLESS YOU KNOW WHAT YOU DO !!!!                       #
#                                                                                    #
#                                                                                    #
#       _.--""--._                                                                   #
#      /  _    _  \                                                                  #
#   _  ( (_\  /_) )  _                                                               #
#  { \._\   /\   /_./ }                                                              #
#  /_"=-.}______{.-="_\                                                              #
#   _  _.=('""')=._  _                                                               #
#  (_'"_.-"`~~`"-._"'_)                                                              #
#   {_"            "_}                                                               #
#                                                                                    #
######################################################################################


VERSION_STRING = "%s.%s.%s" % VERSION

ENTRY_POINTS = dict()
ENTRY_POINTS['emzed_package'] = [ "package = " + PKG_NAME, ]
if IS_EXTENSION:
    ENTRY_POINTS['emzed_package'].append("extension = " + PKG_NAME)
if APP_MAIN is not None:
    ENTRY_POINTS['emzed_package'].append("main = %s" % APP_MAIN)


if __name__ == "__main__":   # allows import setup.py for version checking

    from setuptools import setup
    setup(name=PKG_NAME,
        packages=[ PKG_NAME ],
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        url=AUTHOR_URL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        version=VERSION_STRING,
        entry_points = ENTRY_POINTS,
        install_requires = REQUIRED_PACKAGES,
        )
   