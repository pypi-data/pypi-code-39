#! /usr/bin/env python
import os
import logging
import io
from os import listdir
from os.path import isfile, join
import random
import string
import argparse
import re
import sys
from datetime import datetime
from time import gmtime, strftime
from io import StringIO



if sys.version_info[0] < 3:  ##to check python version and modify for the code to run in python2 versions
    from io import open

    reload(sys)
    sys.setdefaultencoding('utf8')


def read_in_chunks(file_object,chunk_size=2000):  # reads the file in chunks of default 2000 bytes this can be specified by users
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def timeStampVaalidator(word):
    new_word = word.strip()
    obj = re.match("^([0-9]{2,4})\/([0-1][0-9])\/([0-3][0-9])(?:( [0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$", new_word,
                   re.M | re.I)
    obj1 = re.match("^([0-9]{2,4})-([0-1][0-9])-([0-3][0-9])(?:( [0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$", new_word,
                    re.M | re.I)
    obj2 = re.match("^([0-3][0-9])-([0-1][0-9])-([0-9]{2,4})(?:( [0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$", new_word,
                    re.M | re.I)
    obj3 = re.match("^([0-3][0-9])\/([0-1][0-9])\/([0-9]{2,4})(?:( [0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$", new_word,
                    re.M | re.I)
    obj4 = re.match("^([0-3][0-9])\.([0-1][0-9])\.([0-9]{2,4})(?:( [0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$", new_word,
                    re.M | re.I)
    obj5 = re.match("^([0-9]{2,4})\.([0-1][0-9])\.([0-3][0-9])(?:([0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$", new_word,
                    re.M | re.I)
    obj6 = re.match("(([0-9]{2,4})-([0-1][0-9]|[0-9])-[0-3][0-9]T)(?:([0-2][0-9]):([0-5][0-9]):([0-5][0-9]))?$",
                    new_word, re.M | re.I)

    if obj:
        time = strftime("%Y/%m/%d %H:%M:%S", gmtime()).split(' ')
        return True, time[0]
    elif obj1:
        time = (str(datetime.now()).split(' '))
        return True, time[0]
    elif obj2:
        time = strftime("%d-%m-%Y %H:%M:%S", gmtime()).split(' ')
        return True, time[0]
    elif obj3:
        time = strftime("%d/%m/%Y %H:%M:%S", gmtime()).split(' ')
        return True, time[0]

    elif obj4:
        time = strftime("%d.%m.%Y %H:%M:%S", gmtime()).split(' ')
        return True, time[0]
    elif obj5:
        time = datetime.today().isoformat()
        return True, time
    elif obj6:
        time = datetime.today().isoformat()
        return True, time

    else:
        return False, word


def maskGenerator(word, flag=False, isJson = False):  # iterates through word letter by letter and replaces the same by random character
    c = ""
    r, f = timeStampVaalidator(word)
    if r:  # checking if it is a time stamp
        return f
    else:  # if not iterating through each element and masking it
        i = 0

        if "[CDATA" in word:
              word = word.replace("[CDATA", "***")


        while (i < len(word)):
            if word[i].isdigit():
                c += str(random.randint(1, 9))
            elif word[i].isupper():
                c += random.choice(string.ascii_letters).upper()
            elif word[i].isspace():
                c = c + word[i]
            elif word[i].islower():
                if isJson and word[i:i+4]=='true':
                    i+=3 #below is other +1
                    c+='true'
                elif isJson and word[i:i+5]=='false':
                    i+=4 #below is other +1
                    c+='false'
                else:
                    c += random.choice(string.ascii_letters).lower()
            else:
                if flag == True:
                    if word[i] == "&":
                        while word[i] != ";":
                            c += word[i]
                            i += 1
                        c = c + ';'
                    else:
                        c += word[i]
                else:
                    c += word[i]
            i += 1

        c = c.replace("***", "[CDATA")
        return c


