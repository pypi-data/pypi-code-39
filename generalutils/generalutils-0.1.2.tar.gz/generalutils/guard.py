import os

class Filesystem:
    '''Guard class containing static methods to easily check filesystem functions'''
    
    @staticmethod
    def PathExist(path):
        '''Check whether a path exists
        
        Args:
            path (string): Path to the item
        Returns:
            (bool) Returns true on success
        '''

        # Check whether the path the file or directory exists
        if not os.path.exists(path):
            exception = f"Path - '{path}' does not exist"
            raise Exception(exception)
        return True

class Collections:
    '''Guard class containing static methods to easily check basic collection functions'''
    
    @staticmethod
    def IsNotNoneOrEmpty(obj):
        '''Check whether an object is none or empty
        
        Args:
            object (obj): Object which is getting checked
        Returns:
            (bool) Returns true on success
        '''

        # Check whether the object is none or empty  
        if not obj:
            exception = f"Object - '{obj}' is none or empty"
            raise Exception(exception)
        return True

class Http:
    '''Guard class containing static methods to easily check basic http functions'''

    @staticmethod
    def StatusCode(excpectedStatusCode, statusCode):
        '''Check whether the returned status codes are correct
        
        Args:
            excpectedStatusCode (StatusCode): The excpected status code
            statusCode (int): Returned status code    
        Returns:
            (bool): Returns true on success
        '''

        # Check whether the status codes are equal
        if not statusCode == excpectedStatusCode:
            raise Exception(f"Returned status code: {statusCode}, excepted status code: {excpectedStatusCode}")
        return True
