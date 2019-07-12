"""
Utillities for exploring the filesystem
Created by 復讐者 on 12/27/16
"""
__author__ = '復讐者'

import os
import datetime


def getDateForMakingFileName():
    """Returns the standard string format of today's date to be used in making a file name"""
    return datetime.date.isoformat( datetime.date.today() )


def getTimestampForMakingFileName():
    """Returns the standard string format of timestamp used in making a file name"""
    return datetime.datetime.now().strftime( "%Y-%m-%d_%H:%M:%S" )


def getSystemRoot():
    """
    Returns the base directory path.
    """
    return os.getenv( "HOME" )


def makeDataFileList( folderPath, exclude=[ ] ):
    """
    Returns a a list of all files in the source directory
    so that each file has its path appended to it.

    Args:
        folderPath: The path to get file names from
        exclude: file names which should not be included in the output list
    """
    exclude = exclude if any( exclude ) else [ '.DS_Store' ]
    datafiles = [ ]
    for root, dirs, files in os.walk( folderPath ):
        for name in files:
            if name not in exclude:
                datafiles.append( os.path.join( root, name ) )

    return datafiles


def makeDataFileIterator( folderPath, exclude=[ ] ):
    """
    Returns an iterator of all files in the source directory
    so that each file has its path appended to it.

    Args:
        folderPath: The path to get file names from
        exclude: file names which should not be included in the output list
    """
    exclude = exclude if any( exclude ) else [ '.DS_Store' ]
    for root, dirs, files in os.walk( folderPath ):
        for name in files:
            if name not in exclude:
                yield os.path.join( root, name )


if __name__ == '__main__':
    pass
