import os

def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles


all_files = getListOfFiles('/Users/Mukeshkhare/Desktop/apple-season')

i = 0
while i < len(all_files):
    if '.html' not in all_files[i] and '.py' not in all_files[i] and '.css' not in all_files[i] or '.pyc' in all_files[i]:
        all_files.remove(all_files[i])
    else:
        i += 1

i = 0
while i < len(all_files):
    if 'venv' in all_files[i]:
        all_files.remove(all_files[i])
    else:
        i += 1

lines = 0
for file in all_files:
    with open(file, 'r') as f:
        lines += len(f.read().split('\n'))

print(lines)
