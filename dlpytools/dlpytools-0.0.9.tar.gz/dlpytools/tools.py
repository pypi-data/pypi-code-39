import os
import sys
import sqlite3
from win32.win32crypt import CryptUnprotectData

osPlatform = sys.platform
if osPlatform == 'win32':
    FPSLASH = '\\'
if osPlatform == 'linux1' or osPlatform == 'linux2' or osPlatform == 'linux':
    FPSLASH = '/'


def getAFiles(cwd='.',fileList=[]):
  allPath = os.listdir(cwd)
  dirs = []
  for each in allPath:
    path = cwd + FPSLASH + each
    if os.path.isdir(path):
      dirs.append(path)
    if os.path.isfile(path):
      fileList.append(path)
  for each in dirs:
    getAFiles(each,fileList)
  return fileList

def getADirs(cwd='.',dirList=[]):  
  allPath = os.listdir(cwd)
  dirs = []
  for each in allPath:
    path = cwd + FPSLASH + each
    if os.path.isdir(path):
      dirs.append(path)
      dirList.append(path)
  for each in dirs:
    getADirs(each,dirList)
  return dirList

def getCFiles(cwd='.'):
  allPath = os.listdir(cwd)
  files = []
  for each in allPath:
    path = cwd + FPSLASH + each
    if os.path.isfile(path):
      files.append(path)
  return files

def getCDirs(cwd='.'):
  allPath = os.listdir(cwd)
  dirs = []
  for each in allPath:
    path = cwd + FPSLASH + each
    if os.path.isdir(path):
      dirs.append(path)
  return dirs

def getcookiefromchrome(host='.oschina.net'):
    cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
    sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu=conn.cursor()        
        cookies={name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
        return cookies
# ========================================================================
def getIndexListFromFindFunc(string,key,start=0,indexList=[]):
  index = string.find(key,start)
  start = index + 1
  if index != -1:
    indexList.append(index)
    getIndexListFromFindFunc(string,key,start,indexList)
  return indexList

def convertUnicodeStringToString(string):
  indexList = getIndexListFromFindFunc(string,'\\u')
  unicodeDict = {}
  for i in indexList:
    uni = string[i+1:i+6]
    unicodeDict[uni] = chr(int(uni[1:],16))
  for key in dict.keys(unicodeDict):
    string = string.replace('\\'+key,unicodeDict[key])
  return string


