import xml.etree.ElementTree as ET
from parserXBRL.utils import ns


class Arc(object):
    def __init__(self, _concept=None, _role=None, _order=None, _from=None, _to=None):
        self._concept = _concept
        self._type = "arc"
        self._role = _role
        self._order = _order
        self._from = _from
        self._to = _to
        self.weight = None
        self.priority = None
        self.use = None

    def __del__(self):
        pass

    def get_listArcFromFile(self, file, concept):
        root = ET.parse(file).getroot()
        listArc = []
        for arc in root.iter(ns.get_ns('link') + 'labelArc'):
            newarc = Arc()
            newarc._concept = concept
            if hasattr(arc.attrib, 'order'):
                newarc._order = arc.attrib['order']
            if arc.attrib[ns.get_ns('xlink') + 'arcrole']:
                newarc._role = arc.attrib[ns.get_ns('xlink') + 'arcrole']
            else:
                newarc._role = arc.attrib[ns.get_ns('xlink') + 'role']
            newarc._from = arc.attrib[ns.get_ns('xlink') + 'from']
            newarc._to = arc.attrib[ns.get_ns('xlink') + 'to']
            listArc.append(newarc)
        return listArc

    def get_arcByLocatorFromMemory(self, listArc, loc):
        newlistArc = []
        for arc in listArc:
            if arc._from == loc._label:
                newlistArc.append(arc)
            else:
                pass
        return newlistArc
