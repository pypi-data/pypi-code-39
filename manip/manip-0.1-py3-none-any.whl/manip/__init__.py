from functools import wraps
from pathlib import Path
import os, re

def manipulate(func, *args, at='', path='.', recursive=False, ignore=True, test=True, prefix='new_', posfix='', log=True, **kwargs):
    """INSTRUCTIONS
    Decorator that transforms an [str] = function( [str]:text, *args, **kwargs ) into an function that apllies itself into a folder.\n
    The default values for the new function can be set at the decorator.
    \tat - regex to search target files
    \tpath - folder with files to change (start folder on recursive mode)
    \trecursive - makes the function call itself on all folders inside the start folder
    \tignore - ignore changes on file if function returns any error and continues to the next file
    \ttest - creates a new file with the changes for test (NOT recommended with: recursive = True)
    \tprefix/posfix - strings added before and after test files
    \tlog - shows on console steps
    
    simple usage:
        @manipulate()
        def function(text):
            return text + ' changed'
    
    Default values on decorator are set to avoid writting over important files with broken functions.\n
    \t!! ATENTION !!\n
    MAKE SURE TO ALWAYS TEST YOUR FUNCTIONS BEFORE APLLYING ANY TRUE CHANGES.
    """
    objects = os.listdir(path)

    for obj in objects:
        new_path = str(Path(path) / obj)

        if log: print('found:  '+ new_path)
        if os.path.isfile(new_path) and re.search(at, new_path):
            if log: print('working on file...')
            with open(new_path, 'r') as f:
                if log: print('\tloading file...')
                text = ''
                for line in f.readlines(): text += line

            if log: print('\ttransforming file...')
            try:
                new_text = func( *(text,)+args, **kwargs )
            except Exception as e:
                if ignore:
                    if log: print('\t\tERROR: Could not make changes on file.')
                    continue
                else:
                    raise(e)

            with open((Path(path) / (prefix + obj + posfix)) if test else new_path, 'w') as f:
                if log: print('\tsaving file...')
                f.write(new_text)

        elif recursive and os.path.isdir(new_path):
            manipulate(func, *args, at=at, path=path, recursive=recursive, ignore=ignore, test=test, prefix=prefix, posfix=posfix, log=log, **kwargs)


def manip( at='', path='.', recursive=False, ignore=True, test=True, prefix='new_', posfix='', log=True ):
    """INSTRUCTIONS
    Decorator that transforms an [str] = function( [str]:text, *args, **kwargs ) into an function that apllies itself into a folder.\n
    The default values for the new function can be set at the decorator.
    \tat - regex to search target files
    \tpath - folder with files to change (start folder on recursive mode)
    \trecursive - makes the function call itself on all folders inside the start folder
    \tignore - ignore changes on file if function returns any error and continues to the next file
    \ttest - creates a new file with the changes for test (NOT recommended with: recursive = True)
    \tprefix/posfix - strings added before and after test files
    \tlog - shows on console steps
    
    simple usage:
        @manipulate()
        def function(text):
            return text + ' changed'
    
    Default values on decorator are set to avoid writting over important files with broken functions.\n
    \t!! ATENTION !!\n
    MAKE SURE TO ALWAYS TEST YOUR FUNCTIONS BEFORE APLLYING ANY TRUE CHANGES.
    """

    def decorator( func ):
        @wraps( func )
        def wrapper(*args, at=at, path=path, recursive=recursive, ignore=ignore, test=test, prefix=prefix, posfix=posfix, log=log, **kwargs):
            manipulate(func, *args, at=at, path=path, recursive=recursive, ignore=ignore, test=test, prefix=prefix, posfix=posfix, log=log, **kwargs)
        return wrapper
    return decorator
