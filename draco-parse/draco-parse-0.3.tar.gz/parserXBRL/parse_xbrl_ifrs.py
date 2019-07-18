

import re
from parserXBRL.taxonomia.instancia import XbrlElement

class XBRLParserIfrs(object):

    def __init__(self, precision=0):
        self.precision = precision

    @classmethod
    def parse(self, fileSoup):
        """
        parse is the main entry point for an XBRLParser. It takes a file
        handle.
        """

        xbrl_obj = XBRL()

        

        xbrl = fileSoup
        # file_handler.close()
        xbrl_base = xbrl.find(name=re.compile("xbrl*:*"))

        if xbrl.find('xbrl') is None and xbrl_base is None:
            raise Exception('The xbrl file is empty!')

        # lookahead to see if we need a custom leading element
        lookahead = xbrl.find(name=re.compile("context",
                              re.IGNORECASE | re.MULTILINE)).name
        if ":" in lookahead:
            self.xbrl_base = lookahead.split(":")[0] + ":"
        else:
            self.xbrl_base = ""

        return xbrl

    

    @classmethod
    def parseIFRS(self,
                  xbrl, tagElement=[]):
        """
        Parse GAAP from our XBRL soup and return a GAAP object.
        """
        ifrs_obj = IFRS()
        # print( tagElement)
        length = len(tagElement)
        for e in range(length):
          


            tag = tagElement[e]
            
            
            tag_revenues = xbrl.find_all(tag)
            
           
            listRevenue = []
            i = 0
            # print(tag_revenues[0].find_all(attrs={"decimals"}))
            while i < len(tag_revenues):
                elementSoup = tag_revenues[i]
                elemento = XbrlElement.Element()
                elemento._position = i
                elemento._xml_line = tag_revenues[i]
                attrs = tag_revenues[i].attrs
                # print(attrs)

                # for key in attrs:
                #     if key == 'decimals':
                #         print('tiene decimals')
                elemento._decimals = attrs['decimals']
                    # else:
                    #     print('no tiene decimals')
                    #     elemento._decimals = None

                    # if key == 'id':
                    #     print('tiene id')
                elemento._id = attrs['id']
                    # else:
                    #     print('no tiene id')
                    #     elemento._id = None

                    # if key == 'contextref':
                    #     print('tiene contextref')
                elemento._contextref = attrs['contextref']
                    # else:
                    #     print('no tiene contextref')
                    #     elemento._contextref = None

                    # if key == 'unitref':
                    #     print('tiene unitref')
                elemento._unitref = attrs['unitref']
                    # else:
                    #     print('no tiene unitref')
                    #     elemento._unitref = None

                # for key in attrs:
                #     if key == 'id':
                #         print('tiene id')
                #         elemento._id = attrs['id']
                #     else:
                #         print('no tiene id')
                #         elemento._id = None
            
                # for key in attrs:
                #     if key == 'contextref':
                #         print('tiene contextref')
                #         elemento._contextref = attrs['contextref']
                #     else:
                #         print('no tiene contextref')
                #         elemento._contextref = None

                # for key in attrs:
                #     if key == 'unitref':
                #         print('tiene unitref')
                #         elemento._unitref = attrs['unitref']
                #     else:
                #         print('no tiene unitref')
                #         elemento._unitref = None

                if elementSoup.text:
                    elemento._value = elementSoup.text
                else:
                    elemento._value = None

                listRevenue.append(elemento)
                i += 1
        
        
            ifrs_obj.elementos.extend(listRevenue)
        
        return ifrs_obj

    

    
   



class XBRL(object):
    def __str__(self):
        return ""



class IFRS(object):
    def __init__(self,elementos=[]):
        self.elementos = elementos
        


# class IFRSSerializer(Schema):
    
    # revenue = fields.Number()
    


# Base Custom object
class Custom(object):

    def __init__(self):
        return None

    def __call__(self):
        return self.__dict__.items()