def xmlTagMask(s):  # masks the xml attributes
    # exception for the xml header tag
    mask = True
    if "xsi" in s:
        return s
    elif "Namespace" in s:
        return s
    elif "<?" in s:
        return s


    # masking xml attributes

    if ("=" in s) and ("\"" in s):
        y = ""
        i = 0
        while (i < len(s)):
            if s[i] == "=":
                c = 0
                while c < 2:
                    y = y + maskGenerator(s[i])
                    i += 1
                    if s[i] == ("\""):
                        c += 1

            y = y + s[i]
            i += 1
        return y

    else:
        return s


def xmlSpecificTagMask(s, masked,tag_mask_flag,userInput=[], xpath=""):
    
    flag = False
    if "<?" in s:
        return xmlTagMask(s), True, xpath, masked
    elif "!--" in s:
        return xmlTagMask(s), True, xpath,masked
    else:
        xmlAttList = []
        att = "None"
        xmlTag = ""
        r = ""
        r = s.strip()

        if "=" in r:
            xmlAttList = r.split("=")
            xmlTag = xmlAttList[0].split(' ')[0]
            xmlTag = xmlTag[1:]
            if 'ns:' in xmlTag:
                x = xmlTag.split(":")
                xmlTag = x[1]


        else:
            xmlTag = r
            xmlTag = r[1:]
            if 'ns:' in xmlTag:
                x = xmlTag.split(":")
                xmlTag = x[1]

        if xpath == "" or xpath == None:

            xpath = "/" + xmlTag
        else:
            if xmlTag != None:
                xpath = xpath + "/" + xmlTag
        if(len(userInput) > 0):
            for i in userInput:
                 if ((i == xpath)):
                     if tag_mask_flag:
                            masked += 1
                     return xmlTagMask(s), True, xpath,masked
        else:
            return xmlTagMask(s), True, xpath, masked

        return s, False, xpath, masked


def xpathModification(xpath, endTag,tag_count):
    if xpath == "":
        return "", tag_count

    if 'ns:' in endTag:
        x = endTag.split(":")
        endTag = "/"+x[1]

    endTag = endTag.strip()
    xpathList = xpath.split("/")
    if xpathList[-1] == endTag[1:]:
        del xpathList[-1]
        tag_count = tag_count + 1

    c = "/"
    #print(xpathList)
    xpath = c.join(xpathList)
    #print(xpath)
    return xpath,tag_count


def jsonmaskgenerator(s):  # function to mask json content

    if ":" not in s:  # checking for : sign
        return s

    if ("}" in s) or ("]" in s):
        c = 0
        r = ""
        i = 0

        while (
            (s[i] != "}")
            or (s[i] != "]")
        ):  # iterating and appending the content of the xml attribure and then performing slicing to mask the content


            r = r + s[i]
            c += 1
            i += 1
            if (i >= (len(s) - 1)):
                break

        k = r.split(':')
        s = s[c:]
        m = maskGenerator(k[1], isJson = True)


        return ":" + m + s

    else:
        m = s.split(':')
        ## fix 30th May 2019
        ## to handle when there are ":" in the contents as well
        if len(m) > 2:
            m = m[1:]
            k = ':'.join(m)
            c = []
            c.append('')
            c.append(k)
            m = c
            c = []
            k = ''
        ## end of fix
        n = maskGenerator(m[1], isJson = True)
        return ":" + n



