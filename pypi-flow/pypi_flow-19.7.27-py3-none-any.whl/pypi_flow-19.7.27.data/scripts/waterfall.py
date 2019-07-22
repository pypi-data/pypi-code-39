import datetime
import grtoolkit as grt
from grtoolkit.Python import packageDir

#COLLECT PROJECT INPUT FROM USER
print("Welcome to the pypi_flow project creator!\nA project will be created in this directory based on the following information:\n")
packageName = input("package name: ")
author = input("author: ")
description = input("project description: ")
email = input("contact email: ")
url = input("project website: ")
year = datetime.datetime.now().year

projectFolder = grt.cwd()
templateSource = packageDir("pypi_flow") + "\\packageTemplate"

print(projectFolder)