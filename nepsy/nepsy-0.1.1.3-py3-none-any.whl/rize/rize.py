import nep
import os
from os import listdir
from os.path import isfile, join
import simplejson
import shutil
import sys
import time
import nep
import subprocess


def getRIZEpath():
    import os
    path = os.environ['RIZE']
    print (path)
    return path

def setRIZEpath(new_path, additional = "/"):
    import os
    if os.environ.get('OS','') == 'Windows_NT':
        from subprocess import Popen
        from subprocess import CREATE_NEW_CONSOLE
        command = 'setx RIZE "' + new_path + additional + '"'
        Popen(command, creationflags=CREATE_NEW_CONSOLE)
        
    os.environ["RIZE"] = new_path


# -----------------------------------. onCreateFolder --------------------------------
# Save JSON file
def onCreateFolder(path, name_folder):
    if not os.path.exists(path + "/" + name_folder):
        os.makedirs(path + "/" + name_folder)



# -----------------------------------. onSaveJSON --------------------------------
# Save JSON file
def onSaveJSON(path, name, code):
    file_save = open(path +  "/" +  name + ".json" , "w")
    file_save.write(simplejson.dumps(code, separators=(',', ':'), sort_keys=True,  indent=4))
    file_save.close()

# -----------------------------------. onSaveFile --------------------------------
# Save JSON file
def onSaveFile(path, name, code):
    file_save = open(path +  "/" +  name , "w")
    file_save.write(code.encode('utf8'))
    file_save.close()


        
# -------------------------------------  json2dict  --------------------------------
# Description: Convert json string to python dictionary
def json2dict(s, **kwargs):
    """Convert JSON to python dictionary. See jsonapi.jsonmod.loads for details on kwargs.
     
        Parameters
        ----------
        s: string
            string with the content of the json data

        Returns:
        ----------
        d: dictionary
            dictionary with the content of the json data
    """

    import sys
    if sys.version_info[0] == 3:
        return simplejson.loads(s, **kwargs)

    else:
        if str is unicode and isinstance(s, bytes):
            s = s.decode('utf8')
    
    return simplejson.loads(s, **kwargs)

# -------------------------------------  dict2json  -------------------------------
# Description: Convert python dictionary to a json value
def dict2json(o, **kwargs ):
    """ Load object from JSON bytes (utf-8). See jsonapi.jsonmod.dumps for details on kwargs.
     
        Parameters
        ----------
        o: dictionary
            dictionary to convert
            

        Returns:
        ----------
        d: string
            string in json format

    """
        
    if 'separators' not in kwargs:
        kwargs['separators'] = (',', ':')
        
    s = simplejson.dumps(o, **kwargs)

    import sys
    if sys.version_info[0] == 3:
        if isinstance(s, str):
            s = s.encode('utf8')

    else:
        if isinstance(s, unicode):
            s = s.encode('utf8')
        
    return s


# -------------------------------------  read_json  -------------------------------
# Description: Read a json file
def read_json(json_file):
    """ Read a json file and return a string 
        
        Parameters
        ----------
        json file:string
            Path +  name + extension of the json file

        Returns:
        ----------
        json_data: string
            string with the content of the json data

    """
    json_data = open (json_file).read()
    return json_data

# -------------------------------------  getFiles  -------------------------------
# Description: Get list of files in some folder
def getFiles(path):
    """ Get a list of files that are inside a folder
        
        Parameters
        ----------
        path: string
            path of the folder

        Returns:
        ----------
        onlyfiles: list 
            list of strings with the name of the files in the folder

    """
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    print ("Available primitives:" +  str(onlyfiles))
    return onlyfiles


# ----------------------------- getRobotConfiguration -------------------------
# Description: Get configuration of a robot
def getRobotConfiguration(input_ = "pepper", options_ = ""):
    node_name = input_
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = getRIZEpath()
    
    print (path + "/robots/" + node_name + ".json")
    json_node = read_json(path + "/robots/" + node_name + ".json")
    dict_node = json2dict(json_node)
    print (json_node)
    return True, dict_node

# ----------------------------- getNodeConfiguration -------------------------
# Description: Get configuration of a robot
def getNodeConfiguration(input_ = "pepper", options_ = ""):
    node_name = input_
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = getRIZEpath()
    print (path + "/devices/" + node_name + ".json")
    json_node = read_json(path + "/devices/" + node_name + ".json")
    dict_node = json2dict(json_node)
    print (json_node)
    return True, dict_node