def xmlParse(input, out, bufferbyte, tag_count,masked,mask=""):
    
    count_lt = count_gt = delta_tagcount = 0 #Valdemar
    additional = cdataExtra = "" #Valdemar
    cdataStart = "<![CDATA[" #Valdemar
    breakFlag = False #Valdemar
    isDoubleQuoted = False #Valdemar
    
    listmask = []
    xpath = ""
    cdataList = []
    cdataInitial = False
    cdata = False
    cdataContent = ""
    mask = str(mask)
    tag_mask_flag  = True
    
    if ',' in mask:
        listmask = mask.split(',')
    elif mask == "" or mask == "None":
        listmask = []
    else:
        listmask.append(mask)

    if len(listmask) > 0:
        shouldMask = False
    else:
        shouldMask = True
    additional_content = ""  # to store the contents of the line if it is not ending with > tag
    with open(input, buffering=bufferbyte, encoding="utf-8") as file:
        
        generator = read_in_chunks(file, bufferbyte // 2)
        while True:
            
            try:
                if not additional:
                    file_content = next(generator)
                    if not file_content.strip():
                        break
                else:
                    file_content = additional
                    additional = ""

                cdata = True if cdataStart in file_content else False

                if not cdata:
                    #print('cdata false')
                    if True:
                        file_content_parts = file_content.split('"')
                        countingContent = " ".join([file_content_parts[i] for i in range(len(file_content_parts)) if i%2==int(isDoubleQuoted)])
                        count_lt = countingContent.count("<")
                        count_gt = countingContent.count(">")

                    if count_lt==count_gt:
                        tag_count, masked = XmlHandleNormalContent(file_content, out, tag_count, masked, mask, tag_mask_flag, listmask, xpath, shouldMask)
                        file_content=""
                    
                    else: #elif count_lt>count_gt:
                        delta_tagcount = count_lt-count_gt
                        while delta_tagcount>0:
                            additional = next(generator)
                            if not cdataStart in additional:
                                for symbol_i in range(len(additional)):
                                    symbol = additional[symbol_i]

                                    if symbol=='"':
                                        isDoubleQuoted = not isDoubleQuoted

                                    elif not isDoubleQuoted:
                                        if symbol=="<":
                                            delta_tagcount+=1
                                        elif symbol==">":
                                            delta_tagcount-=1
                                    file_content+=symbol
                                    if delta_tagcount==0:
                                        additional = additional[symbol_i+1:]
                                        tag_count, masked = XmlHandleNormalContent(file_content, out, tag_count, masked, mask, tag_mask_flag, listmask, xpath, shouldMask)
                                        file_content=""
                                        breakFlag = True
                                        break
                                if breakFlag:
                                    breakFlag = False
                                    break
                            else:
                                result = additional.find(cdataStart)
                                cdataContent = additional[result:]
                                #file_content+= additional[:result]
                                if additional[:result]:

                                    file_content_parts = additional[:result].split('"')
                                    countingContent = " ".join([file_content_parts[i] for i in range(len(file_content_parts)) if i%2==int(isDoubleQuoted)])
                        
                                    new_count_lt = countingContent.count("<")
                                    new_count_gt = countingContent.count(">")
                                    if delta_tagcount+new_count_lt-new_count_gt==0: #all tags closed before cdata
                                        delta_tagcount=0
                                        file_content+= additional[:result]
                                        tag_count, masked = XmlHandleNormalContent(file_content, out, tag_count, masked, mask, tag_mask_flag, listmask, xpath, shouldMask)
                                        file_content = ""
                                        additional = cdataContent
                                    
                                        break #while delta_tagcount>0:
                                    else: #close maximum tags before cdata
                                        for symbol_i in range(len(additional[:result])):
                                            symbol = additional[:result][symbol_i]

                                            if symbol=='"':
                                                isDoubleQuoted = not isDoubleQuoted

                                            elif not isDoubleQuoted:
                                                if symbol=="<":
                                                    delta_tagcount+=1
                                                elif symbol==">":
                                                    delta_tagcount-=1
                                            file_content+=symbol
                                            if delta_tagcount==0:
                                                additional = additional[symbol_i+1:]
                                                tag_count, masked = XmlHandleNormalContent(file_content, out, tag_count, masked, mask, tag_mask_flag, listmask, xpath, shouldMask)
                                                file_content=""
                                                breakFlag = True
                                                break #for symbol_i

                                        if not breakFlag:
                                            tag_count, masked, additional, isDoubleQuoted = XmlHandleCdata(file_content, cdataContent, generator, out, tag_count, delta_tagcount, shouldMask, masked, mask, tag_mask_flag, listmask, xpath, isDoubleQuoted)
                                            breakFlag = True
                                            
                                        if breakFlag:
                                            breakFlag = False
                                            break #while delta_tagcount>0:
                                else:
                                    tag_count, masked, additional, isDoubleQuoted = XmlHandleCdata(file_content, cdataContent, generator, out, tag_count, delta_tagcount, shouldMask, masked, mask, tag_mask_flag, listmask, xpath, isDoubleQuoted)
                else: #if cdata
                    result = file_content.find(cdataStart)
                    cdataContent = file_content[result:]
                    file_content = file_content[:result]
                    delta_tagcount = 0
                    if file_content:

                        file_content_parts = file_content.split('"')
                        countingContent = " ".join([file_content_parts[i] for i in range(len(file_content_parts)) if i%2==int(isDoubleQuoted)])
                        
                        new_count_lt = file_content_parts.count("<")
                        new_count_gt = file_content_parts.count(">")
                        if delta_tagcount+new_count_lt-new_count_gt==0:
                            delta_tagcount=0
                            tag_count, masked = XmlHandleNormalContent(file_content, out, tag_count, masked, mask, tag_mask_flag, listmask, xpath, shouldMask)
                            file_content=""
                            additional = cdataContent
                        
                        else: #close maximum tags before cdata
                            for symbol_i in range(len(file_content)):
                                symbol = file_content[symbol_i]

                                if symbol=='"':
                                    isDoubleQuoted = not isDoubleQuoted

                                elif not isDoubleQuoted:
                                    if symbol=="<":
                                        delta_tagcount+=1
                                    elif symbol==">":
                                        delta_tagcount-=1
                                        
                                file_content+=symbol
                                if delta_tagcount==0:
                                    additional = file_content[symbol_i+1:]
                                    tag_count, masked = XmlHandleNormalContent(file_content, out, tag_count, masked, mask,tag_mask_flag, listmask, xpath, shouldMask)
                                    file_content=""
                                    break #for symbol_i
                            if delta_tagcount!=0:
                                tag_count, masked, additional, isDoubleQuoted = XmlHandleCdata(file_content, cdataContent, generator, out, tag_count, delta_tagcount,shouldMask, masked, mask, tag_mask_flag, listmask, xpath, isDoubleQuoted)

                    else:
                        tag_count, masked, additional, isDoubleQuoted = XmlHandleCdata(file_content, cdataContent, generator, out, tag_count, delta_tagcount,shouldMask, masked, mask, tag_mask_flag, listmask, xpath, isDoubleQuoted)
                                
                        
            except StopIteration:
                if not cdata and file_content:
                    tag_count, masked = XmlHandleNormalContent(file_content, out, tag_count, masked, mask,tag_mask_flag, listmask, xpath, shouldMask)
                    file_content=""
                break

        if(len(listmask) < 1):
            masked = tag_count

    return tag_count,masked


def XmlHandleNormalContent(file_content, out, tag_count, masked, mask, tag_mask_flag, listmask, xpath, shouldMask):
    
    if True:
        if True:
            if True:
                if True:
                    if file_content:
                        lines = file_content.split('>')

                        if type(out)==str:
                            file2 = open(out, "a+", encoding="utf-8")
                        else:
                            file2 = out
                        if True:
                        
                            for i in lines:  # iterating through the lines
                                if not len(i.strip())>1: continue
                            
                                if (i.strip().startswith('<') and i.strip()[1] != "/"):
    
                                    i, shouldMask, xpath,masked = xmlSpecificTagMask(i,masked,tag_mask_flag , listmask, xpath)  # masking xml atrribute

                                    file2.write(i + ">")  # writing in the output file

                                else:
                                    b = i.split("<")  # splitting based on opening tag
                                    if (sys.version_info[
                                        0] < 3):  # since below python 3 we do not have unicode characters by default.
                                        if shouldMask == True:
                                            file2.write(maskGenerator(b[0], True).decode('utf-8'))  # masking the attributes

                                        else:
                                            file2.write(b[0].decode('utf-8'))
                                        if len(b) > 1:
                                            #Fix May19 issue reported by kris
                                            try:
                                                xpath,tag_count = xpathModification(xpath, xmlTagMask(b[1]),tag_count)
                                            except Exception:
                                                xpathModification(xpath, xmlTagMask(b[1]),tag_count)
                                            #Fix complete
                                            file2.write("<" + xmlTagMask(b[1]) + ">")  # appending the closing tags

                                    else:
                                        if shouldMask == True:
                                            file2.write(maskGenerator(b[0], True))  # masking the attributes


                                        else:   
                                            file2.write(b[0])
                                        if len(b) > 1:
                                            xpath,tag_count = xpathModification(xpath, xmlTagMask(b[1]),tag_count)

                                            file2.write("<" + xmlTagMask(b[1]) + ">")  # appending the closing tags
                                            
                        if type(out)==str:
                            file2.close() #close only regular file with string name and do not touch StringIO's
    if(len(listmask) < 1):
        masked = tag_count

    return tag_count,masked



def XmlHandleCdata(file_content, cdataContent, generator, out, tag_count, delta_tagcount, shouldMask, masked, mask, tag_mask_flag, listmask, xpath, isDoubleQuoted):
    
    cdataEnding =  "]]>"
    cdataStart = "<![CDATA[" 
    tempFile, tempFile_Cdata = StringIO(), StringIO()
    cdataStartPosition = len(file_content)
    additional = ""

    if cdataEnding in cdataContent: #short cdata
        result = cdataContent.find(cdataEnding)+len(cdataEnding)
        additional = cdataContent[result:]
        cdataContent=cdataContent[:result]

        file_content_parts = additional.split('"')
        countingContent = " ".join([file_content_parts[i] for i in range(len(file_content_parts)) if i%2==int(isDoubleQuoted)])


        new_count_lt = countingContent.count("<")
        new_count_gt = countingContent.count(">")
        
        

    else:
        while not cdataEnding in cdataContent:
            cdataExtra = next(generator)
            if cdataEnding in cdataExtra:
                result = cdataExtra.find(cdataEnding)+len(cdataEnding) #< tag should not be counted
                cdataContent+=cdataExtra[:result]
                additional = cdataExtra[result:]

                file_content_parts = additional.split('"')
                countingContent = " ".join([file_content_parts[i] for i in range(len(file_content_parts)) if i%2==int(isDoubleQuoted)])
                
                new_count_lt = countingContent.count("<")
                new_count_gt = countingContent.count(">")
                break
            else:
                cdataContent+=cdataExtra


    if True:
        if (sys.version_info[0] < 3):  # since below python 3 we do not have unicode characters by default.
            if shouldMask == True:
                tempFile_Cdata.write(maskGenerator(cdataContent, True).decode('utf-8'))  # masking the attributes

            else:
                tempFile_Cdata.write(cdataContent.decode('utf-8'))

        else:
            if shouldMask == True:
                tempFile_Cdata.write(maskGenerator(cdataContent, True))  # masking the attributes

            else:
                tempFile_Cdata.write(cdataContent)

    

    #cdata part ends!!!!
    
    if additional:
        if delta_tagcount+new_count_lt-new_count_gt==0:
            delta_tagcount=0
            file_content+= additional
            if not cdataStart in additional:
            
                tag_count, masked = XmlHandleNormalContent(file_content, tempFile, tag_count, masked, mask, tag_mask_flag, listmask, xpath, shouldMask)
                file_content=""; additional=""
        else:
            
            for symbol_i in range(len(additional)):
                symbol = additional[symbol_i]

                if symbol=='"':
                    isDoubleQuoted = not isDoubleQuoted

                elif not isDoubleQuoted:
                    if symbol=="<":
                        delta_tagcount+=1
                    elif symbol==">":
                        delta_tagcount-=1
                file_content+=symbol
                if delta_tagcount==0:
                    additional = additional[symbol_i+1:]
                    tag_count, masked = XmlHandleNormalContent(file_content, tempFile, tag_count, masked, mask, tag_mask_flag, listmask, xpath, shouldMask)
                    file_content=""
                    break

            if delta_tagcount!=0:
                while True:
                    
                    additional = next(generator)
                    if cdataStart in additional:
                        raise ValueError("We don't expect 2 cdata's! Generally this case should'n happen. Please report the issue")

                    for symbol_i in range(len(additional)):
                        symbol = additional[symbol_i]
                        if symbol=="<":
                            delta_tagcount+=1
                        elif symbol==">":
                            delta_tagcount-=1
                        file_content+=symbol
                        if delta_tagcount==0:
                            additional = additional[symbol_i+1:]
                            tag_count, masked = XmlHandleNormalContent(file_content, tempFile, tag_count, masked, mask, tag_mask_flag, listmask, xpath, shouldMask)
                            file_content=""
                            break

                    if delta_tagcount==0:
                        break

    firstPart = tempFile.getvalue()
    secondPart = tempFile_Cdata.getvalue()
    finalString = firstPart[:cdataStartPosition]+secondPart+firstPart[cdataStartPosition:]
    open(out, 'a+', encoding = 'utf8').write(finalString)
    
        
    

    if(len(listmask) < 1):
        masked = tag_count
        
    return tag_count,masked, additional, isDoubleQuoted




def jsonParse(input, out, bufferbyte):
    additiona_content = ""  # to store line not ending with :
    
    with open(input, buffering=bufferbyte, encoding="utf-8") as file:
        if True:
            content = file.read()
        #for content in read_in_chunks(file, (int(bufferbyte / 2))):

            if additiona_content != "":
                content = additiona_content + content  # adding remaining content to the new content
            if content[-1] == ':':
                content = content[:-1]
                additiona_content = ':'

            else:
                c = 0
                for k in reversed(content):
                    if k == ':':
                        break
                    c += 1
                additiona_content = content[-c - 1:]  # adding the contents till :
                content = content[
                          :-c - 1]  # removing the contents by slicing off the data present in additional content
                
                with open(out, "a+", encoding="utf-8") as file2:
                    i = 0
                    s = ""
                    while (i < len(content)):
                        if content[i] == ":":
                            r = ""
                            while (content[i] != ","):  # iterating through the data to mask
                                check = i  # #to change the value of i later on if the list has data instead of k,v pairs
                                flag = False
                                if content[i] == '[':  # to check wehter the list has key value pairs

                                    k = ""
                                    while content[check] != ']':

                                        if content[check] == '{':
                                            flag = True
                                            break
                                        else:
                                            
                                            if content[check:check+4]=='true':
                                                
                                                k+="true"
                                                check+=4
                                            elif content[check:check+5]=='false':
                                                
                                                k+="false"
                                                check+=5
                                            else:
                                                k = k + maskGenerator(content[check])
                                            
                                                check += 1
                                    if flag == False:
                                        i = check + 1
                                        s = s + ":" + k + "]"
                                        r = ""
                                        #30th May Fix
                                        break
                                        #end

                                if flag == True or i < len(content):

                                    if content[i] == '{' or content[i] == '[':
                                        r = r + content[i]
                                        i = i + 1
                                        break

                                    else:
                                        # s = s + content[i]
                                        r = r + content[i]
                                        i = i + 1

                            if r != "":
                                if ('{' not in r) or ('[' not in r):
                                    s = s + jsonmaskgenerator(r)
                                else:
                                    s = s + r

                        else:
                            s = s + content[i]
                            i += 1

                    file2.write(s)

    with open(out, "a", encoding="utf-8") as file2:
        file2.write(jsonmaskgenerator(additiona_content))


def commandLine(args):
    file_count = 0
    if args.log != "":
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.FileHandler(args.log),
                logging.StreamHandler()
            ])

    else:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.StreamHandler()
            ])

    logger = logging.getLogger()



    if args.input != "":

        if (os.path.isdir(args.input)):
            inputDirectory = args.input + "/"
            if not os.path.exists(args.outputDir):
                try:
                    os.makedirs(args.outputDir)
                except:
                    logger.warning("Exiting no write access")
                    sys.exit()
            if not os.access(args.outputDir, os.W_OK):
                logger.warning('Exiting no write access')
                sys.exit()
            files = []
            logger.info("Initializing Masking")
            logger.info("Processing")
            for subdir, dirs, allfiles in os.walk(inputDirectory):
                for file in allfiles:
                    files.append(os.path.join(subdir, file))
            for names in files:
                tag_count = 0
                tag_mask = 0
                name, ext = os.path.splitext(names)
                fileName = name.split(inputDirectory)
                output = args.outputDir + "/" + fileName[-1] + ext
                if not os.path.exists(os.path.dirname(output)):
                    os.makedirs(os.path.dirname(output))
                if os.path.exists(output):
                    os.remove(output)


                if ext == ".xml":
                    tag_count,tag_mask = xmlParse((names), output, args.byteSize,tag_count ,tag_mask, args.mask)
                    logger.info("Completed Processing " + inputDirectory + names + " Maksed file location " + output)
                    logger.info("Total tags found in "+name + " = "+ str(tag_count))
                    logger.info("Total tags masked in  " + name + " = " + str(tag_mask))

                elif ext == ".json":
                    
                    jsonParse((names), output, args.byteSize)
                    logger.info("Completed Processing " + names + " Maksed file location " + output)
                file_count += 1

            logger.info("Total files Masked "+str(file_count))







        elif os.path.isfile(args.input):
            tag_count = 0
            tag_mask = 0
            name, ext = os.path.splitext(args.input)
            fileName = name.split("/").pop()
            if not os.path.exists(args.outputDir):
                try:
                    os.makedirs(args.outputDir)
                except:
                    logger.warning("Exiting no write access")
                    sys.exit()
            if not os.access(args.outputDir, os.W_OK):
                logger.warning("Exiting no write access")
                sys.exit()
            output = args.outputDir + "/" + fileName + ext
            if os.path.exists(output):
                os.remove(output)

            logger.info("Initialising Masking")

            if ext == ".xml":
                tag_count,tag_mask = xmlParse(args.input, output, args.byteSize,tag_count,tag_mask, args.mask)
                logger.info("Completed Processing " + args.input + " Maksed file location " + output)
                logger.info("Total tags found in " + fileName + " = " + str(tag_count))
                logger.info("Total tags masked in  " + fileName + " = " + str(tag_mask))

            elif ext == ".json":
                logger.info("Processing " + fileName)
                
                jsonParse(args.input, output, args.byteSize)
                logger.info("Completed Processing " + args.input + " Maksed file location " + output)



            else:
                logger.warning("Please provide valid xml/json file")
                sys.exit()

            logger.info("Masking Completed")
        else:
            logger.warning("Invalid directory/ File ")
            sys.exit()

    else:
        logger.warning("Please provide input")
        sys.exit()


def main():
    parser = argparse.ArgumentParser(description="Data Masking")

    
    parser.add_argument("-i", help="Input Directory Name / File Name", dest="input", type=str, required=True)
    parser.add_argument("-b", help="Provide byte size to buffer", dest="byteSize", type=int, default="2000000")
    parser.add_argument("-o", help="Output Directory Name", dest="outputDir", type=str, required=True)
    parser.add_argument("-l", help="Input xpath or xpaths seperated by ,", dest="mask", type=str)
    parser.add_argument("-L", help="Output in Log File",dest="log", type=str,default="")
    parser.set_defaults(func=commandLine)
    args = parser.parse_args()
    args.func(args)
    return args


if __name__ == "__main__":
    
    args = main()

