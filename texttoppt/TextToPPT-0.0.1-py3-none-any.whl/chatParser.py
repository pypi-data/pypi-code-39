import re
import sys
import json


class WhatsAppChatParser:
    def __init__(self, chatExportFile ):
        self.quoteList = []
        self.ignoredList = []
        self.quoteIndex = 0
        self.deletedPattern()
        self.author = 'All'
       
    def SetMessageAuthor(self, author):
        self.author = author


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


    def ExtractQuoteList(self, chatExportFile ):
        fileHandler = open (chatExportFile, "r", encoding="utf8")
        timeStamp = re.compile(".*\s*\[.*\]")
        if ( self.author == 'All' ):
            messageStartPattern = re.compile(".*\s*\[.*\] .*: ")
        else:
            messageStartPattern = re.compile(".*\s*\[.*\] "+self.author+": ")
        message = ""
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
                if ( insideMessage) :
                    self.quoteList.append(message)
                    insideMessage = False

                if ( m ):
                    message = line[len(m.group()):]
                    insideMessage = True
            else :
                if ( insideMessage ):
                    message = message + line



        # Close Close
        fileHandler.close()
        if ( insideMessage ):
            self.quoteList.append(message)

 
    def getNextQuote(self):
        if ( self.quoteIndex >= len(self.quoteList)):
            raise
        message = self.quoteList[self.quoteIndex]
        self.quoteIndex += 1
        return ( message )
