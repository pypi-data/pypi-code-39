import re


from bs4 import BeautifulSoup
from parserXBRL.cargar_fichero import cargar
from parserXBRL.taxonomia.linkbase import Arc, Label, Locator
from parserXBRL.taxonomia.instancia import XbrlElement
from parserXBRL.utils import TaxonomiaRe
from parserXBRL.parse_xbrl_ifrs import XBRLParserIfrs, IFRS


class Intancia(object):
    def __init__(self, id=None, company=None, filename=None, elementList=None):
        if elementList is None:
            elementList = []
        self._id = id
        self._company = company
        self._filename = filename
        self._elementList = elementList
        self._contextList = []
    def __del__(self):
        pass


    def getInstanceByFile(self,
                          instanceName,
                          labelNameList, showLabels):

        loc = Locator.Locator()

        arc = Arc.Arc()
        label = Label.Label()
        xinstance = Intancia
        locatorList = []
        arcList = []
        labelList = []
        # xinstance._id = position
        xinstance._filename = instanceName
        flag = ""
        if showLabels:
            for labelName in labelNameList:
                locatorList.extend(loc.get_listLocatorFromFile(labelName))
                arcList.extend(arc.get_listArcFromFile(labelName, "labelArc"))
                labelList.extend(label.get_listLabelFromFile(labelName))
        else:
            pass
        file = cargar.get_file(instanceName)
        # file = cargar.get_fileByUrl(instanceName)
        # print(file)
        line = file.readline()
        xbrlElementList = []

        i = 1
        while line != "":
            e = XbrlElement.Element
            xre = TaxonomiaRe.XbrlRe()
            match = re.search(xre.get_elementRe(), line)
            if match:

                e._position = i

                e._xml_line = match.group()

                name = re.search(xre.get_elementName(), match.group())
                if name:
                    e._name = str.replace(name.group(), ":", "")
                else:
                    e._name = None

                decimals = re.search(xre.get_elementDecimals(), match.group())
                if decimals:
                    decimals = str.replace(decimals.group(), "\"", "")
                    decimals = str.replace(decimals, "\'", "")
                    e._decimals = str.replace(decimals, "decimals=", "")
                else:
                    e._decimals = None

                id = str.replace(match.group(), "-",
                                 "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a")
                id = re.search(xre.get_elementId(), id)
                if id:
                    id = str.replace(id.group(), "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a",
                                     "-")
                    id = str.replace(id, "\"", "")
                    id = str.replace(id, "\'", "")
                    e._id = str.replace(id, "id=", "").strip()
                else:
                    e._id = None

                cr = str.replace(match.group(), "-",
                                 "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a")
                cr = re.search(xre.get_elementContextRef(), cr)
                if cr:
                    cr = str.replace(cr.group(), "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a",
                                     "-")  # it replaces the improbable sequence by hyphen
                    cr = str.replace(cr, "\"", "")
                    cr = str.replace(cr, "\'", "")
                    e._context_ref = str.replace(cr, "contextRef=", "").strip()
                else:
                    e._context_ref = None

                ur = str.replace(match.group(), "-",
                                 "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a")
                ur = re.search(xre.get_elementUnitRef(), ur)
                if ur:
                    ur = str.replace(ur.group(), "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a",
                                     "-")  # it replaces the improbable sequence by hyphen
                    ur = str.replace(ur, "\"", "")
                    ur = str.replace(ur, "\'", "").strip()
                    e._unit_ref = str.replace(ur, "unitRef=", "").strip()
                else:
                    e._unit_ref = None

                value = str.replace(match.group(), ".",
                                    "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a")
                value = str.replace(value, ",",
                                    "a9a9a9a9a9z9z9z9z9za9a9a9a9a9z9z9z9z9z")
                value = re.search(xre.get_elementValue(), value)
                if value:
                    value = str.replace(value.group(), ">", "")
                    value = str.replace(value, "<", "")
                    value = str.replace(value, "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a", ".")
                    e._value = str.replace(value, "a9a9a9a9a9z9z9z9z9za9a9a9a9a9z9z9z9z9z", ",").strip() if len(
                        str.replace(value, "a9a9a9a9a9z9z9z9z9za9a9a9a9a9z9z9z9z9z", ",").strip()) > 0 else None
                    if (e._name == "EntityRegistrantName"):
                        flag = e._value
                else:
                    e._value = None

                newLabelList = []
                if (e._context_ref and showLabels):
                    newLabelList = label.get_labelsByLabelFromMemory(labelList, arc.get_arcByLocatorFromMemory(arcList,
                                                                                                               loc.get_locatorByElementFromMemory(
                                                                                                                   locatorList,
                                                                                                                   e)))
                else:
                    pass

                if e._context_ref:
                    xbrlElementList.append(
                        XbrlElement.Element(e._position, e._xml_line, e._name, e._decimals, e._id, e._context_ref,
                                            e._unit_ref, e._value,
                                            newLabelList))
                i += 1
            else:  # match:
                pass
            line = file.readline()
        file.close()
        xinstance._company = flag
        xinstance._elementList = xbrlElementList

        return xinstance
    def getInstanceByUrl(self,
                          instanceName,
                          labelNameList, showLabels):

        loc = Locator.Locator()

        arc = Arc.Arc()
        label = Label.Label()
        xinstance = Intancia
        locatorList = []
        arcList = []
        labelList = []
        # xinstance._id = position
        xinstance._filename = instanceName
        flag = ""
        if showLabels:
            for labelName in labelNameList:
                locatorList.extend(loc.get_listLocatorFromFile(labelName))
                print(locatorList)
                arcList.extend(arc.get_listArcFromFile(labelName, "labelArc"))
                print(arcList)
                labelList.extend(label.get_listLabelFromFile(labelName))
                print(labelList)
        else:
            pass
        
        file = cargar.get_file(instanceName)

        # file = cargar.get_fileByUrl(instanceName)
        # print(file)
        xbrlElementList = []

        soup = BeautifulSoup(file , 'lxml')
        
        ifrsParse = XBRLParserIfrs()
        # "ifrs_mx-cor_20141205:clavedecotizacionbloquedetexto",
        tagElementos = [ "ifrs-full:revenue"]
        elemento = ifrsParse.parseIFRS(soup, tagElementos)

       
        for e in elemento.elementos:
            print("--------------INICIO----------------")
            print(e._position)
            print(e._xml_line)
            # print(e._name )
            print(e._decimals )
            print(e._id)
            print(e._context_ref )
            print(e._unit_ref )
            print(e._value)
            # print(e._label)
            print("--------------FIN----------------")
       

        return xinstance
    def getInstanceByUrl2(self,instanceName,labelNameList,showLabels):
        loc = Locator.Locator()

        arc = Arc.Arc()
        label = Label.Label()
        xinstance = Intancia
        filestr = cargar.get_fileByUrl(instanceName)
        elements = filestr.split("\n")
        xbrlElementList = []
        xbrlContext = []

        arcList = []
        labelList = []
        locatorList = []
        if showLabels:
            for labelName in labelNameList:
                locatorList.extend(loc.get_listLocatorFromFile(labelName))
                arcList.extend(arc.get_listArcFromFile(labelName, "labelArc"))
                labelList.extend(label.get_listLabelFromFile(labelName))
        else:
            pass
        i = 1
        xinstance._filename = instanceName
        flag = ""
        for line in elements:
            e = XbrlElement.Element
            xre = TaxonomiaRe.XbrlRe()
            match = re.search(xre.get_elementRe(), line)
            if match:

                e._position = i

                e._xml_line = match.group()

                name = re.search(xre.get_elementName(), match.group())
                if name:
                    e._name = str.replace(name.group(), ":", "")
                else:
                    e._name = None

                decimals = re.search(xre.get_elementDecimals(), match.group())
                if decimals:
                    decimals = str.replace(decimals.group(), "\"", "")
                    decimals = str.replace(decimals, "\'", "")
                    e._decimals = str.replace(decimals, "decimals=", "")
                else:
                    e._decimals = None

                id = str.replace(match.group(), "-",
                                 "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a")
                id = re.search(xre.get_elementId(), id)
                if id:
                    id = str.replace(id.group(), "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a",
                                     "-")
                    id = str.replace(id, "\"", "")
                    id = str.replace(id, "\'", "")
                    e._id = str.replace(id, "id=", "").strip()
                else:
                    e._id = None

                cr = str.replace(match.group(), "-",
                                 "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a")
                cr = re.search(xre.get_elementContextRef(), cr)
                if cr:
                    cr = str.replace(cr.group(), "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a",
                                     "-")  # it replaces the improbable sequence by hyphen
                    cr = str.replace(cr, "\"", "")
                    cr = str.replace(cr, "\'", "")
                    e._context_ref = str.replace(cr, "contextRef=", "").strip()
                else:
                    e._context_ref = None

                ur = str.replace(match.group(), "-",
                                 "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a")
                ur = re.search(xre.get_elementUnitRef(), ur)
                if ur:
                    ur = str.replace(ur.group(), "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a",
                                     "-")  # it replaces the improbable sequence by hyphen
                    ur = str.replace(ur, "\"", "")
                    ur = str.replace(ur, "\'", "").strip()
                    e._unit_ref = str.replace(ur, "unitRef=", "").strip()
                else:
                    e._unit_ref = None

                value = str.replace(match.group(), ".",
                                    "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a")
                value = str.replace(value, ",",
                                    "a9a9a9a9a9z9z9z9z9za9a9a9a9a9z9z9z9z9z")
                value = re.search(xre.get_elementValue(), value)
                if value:
                    value = str.replace(value.group(), ">", "")
                    value = str.replace(value, "<", "")
                    value = str.replace(value, "z9z9z9z9z9a9a9a9a9az9z9z9z9z9a9a9a9a9a", ".")
                    e._value = str.replace(value, "a9a9a9a9a9z9z9z9z9za9a9a9a9a9z9z9z9z9z", ",").strip() if len(
                        str.replace(value, "a9a9a9a9a9z9z9z9z9za9a9a9a9a9z9z9z9z9z", ",").strip()) > 0 else None
                    if (e._name == "EntityRegistrantName"):
                        flag = e._value
                else:
                    e._value = None

                newLabelList = []
                if (e._context_ref and showLabels):
                    newLabelList = label.get_labelsByLabelFromMemory(labelList, arc.get_arcByLocatorFromMemory(arcList,
                                                                                                               loc.get_locatorByElementFromMemory(
                                                                                                                   locatorList,
                                                                                                                   e)))
                else:
                    pass

                if e._context_ref:
                    xbrlElementList.append(
                        XbrlElement.Element(e._position, e._xml_line, e._name, e._decimals, e._id, e._context_ref,
                                            e._unit_ref, e._value,
                                            newLabelList))
                else:
                    xbrlContext.append(e._xml_line)
                i += 1
            else:  # match:
                pass
        print("finish process url:")
        print(len(xbrlElementList))
        xinstance._company = flag
        xinstance._elementList = xbrlElementList
        xinstance._contextList = xbrlContext
        return xinstance