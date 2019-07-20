import re
import sys
import json
from .chatParser import WhatsAppChatParser
from .slideGenerator import SlideGenerator
from pptx.enum.shapes import MSO_SHAPE

class TextToPPTOrchestrator:
    def __init__(self):
        self.author = 'All'
        self.startDate = '01/01/00'
        self.endDate = '01/01/68'
        self.shapeType = 'round rectangle'
        self.fontSize = int(28)
        self.left = float(0.5)
        self.top = float(0.40)
        self.width = float(9.0)
        self.height = float(6.60)
        self.shapemap = {}
        self.shapemap['rectangle'] = MSO_SHAPE.RECTANGLE
        self.shapemap['round rectangle'] = MSO_SHAPE.ROUNDED_RECTANGLE
        self.shapemap['curved ribbon'] = MSO_SHAPE.CURVED_UP_RIBBON
    
    def SetMessageAuthor(self, author):
        self.author = author

    def SetStartDate(self,startDate):
        self.startDate = startDate

    def SetEndDate(self,endDate):
        self.endDate = endDate

    def SetFontSize(self, size ):
        self.fontSize = int(size)

    def SetShapeType(self, shapeType ):
        self.shapeType = shapeType

    def SetShapeLeft(self, left ):
        self.left = float(left)

    def SetShapeTop(self, top ):
        self.top = float(top)

    def SetShapeWidth(self, width ):
        self.width = float(width)

    def SetShapeHeight(self, height ):
        self.height = float(height)
  
    def ConvertTextFileToPPT( self, inputfile , outputfile ):
        chatparser = WhatsAppChatParser(inputfile)
        chatparser.SetMessageAuthor(self.author)
        chatparser.SetStartDate(self.startDate)
        chatparser.SetEndDate(self.endDate)
        chatparser.ExtractQuoteList(inputfile)
        generator = SlideGenerator(outputfile)
        generator.SetFontSize(self.fontSize)
        generator.SetShapeType(self.shapeType)
        generator.SetShapeLeft(self.left)
        generator.SetShapeTop(self.top)
        generator.SetShapeWidth(self.width)
        generator.SetShapeHeight(self.height)
    
        while True:
            try:
               generator.addSlide(chatparser.getNextQuote())
            except:
               break
        generator.save()  
