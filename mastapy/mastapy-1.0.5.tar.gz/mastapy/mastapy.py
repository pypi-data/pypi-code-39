import clr
import functools

MASTA_PROPERTIES = dict()

def masta_property(func=None, name='', *, description='', symbol='', measurement=''):
    ''' Decorator method for creating MASTA properties in Python

    Keyword arguments:
    -- func: The function that the decorator is wrapping
    -- name: The name of the property displayed in Masta
    -- description: The description of what the property does (optional)
    -- symbol: The symbol for the property displayed in Masta (optional)
    -- measurement: Unit the property displayed in, in Masta (optional)
    '''

    def decorator_masta_property(func):
        MASTA_PROPERTIES[func.__name__] = func, name, description, symbol, measurement
        return func

    return decorator_masta_property if func is None else decorator_masta_property(func)


def init(path_to_dll_folder):
    '''Initialises the Python to MASTA API interop

    Keyword arguments:
    -- path_to_dll_folder: Path to your MASTA folder that
                           includes the MastaAPI.dll file
    '''
    clr.AddReference(path_to_dll_folder + 'MastaAPI.dll')
    from SMT.MastaAPI import UtilityMethods
    UtilityMethods.InitialiseApiAccess(path_to_dll_folder)