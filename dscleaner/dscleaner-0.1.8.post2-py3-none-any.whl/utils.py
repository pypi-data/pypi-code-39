
def path_splitter(path):
    """
        Cleans extra / characters, 
        splits the path in 4 parts: See example

        Parameters:
            path:
                Receives a path

        Returns:
            tuple: dictionary with the following keys:
                {full_path, path, name, extension}

        Example:
            >>> path.splitter('C:/Data/example.wav/')
            {
                'full_path':'C:/Data/example.wav',
                'path':'C:/Data/',
                'name':'example.wav',
                'extension':'wav'
            }
    """

    if(path.endswith("/")): 
        #if it ends with a slash removes it
        path = path[:-1]
    stripped_path = path.split("/")
    if("." in path[2:]): #if it has a dot means it has an extension; [2:] is used in case it is a relative path
        path = '/'.join(stripped_path[:-1])+'/' #constructs the path, except the filename
        file_name = stripped_path[-1] #gets the filename
        extension = file_name.split('.')[-1] # gets the extension
    else:
        path = '/'.join(stripped_path)+'/' #constructs the path, except the filename
        file_name = None
        extension = None
    
    if(len(path) < 2):
        #if it has only a character(possibly /, so removes it in order to avoid refering to root on mac/linux)
        #now theres a problem... if the user really wants to refer to the root? Shame, you cannot lol
        path = path[:-1]
    return {'full_path': path+file_name ,'path': path,'name': file_name,'extension': extension}


def is_number(input):
    """
        Receives an input and checks if it is actually a number
    """
    try:
        float(input)
    except ValueError as id:
        return False
    else:
        return True