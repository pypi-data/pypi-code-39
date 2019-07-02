import xml.etree.ElementTree as ET
from parserXBRL.utils import ns


class Label:
    def __init__(self, _label=None, _lang=None, _role=None, _id=None, _value=None):
        self._type = "resource"
        self._label = _label
        self._lang = _lang
        self._role = _role
        self._id = _id
        self._value = _value

    def __del__(self):
        pass

    def __str__(self):
        return self._value

    def get_listLabelFromFile(self, file):
        root = ET.parse(file).getroot()
        listLabel = []
        for label in root.iter(ns.get_ns('link') + 'label'):
            newlabel = Label()
            newlabel._label = label.attrib[ns.get_ns('xlink') + 'label']
            newlabel._lang = label.attrib[ns.get_ns('xml') + 'lang']
            newlabel._role = label.attrib[ns.get_ns('xlink') + 'role']
            newlabel._value = label.text
            listLabel.append(newlabel)
        return listLabel

    def get_labelsByLabelFromMemory(self, listLabel, listArc):
        newlistlabel = []
        for arc in listArc:
            for label in listLabel:
                if label._label == arc._to:
                    newlistlabel.append(label)
                else:
                    pass
        return newlistlabel
