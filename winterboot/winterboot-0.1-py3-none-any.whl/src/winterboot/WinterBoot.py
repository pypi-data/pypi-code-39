from os.path import isfile, join, isdir
import importlib
import re
from posix import listdir

providers = {}

consumers = {}

def importAll(onlyfiles, package, pattern, nameConverter=lambda x: x):
    imported = []
    for file in onlyfiles:
        if re.match(pattern, file) and not file.startswith("_"):
            fullPath = package.__name__ + "." + nameConverter(file)
            imported.append(importlib.import_module(fullPath, package))
    return imported


def _autoload(package):
    mypath = package.__path__[0]
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    importAll(onlyfiles, package, ".*Service.py$", lambda x:x[:-3])
    onlydirs = [f for f in listdir(mypath) if isdir(join(mypath, f))]
    for loadedPackage in importAll(onlydirs, package, ".*"):
        _autoload(loadedPackage)

def autoload(package):
    _autoload(package)
    wire()

def wireOneService(serviceId, lazy=False):
    if serviceId not in consumers:
        return
    if serviceId not in providers:
        if not lazy:
            raise(AttributeError("no provider is registered as {0}".format(serviceId)))
        else:
            return
    provider = providers[serviceId][0]
    providers[serviceId][0] = provider
    for consumer in consumers[serviceId]:
        consumer.provider = provider

def wire():
    for serviceId in consumers:
        wireOneService(serviceId)

def addConsumer(moduleName, client):
    if moduleName not in consumers:
        consumers[moduleName] = []
    consumers[moduleName].append(client)

def addProvider(serviceId, klass):
    if serviceId not in providers:
        providers[serviceId] = []
    providers[serviceId].append(klass)
