import os

class Filesystem:
    '''Guard class containing static methods to easily check filesystem functions'''
    
    @staticmethod
    def PathExist(path):
        '''Check whether a path exists
        
        Args:
            path (string): Path to the item
        '''

        # Check whether the path the file or directory exists
        if not os.path.exists(path):
            exception = f"Path - '{path}' does not exist"
            raise Exception(exception)
        return True
