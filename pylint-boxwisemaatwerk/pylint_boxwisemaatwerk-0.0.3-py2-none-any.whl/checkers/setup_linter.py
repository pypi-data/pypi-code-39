import os
import time


files_to_search = ['C:\Program Files (x86)']
hint_file = ['C:\Program Files (x86)\TranCon\BOXwisePro\Server']

def get_path():
        pylintrc_setting = 'trancon-installation-folder='
        pylintrc_location = 'C:\\dev\\.pylintrc'
        begin = time.time()
        fileHandle = open ( pylintrc_location,"r" )
        lineList = fileHandle.readlines()
        if pylintrc_setting in lineList[-1]:
            #setup already exists so we can just read the path from this file
            trancon_path =  lineList[-1].replace(pylintrc_setting,"")
            fileHandle.close()
        else:
            fileHandle.close()
            #setting doesn't exists so first search for the tranconpath only in programfiles for now
            found = False
            #check common installation folders
            for common_place in hint_file:
                if os.path.exists(common_place):
                    found = True
                    trancon_path = common_place
                    break

            #if the path still hasn't been found walk through all program files to see if its deeper
            if not found:
                for search_dir in files_to_search:
                    current_dir = os.getcwd()
                    os.chdir(search_dir)
                    found = False
                    for root, dirs, files in os.walk(search_dir):
                        if root.endswith("\TranCon\BOXwisePro\Server"):
                            #boxwise is installed
                            trancon_path = root
                            found = True
                            break
                    if found:
                       break
                #out of the files to search forloop
                os.chdir(current_dir)
                if not found:
                    #TODO: sometype of error message that boxwise isn't installed
                    return 'not found'
            fileHandle = open(pylintrc_location, 'a')
            fileHandle.write('\n \n' + pylintrc_setting + trancon_path)
            fileHandle.close()
        end = time.time()
        print end-begin
        return trancon_path