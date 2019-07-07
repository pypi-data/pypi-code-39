import os
import sys

# change path separator according to the os.
osPlatform = sys.platform
if osPlatform == 'win32':
    FPSLASH = '\\'
if osPlatform == 'linux1' or osPlatform == 'linux2':
    FPSLASH = '/'
    
cwd = os.getcwd()



# get all dir path in current directory,order by numbers ascend(assume index number in front of file name,and subsequent file name do not includes numbers)
def getDirList(path=cwd):
    dirList = []
    allDir = os.listdir(path)
    def getNum(val):
        baseName = os.path.basename(val)
        baseName = baseName.split('.')[0]
        result = ''
        for each in baseName:
            if each.isdigit():
                result = result + each
        if result=='':
            result=9999999
        return result
    allDir.sort(key=lambda f: int(getNum(f)))
    for each in allDir:
        each = path + FPSLASH + each
        if os.path.isdir(each):
            dirList.append(each)
    return dirList


# get all dir path in current directory,order by numbers ascend(assume index number in front of file name,and subsequent file name do not includes numbers)
def getFileList(path=cwd):
    fileList = []
    allDir = os.listdir(path)
    def getNum(val):
        baseName = os.path.basename(val)
        baseName = baseName.split('.')[0]
        result = ''
        for each in baseName:
            if each.isdigit():
                result = result + each
        if result=='':
            result=9999999
        return result
    allDir.sort(key=lambda f: int(getNum(f)))
    for each in allDir:
        each = path + FPSLASH + each
        if os.path.isfile(each):
            fileList.append(each)
    return fileList

