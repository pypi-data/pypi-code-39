import xml.etree.ElementTree as ET
from parserXBRL.utils import ns


class Locator(object):
    def __init__(self, _href=None, _label=None):
        self._type = "locator"
        self._href = _href
        self._label = _label

    def __del__(self):
        pass

    def get_listLocatorFromFile(self, file):
        root = ET.parse(file).getroot()
        listLocator = []
        for locator in root.iter(ns.get_ns('link') + 'loc'):
            loc = Locator()
            loc._href = locator.attrib[ns.get_ns('xlink') + 'href']
            loc._label = locator.attrib[ns.get_ns('xlink') + 'label']
            listLocator.append(loc)
        return listLocator

    def get_locatorByElementFromMemory(self, listLocator, ele):
        for loc in listLocator:
            if "_" + ele._name in loc._href:
                return loc
            else:
                pass
