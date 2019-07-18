import os
import sys

osPlatform = sys.platform
if osPlatform == 'win32':
    FPSLASH = '\\'
if osPlatform == 'linux1' or osPlatform == 'linux2' or osPlatform == 'linux':
    FPSLASH = '/'


def getAFiles(cwd='.',fileList=[]):
  print(cwd)
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
  print(cwd)  
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
