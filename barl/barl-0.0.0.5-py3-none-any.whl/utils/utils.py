####################################################
#
# This Work is written by Nikolai Rozanov <nikolai>
#
# Contact:  nikolai.rozanov@gmail.com
#
# Copyright (C) 2018-Present Nikolai Rozanov
#
####################################################

####################################################
# IMPORT STATEMENTS
####################################################

# >>>>>>  Native Imports  <<<<<<<

# >>>>>>  Package Imports <<<<<<<

# >>>>>>  Local Imports   <<<<<<<


####################################################
# CODE
####################################################
def unzip(zipedList):
    """
    unzips
    """
    temp = list( zip( *zipedList ) )

    return list( temp[0] ), list( temp[1] )






####################################################
# MAIN
####################################################


# EOF
