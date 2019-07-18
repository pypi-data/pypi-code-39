import re
import validators
from parserXBRL.taxonomia.instancia import XbrlIntancia


def getXbrlInstance(instanceName,
                    labelNameList, showLabels):
    xbrl_instancia = XbrlIntancia.Intancia()




    if not validators.url(instanceName):
        xi = xbrl_instancia.getInstanceByFile(instanceName,
                                              labelNameList, showLabels
                                              )
    else:
        xi = xbrl_instancia.getInstanceByUrl2(instanceName,
                                              labelNameList, showLabels
                                              )

                                          
    return xi


def getElementAtribute(xbrlInstance, element, refContext, show='all'):
    listSingleElemet = []
    if (len(xbrlInstance._elementList) > 0):
        for ele in xbrlInstance._elementList:
            if element == ele._name:

                if show == "all":
                    if (ele._xml_line):
                        print("Linea xml:      [" + str(ele._xml_line) + "]")
                    if ele._name:
                        print("Nombre:         [" + ele._name + "]")
                    if ele._value:
                        print("Valor:          [" + ele._value + "]")
                    if ele._unit_ref:
                        print("Unidad:         [" + ele._unit_ref + "]")
                    if ele._context_ref:
                        print("Contextp:       [" + ele._context_ref + "]")
                    if ele._id:
                        print("Id:             [" + ele._id + "]")
                    if ele._decimals:
                        print("Decimales:      [" + ele._decimals + "]")
                    print("Etiquetas del concepto{")
                    try:
                        if (ele._label):
                            for label in ele._label:
                                if label:
                                    if label._type:
                                        print("  ===== Tipo :        [" + label._type + "]")
                                    if label._value:
                                        print("  ===== Valor:        [" + label._value + "]")
                                    if label._lang:
                                        print("  ===== Lenguaje:     [" + label._lang + "]")
                                    if label._label:
                                        print("  ===== etiqueta/id:  [" + label._label + "]")
                                    if label._role:
                                        print("  ===== Rol:     [" + label._role + "]")
                                print("  ============================================")
                                print("  ")

                        else:
                            print("  ===== [No tiene etiquetas]")
                        print("} //Fin etiquetas")
                        print("  ===============================")
                    except ValueError:
                        print("  ===== [No tiene etiquetas]")
                else:
                    listSingleElemet.append(ele)
        if show == "all":
            return
        if show == "valor":
            if refContext <= len(listSingleElemet) and listSingleElemet[refContext]._value:
                print(listSingleElemet[refContext]._name + ": " + listSingleElemet[refContext]._value)
                return
            else:
                print("El valor no se encuentra")


def getElements(xbrlInstance,show="all"):
    if (len(xbrlInstance._elementList) > 0):
        for ele in xbrlInstance._elementList:
            if show == "all":
                if (ele._xml_line):
                    print("Linea xml:      [" + str(ele._xml_line) + "]")
                if ele._name:
                    print("Nombre:         [" + ele._name + "]")
                if ele._value:
                    print("Valor:          [" + ele._value + "]")
                if ele._unit_ref:
                    print("Unidad:         [" + ele._unit_ref + "]")
                if ele._context_ref:
                    print("Contextp:       [" + ele._context_ref + "]")
                if ele._id:
                    print("Id:             [" + ele._id + "]")
                if ele._decimals:
                    print("Decimales:      [" + ele._decimals + "]")
                print("Etiquetas del concepto{")
                try:
                    if (ele._label):
                        for label in ele._label:
                            if label:
                                if label._type:
                                    print("  ===== Tipo :        [" + label._type + "]")
                                if label._value:
                                    print("  ===== Valor:        [" + label._value + "]")
                                if label._lang:
                                    print("  ===== Lenguaje:     [" + label._lang + "]")
                                if label._label:
                                    print("  ===== etiqueta/id:  [" + label._label + "]")
                                if label._role:
                                    print("  ===== Rol:     [" + label._role + "]")
                                print("  ============================================")
                                print("  ")


                    else:
                        print("  ===== [No tiene etiquetas]")
                    print("} //Fin etiquetas")
                    print("  ===============================")
                except ValueError:
                    print("  ===== [No tiene etiquetas]")
            else:
                if ele._name and ele._value:
                    print(ele._name +":"+ ele._value)



def getDictAtributes(xbrlInstance, element):
    listSingleElemet = {}
    #
    # for elemento in element.keys():
       
    if (len(xbrlInstance._elementList) > 0):

        for ele in xbrlInstance._elementList:
            print(ele._name+":"+ele._value)
            if ele._name in element.keys():
                elemento = element.get(ele._name)
                if isinstance(elemento, dict):
                    print(elemento["value"] + "**: " + str(ele._value))
                    print(ele._context_ref)
                else:
                    print(element.get(ele._name) + "*: " + str(ele._value))
                listSingleElemet[ele._name] = ele._value
                del element[ele._name]

    return listSingleElemet   
    

def print_first_menu():
    print(30 * "-", "MENU", 30 * "-")
    print("1. Todos los valores")
    print("2. Un elemento")
    print("3. Desde url")
    print(67 * "-")
def print_menu():
    print(30 * "-", "MENU", 30 * "-")
    print("1. Trimestre Año Actual")
    print("2. Acumulado Año Actual")
    print("3. Trimestre Año Anterior")
    print("4. Acumulado Año Anterior")
    print(67 * "-")
