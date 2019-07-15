# universal.py

"""
universal.py: This module is used for Developmental Engineering purposes.
"""

import os
import sys
import json
import requests
import subprocess

headers = {'Content-type':'application/json'}

# USE IN OTHER PROGRAMS TO DOWNLOAD MODULE
def downloadfile(this_file, url):
    proc_output = subprocess.Popen(["wget", "-o", "/dev/null", "-O", this_file, url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc_output.communicate()

    return out, err

# USE IN OTHER PROGRAMS TO INSTALL MODULE
# module_name = module_file_name
# log_update = subprocess.Popen(["sudo", "pip", "install", module_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# status, err = log_update.communicate()

def print_user_input(this_input):
    return (u'You\'re input is "'
            u'{}"').format(this_input)

def get_env_creds(argument):
    switch = {
        "Test" : {"env_url" : "",
                 "key" : "",
                 "secret" : "",
                    },
        "Dev" : {"env_url" : "",
                "key" : "",
                "secret" : "",
                    },
        "Prod" : {"env_url" : "",
                "key" : "",
                "secret" : "",
                    },
    }
    data = switch.get(argument, "ERROR: Invalid Environment!")

    env_url = data['env_url']
    key = data['key']
    secret = data['secret']

    return env_url, key, secret

values = get_env_creds('Test')
env_url = values[0]
key = values[1]
secret = values[2]

class UrlRequest:
    def __init__(self, url, key, secret):
        self.url = url
        self.key = key
        self.secret = secret

        response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
        binary = response.content
        output = json.loads(binary)
        json_string = json.dumps(output, indent=4)

        self.response = response
        self.output = output
        self.json_string = json_string

# env_request = UrlRequest(env_url, key, secret)
# print(env_request.output)
# print(env_request.json_string)

# class file_exist:
#     def __init__(self, this_file):
#         status = os.path.exists(this_file)
#         if(status == True):
#             if(os.path.isdir(this_file)):
#                 file_type = 'directory'
#                 # print(file_type)
#             elif(os.path.isfile(this_file)):  
#                 file_type = 'file'
#                 # print(file_type)
#             else:
#                 print("It is a special file (socket, FIFO, device file, etc.)" )
#             status = 'exist'
#         else:
#             file_type = status
#             status = status

#         self.file_type = file_type
#         self.status = status

# binary_file_results = file_exist(terraform_binary_path)
# state_file_results = file_exist(terraform_state_file_path)

# if(state_file_results.file_type == 'file' and state_file_results.status == 'exist'):
#     os.remove(terraform_state_file_path)

# if(binary_file_results.file_type == 'file' and binary_file_results.status == 'exist'):
#     # print(binary_file_results.file_type)
#     # print(binary_file_results.status)

#     projects_url = ""
#     projects_request = UrlRequest(projects_url, key, secret)

#     # print(projects_request.json_string)
#     output = projects_request.output

#     for counter in range(len(output['data'])):
#         # print(counter)
#         env_name = output['data'][counter]['name']
#         env_id = output['data'][counter]['id']
#         print("ENV Name: " + env_name + " / " + "ENV ID: " + env_id)
#         print("")
#             # if(output['data'][counter]['name']) == instance_name:
#             #     env_id = output['data'][counter]['id']

# Get everything after last character occurrence
def lasttrim(character, trim_this):
    """Get all contents after specified character\n
    ex: lasttrim('.', string)
    """
    trimmed = trim_this[trim_this.rindex(character)+1:]

    return trimmed

def filestatus(this_file):
    """Check if file exists, and get the file type"""
    status = os.path.exists(this_file)
    if(status == True):
        if(os.path.isdir(this_file)):
            filetype = 'directory'
            # print(filetype)
        elif(os.path.isfile(this_file)):  
            filetype = 'file'
            # print(filetype)
        else:
            print("It is a special file (socket, FIFO, device file, etc.)" )
        status = 'exist'
    else:
        filetype = status
        status = status
    
    return {'filetype': filetype, 'status': status}

def removeprefix(text, prefix):
    """Remove a prefix from a string"""
    if text.startswith(prefix):
        text = text[len(prefix):] # Removing prefix.
        text = text.lstrip() # Removing leading white space.
        return text
    return text

def getoriginalfilecontent(file):
    """Get entire file contents in original/list format"""
    with open(file) as f:
        file_in_list_format = f.readlines()

    return file_in_list_format

def getfilecontent(file):
    """Get entire file contents"""
    with open(file) as f:
        file_in_list_format = f.readlines()
        file_in_list_to_string_format = ''
        for line in file_in_list_format:
            file_in_list_to_string_format += line

    return file_in_list_to_string_format

def getoriginalfilecontentnoprefix(file, prefix):
    """Get entire file contents in original/list format\n
    In Development!
    """
    with open(file) as f:
        file_in_list_format = f.readlines()
        file_in_list_format_no_prefix = []
        for line in file_in_list_format:
            # print(line)
            # line = removeprefix(line[0], prefix)
            file_in_list_format_no_prefix += line

        # print(file_in_list_format_no_prefix)
    return file_in_list_format_no_prefix

def getfilecontentnoprefix(file, prefix):
    """Get entire file contents"""
    with open(file) as f:
        file_in_list_format = f.readlines()
        file_in_list_to_string_format_no_prefix = ''
        for line in file_in_list_format:
            line = removeprefix(line, prefix)
            file_in_list_to_string_format_no_prefix += line

    return file_in_list_to_string_format_no_prefix

def getfileline(file, linenumber):
    """Get specific line from file"""
    with open(file) as f:
        whole_file = f.readlines()
        line = (whole_file[linenumber])

    return line

def txt2dslist(file):
    """Convert txt file to datastructure in list format"""
    content = getoriginalfilecontent(file)
    data = []
    for line in content:
        row = line.split()
        data.append(row)

    return data
        
def txt2dslistnoprefix(file, prefix):
    """Convert txt file to datastructure in list format & remove prefix"""
    content = getoriginalfilecontent(file)
    data = []
    for line in content:
        line = removeprefix(line, prefix)
        row = line.split()
        data.append(row)

    return data

def removeEmptyElementsFromList(this_list):
    """Remove empty elements from lists\n
    ex: []"""
    clean_list = [x for x in this_list if x]
    
    return clean_list

def getduplicateElementsFromList(this_list):
    """Get duplicate elements from lists"""
    duplicates_from_list = set([x for x in this_list if this_list.count(x) > 1])
    
    return duplicates_from_list