# -*- coding: utf-8 -*-

######################################################################################
#
# YOU CAN / SHOULD EDIT THE FOLLOWING SETTING
#
######################################################################################

PKG_NAME = 'wtbox'

VERSION = (0, 0, 54)

# list all required packages here:

REQUIRED_PACKAGES = ['hires==0.0.14']


### install package as emzed extension ? #############################################
#   -> package will appear in emzed.ext namespace after installation

IS_EXTENSION = True


### install package as emzed app ?  ##################################################
#   -> can be started as app.wtbox()
#   set this variable to None if this is a pure extension and not an emzed app

APP_MAIN = "wtbox.app:run"


### author information ###############################################################

AUTHOR = 'Patrick Kiefer'
AUTHOR_EMAIL = 'pkiefer@ethz.ch'
AUTHOR_URL = ''


### package descriptions #############################################################

DESCRIPTION = "an emzed2 extension providing additional routines for LC-MS workflow building"
LONG_DESCRIPTION = """
An emzed2 extension with additional routines for enhanced LC-MS data analysis workflow 
building. It provides additional routines for emzed Table operations, Feature extraction,
IO, peak integration, etc. 

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
        package_data={'': ['docs/*.htm']}
        )
   