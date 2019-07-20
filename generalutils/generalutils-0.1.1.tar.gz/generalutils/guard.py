import os

class Filesystem:
    '''Guard class containing static methods to easily check filesystem functions'''
    
    @staticmethod
    def PathExist(path):
        '''Check whether a path exists
        
        Args:
            path (string): Path to the item
        Returns:
            (bool) returns true on success
        '''

        # Check whether the path the file or directory exists
        if not os.path.exists(path):
            exception = f"Path - '{path}' does not exist"
            raise Exception(exception)
        return True

class Collections:
    '''Guard class containing static methods to easily check basic collection functions'''
    
    @staticmethod
    def IsNotNoneOrEmpty(object):
        '''Check whether an object is none or empty
        
        Args:
            object (obj): Object which is getting checked
        Returns:
            (bool) returns true on success
        '''

        # Check whether the object is none or empty  
        if not object:
            exception = f"object - '{object}' is none or empty"
            raise Exception(exception)
        return True
