import re
import sys
import json
import datetime
from datetime import datetime
from datetime import timedelta, date


class WhatsAppChatParser:
    def __init__(self, chatExportFile ):
        self.quoteList = []
        self.timeList = []
        self.ignoredList = []
        self.quoteIndex = 0
        self.deletedPattern()
        self.author = 'All'
        self.startDate = '01/01/00'
        self.endDate = '01/01/68'
       
    def SetMessageAuthor(self, author):
        self.author = author

    def SetStartDate(self,startDate):
        self.startDate = startDate

    def SetEndDate(self,endDate):
        self.endDate = endDate

    def deletedPattern(self):
        messageYouDeletedMsgPattern = "^\s*\[.*\] .*: You deleted this message."
        messageOtherDeletedMsgPattern = "^\s*\[.*\] .*: This message was deleted."
        messageWebsiteLinkPattern = "^\s*\[.*\] .*: [.*https://.*|.*www..*|.*.com.*]"
        self.ignoredList.append(messageYouDeletedMsgPattern)
        self.ignoredList.append(messageOtherDeletedMsgPattern)
        self.ignoredList.append(messageWebsiteLinkPattern)
        #return(self.ignoredList)


    def shouldThisBeIgnored(self, line ):

        gotMatch = False
        for regex in self.ignoredList:
            s = re.search(regex,line)
            if( s ):
                gotMatch = True
                break
        if gotMatch:
            return (True)
        return (False)

    def dateFilter(self,line):   
        Dpattern = re.compile(r"\d\d\/\d\d\/\d\d")
        m = Dpattern.findall(line)
        liveDate =  m[0]
        liveDateDays = (datetime.strptime(liveDate,"%d/%m/%y")-datetime(1970,1,1)).days
        endDate = self.endDate
        startDate = self.startDate
        startDateDays = (datetime.strptime(startDate,"%d/%m/%y")-datetime(1970,1,1)).days
        endDateDays = (datetime.strptime(endDate,"%d/%m/%y")-datetime(1970,1,1)).days
        if(liveDateDays >= startDateDays and liveDateDays <= endDateDays):
            return True
        else:
            return False

    def ExtractQuoteList(self, chatExportFile ):
        fileHandler = open (chatExportFile, "r", encoding="utf8")
        timeStamp = re.compile(".*\s*\[.*\]")
        if ( self.author == 'All' ):
            messageStartPattern = re.compile(".*\s*\[.*\] .*: ")
        else:
            messageStartPattern = re.compile(".*\s*\[.*\] "+self.author+": ")
        message = ""
        time = ""
        insideMessage = False


        while True:
            # Get next line from file
            line = fileHandler.readline()

            #senderName = re.search('"^\s*\[.*\] (.*):', line)
            #snd = senderName.group(1)
            # If line is empty then end of file reached
            if not line :
                break;

            if ( self.shouldThisBeIgnored(line) ):
                continue

            m = messageStartPattern.match(line)
            t = timeStamp.match(line)

            if ( t ) :
               if self.dateFilter(line) == True:
                    if ( insideMessage) :
                        self.quoteList.append(message)
                        self.timeList.append(time)
                        insideMessage = False

                    if ( m ):
                        message = line[len(m.group()):]
                        time = line[len(t.group()):]
                        insideMessage = True
            else :
                if ( insideMessage ):
                    message = message + line



        # Close Close
        fileHandler.close()
        if ( insideMessage ):
            self.quoteList.append(message)
            self.timeList.append(time)

 
    def getNextQuote(self):
        if ( self.quoteIndex >= len(self.quoteList)):
            raise
        message = self.quoteList[self.quoteIndex]
        time = self.quoteList[self.quoteIndex]
        self.quoteIndex += 1
        return ( message )
        return ( time )
