import datetime, sys, os, shutil, re
import grtoolkit as grt
from grtoolkit.Python import packageDir

def delDotPrefix(string):
    '''Delete dot prefix to file extension if present'''
    return string[1:] if string.find(".") == 0 else string

def filesInFolder(folder, fileType="*"):  # Returns list of files of specified file type
    fileType = delDotPrefix(fileType)
    file_regex = re.compile(rf".*\.{fileType}", re.IGNORECASE)  # Regular Expression; dot star means find everything
    file_list = []
    for dirpath, _, filenames in os.walk(folder,):  # for each folder
        for file in filenames:
            file_search = file_regex.findall(file)
            if file_search:  # if file_search is not empty
                file_list.append(dirpath + '\\' + file)
    return file_list

print("\nWelcome to the pypi_flow project creator!\nA project will be created in this directory based on the following information:\n")

try:
    projectFolder = sys.argv[1]
    templateSource = packageDir("pypi_flow") + "\\packageTemplate"
    # print(projectFolder)
except IndexError:
    print(r'''
    Error: Python did not receive a directory argument upon being called.
    Try adding %* to the end of the Registry Key [HKEY_CLASSES_ROOT\Applications\python.exe\shell\open\command]\n
    ''')
    exit()

#COLLECT PROJECT INPUT FROM USER
packageName = input("package name: ")
author = input("author: ")
description = input("project description: ")
email = input("contact email: ")
url = input("project website: ")
year = str(datetime.datetime.now().year)

#REPLACEMENT WORDS DICTIONARY
projectDictionary = {
    "$package-name$":packageName,
    "$author$":author,
    "$description$":description,
    "$email$":email,
    "$url$":url,
    "$year$":year,
}

#COPY FILES
packageRoot = projectFolder + f"\\{packageName}"
packageFolder = packageRoot + f"\\{packageName}"
os.makedirs(packageRoot)
os.makedirs(packageFolder)
shutil.copyfile(templateSource + '\\PypiUpload.py', packageRoot + '\\PypiUpload.py')
shutil.copyfile(templateSource + '\\setup.py', packageRoot + '\\setup.py')
shutil.copyfile(templateSource + '\\__init__.py', packageRoot + '\\__init__.py')
shutil.copyfile(templateSource + '\\package_name\\__init__.py', packageFolder + '\\__init__.py')
#MISSING COPYING LICENSE

filelist = filesInFolder(packageRoot)

for file in filelist:
    tempfile = grt.Storage.File(file)
    content = tempfile.read()
    content = grt.File.replaceWords(content, projectDictionary)
    tempfile.write(content)
    