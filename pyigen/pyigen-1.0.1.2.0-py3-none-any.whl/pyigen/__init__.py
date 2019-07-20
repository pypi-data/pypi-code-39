import time
import pkg_resources
import os

name = "pyigen"
version='1.0.1.2'
creation_date='July 19, 2019'

#pyigen.run() variables:
    #for no icon, make icon=None
    #console: True if u want console, False if u don't want console
    #pygameusage: if u want pygame, make True, False, if u don't want quit

slash=' \ '
sep=os.pathsep.replace("'","")

def run(appname,filename,pygameusage,console,icon):
    
    print()

    print("Copy and Paste the code and run it in")
    print("the Terminal or your Command Prompt")
    print("in the same directory as",filename)
    print()

    print("Note: if you need to add files in your program, \
add '--add-data filename{}filename_again' to the code.".format(sep))

    print()


    print("pyinstaller --onefile",end=' ')
    if console==False:
        print("-w", end=' ')
    if icon !=None:
        print("-i",icon, end=' ')

    if pygameusage==True:
        print("--hiddenimport pygame", end=' ')
    print(filename, end=' ')

    print('\n')
        

def pyigen_license():
    lf=pkg_resources.resource_filename('pyigen','files/LICENSE-for-function.txt')
    with open(lf) as l: # The with keyword automatically closes the file when you are done
        print (l.read())

def manual():
    lfa=pkg_resources.resource_filename('pyigen','files/manual.txt')
    with open(lfa) as m: # The with keyword automatically closes the file when you are done
        print (m.read())

def about():
    print("About pyigen {}".format(version))
    print()
    print("Created by Armaan Aggarwal on {}".format(creation_date))

print("pyigen {} successfully imported".format(version))
print("To see the manual of pyigen {}, use the command 'pyigen.manual()'".format(version))