# ------------------------------------- onLoadRobots --------------------------
# Description: Get all robot configurations
def onLoadRobots(input_ = "", options_ = ""):
    lista = []
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = getRIZEpath()
    files = nep.getFiles(path + "/robots")
    for f in files:
        json_value = read_json(path + "/robots/" + f)
        dict_value = json2dict(json_value)
        lista.append(dict_value)
    dict_nodes = {"values":lista}
    return dict_nodes

# ------------------------------------- onSaveRobots ---------------------------
# Description: Save all robot configurations
def onSaveRobots(input_ = "", options_ = ""):
    
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = getRIZEpath()
    path_robots = path + "/robots"

    if not os.path.exists(path_robots):
        os.makedirs(path_robots)

    for f in input_:
        file_save = open(path_robots + "/" + f["name"] + ".json" , "w")
        file_save.write(simplejson.dumps(f, separators=(',', ':'), sort_keys=True,  indent=4))
        file_save.close()

    return {'state': "success"}



# ------------------------------------- onLoadRobots --------------------------
# Description: Get all robot configurations
def onLoadNode(input_ = "", options_ = ""):
    lista = []
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = getRIZEpath()
    files = nep.getFiles(path + "/devices")
    for f in files:
        json_value = read_json(path + "/devices/" + f)
        dict_value = json2dict(json_value)
        lista.append(dict_value)
    dict_nodes = {"values":lista}
    return dict_nodes

# ------------------------------------- onSaveRobots ---------------------------
# Description: Save all robot configurations
def onSaveNode(input_ = "", options_ = ""):
    
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = getRIZEpath()
    path_projects = path + "/devices"

    if not os.path.exists(path_projects):
        os.makedirs(path_projects)

    for f in input_:
        file_save = open(path_projects + "/" + f["name"] + ".json" , "w")
        file_save.write(simplejson.dumps(f, separators=(',', ':'), sort_keys=True,  indent=4))
        file_save.close()

    return {'state': "success"}

# ------------------------------------- onDeleteRobot --------------------------
# Description: Delete robot configuration
def onDeleteRobot(input_ = "", options_ = ""):

    original_path = os.getcwd()
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = getRIZEpath()
    
    try:
        path_file = path + "/robots"
        os.chdir(path_file)

        run_code = ""
        if os.environ.get('OS','') == 'Windows_NT':
            run_code = ("del " + str(input_) + ".json")
        else:
            run_code = ("rm " + str(input_) + ".json")
        print (subprocess.check_output(run_code,  shell=True))

        os.chdir(original_path)
    except:
        os.chdir(original_path)
        

    return {'state': "success"}

# ------------------------------------- onDeleteNode --------------------------
# Description: Get all robot configurations
def onDeleteNode(input_ = "", options_ = ""):

    original_path = os.getcwd()
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = getRIZEpath()
    
    try:
        path_file = path + "/devices"
        os.chdir(path_file)

        run_code = ""
        if os.environ.get('OS','') == 'Windows_NT':
            run_code = ("del " + str(input_) + ".json")
        else:
            run_code = ("rm " + str(input_) + ".json")
        print (subprocess.check_output(run_code,  shell=True))

        os.chdir(original_path)
    except:
        os.chdir(original_path)
        

    return {'state': "success"}


# ------------------------------------- onLoadSettings --------------------------
# Description: Get general rize configuration
def onLoadSettings(input_ = "", options_ = ""):
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = getRIZEpath()
    json_value = read_json(path + "/rize/configuration.json")
    dict_value = json2dict(json_value)
    return dict_value


# ------------------------------------- onSaveSettings ---------------------------
# Description: Save general rize configurations
def onSaveSettings(input_ = "", options_ = ""):
    if os.environ.get('OS','') == 'Windows_NT':
        path = "C:/RIZE"
    else:
        path = getRIZEpath()
    path_projects = path + "/rize"
    file_save = open(path_projects + "/configuration.json" , "w")
    file_save.write(simplejson.dumps(input_, separators=(',', ':'), sort_keys=True,  indent=4))
    file_save.close()

    return {'state': "success"}


# ------------------------------------ onSeeIP -----------------------------------
# Description: Get current IP value
def onSeeIP(input_ = "", options_ = ""):
    print ("IP request ...")
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    cw_ip = s.getsockname()[0]
    s.close()
    result = {'ip': str(cw_ip)}
    return result


