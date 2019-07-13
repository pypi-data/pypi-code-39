#
# Author: Juraj Nyiri
#
#
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pyquery import PyQuery
import re
import datetime
import requests

class TavosPy:
    def __init__(self):
        self.url = "http://www.tavos-as.sk/index.php?view=article&catid=121%3Aporuchova-sluba&id=1208%3Anahlasene-odstavky-vody&tmpl=component&print=1&layout=default&page=&option=com_content&Itemid=601"

        self.htmlData = ""
        self.data = ""


    def setUrl(self, url):
        self.url = url
    
    def getUrl(self):
        return self.url

    def sethtmlData(self, data):
        self.htmlData = data
    
    def gethtmlData(self):
        return self.htmlData

    def setData(self, data):
        self.data = data
    
    def getData(self):
        return self.data

    def updateHtml(self):
        try:
            r = requests.get(self.getUrl())
            if(r.status_code == 200):
                self.sethtmlData(r.text)
                return True
        except requests.exceptions.RequestException:
            return False
        return False

    def updateData(self):
        pq = PyQuery(self.htmlData)

        tag = pq('div.article > table > tbody > tr').find('td')

        pattern = re.compile(r'(\d+)')

        data = []
        #Get proper date

        tdChild = 2

        i = 0
        for date in tag('td:nth-child('+str(tdChild)+')').items():
            if(len(data) <= i or data[i] is None):
                data.append({})
            data[i]['date'] = self.findDates(re.findall(pattern, date.text()))
            print(data[i]['date'])
            i+=1
            
        tdChild+=1

        #Get city
        i = 0
        for city in tag('td:nth-child('+str(tdChild)+')').items():
            if(len(data) <= i or data[i] is None):
                data.append({})
            data[i]['city'] = city.text()
            i+=1

        tdChild+=1

        #Get street
        i = 0
        for street in tag('td:nth-child('+str(tdChild)+')').items():
            if(len(data) <= i or data[i] is None):
                data.append({})
            data[i]['street'] = street.text()
            i+=1

        tdChild+=1

        #Get time / date if specified
        i = 0
        time = False
        for time in tag('td:nth-child('+str(tdChild)+')').items():
            startHour = False
            startMinute = False
            endHour = False
            endMinute = False

            pattern = re.compile(r'(\d+):(\d+)')
            matches = re.findall(pattern, time.text())
            if(len(matches) > 0):
                for hour,minute in matches:
                    if(startHour == False or startMinute == False):
                        startHour = hour
                        startMinute = minute
                    else:
                        endHour = hour
                        endMinute = minute
                    if(len(data) <= i or data[i] is None):
                        data.append({})


            #Attempt to find end/start date from time, sometimes they list it there
            pattern = re.compile(r'(\d+)\.(\d+)\.(\d+)')
            matches = re.findall(pattern, time.text())
            if(len(matches) >= 2):
                for day, month, year in reversed(matches):
                    data[i]['date']['end'] = datetime.datetime(int(year), int(month), int(day))
                    break
                
                for day, month, year in (matches):
                    data[i]['date']['start'] = datetime.datetime(int(year), int(month), int(day))
                    break

            if(startHour != False and startMinute != False and data[i]['date']['start'] != False):
                data[i]['date']['start'] = data[i]['date']['start'].replace(hour=int(startHour), minute=int(startMinute))
            if(endHour != False and endMinute != False):
                if(data[i]['date']['end'] == False):
                    if(data[i]['date']['start'] != False):
                        data[i]['date']['end'] = data[i]['date']['start'].replace(hour=int(endHour), minute=int(endMinute))
                else: 
                    data[i]['date']['end'] = data[i]['date']['end'].replace(hour=int(endHour), minute=int(endMinute))
            else:
                if(data[i]['date']['end'] == False):
                    if(data[i]['date']['start'] != False):
                        data[i]['date']['end'] = data[i]['date']['start'].replace(hour=int(23), minute=int(59))
                else:
                    data[i]['date']['end'] = data[i]['date']['end'].replace(hour=int(23), minute=int(59))
            i+=1

        tdChild+=1

        #Get type of defect
        i = 0
        for typeOfDefect in tag('td:nth-child('+str(tdChild)+')').items():
            if(len(data) <= i or data[i] is None):
                data.append({})
            data[i]['typeOfDefect'] = typeOfDefect.text()
            i+=1

        tdChild+=1

        #Get notes
        i = 0
        for note in tag('td:nth-child('+str(tdChild)+')').items():
            if(len(data) <= i or data[i] is None):
                data.append({})
            data[i]['notes'] = note.text()
            i+=1

        #remove table header
        data.pop(0)
        for dayData in data:
            if(dayData['date']['start']):
                if(dayData['date']['start'].year < 1900):
                    if(dayData['date']['end'].year < 1900):
                        dayData['date']['start'] = dayData['date']['start'].replace(year=1900)
                    else: 
                        dayData['date']['start'] = dayData['date']['start'].replace(year=dayData['date']['end'].year)
            if(dayData['date']['end']):
                if(dayData['date']['end'].year < 1900):
                    if(dayData['date']['start'].year < 1900):
                        dayData['date']['end'] = dayData['date']['end'].replace(year=1900)
                    else: 
                        dayData['date']['end'] = dayData['date']['end'].replace(year=dayData['date']['start'].year)

        self.setData(data)
        
        return len(data) > 0

    def update(self):
        return self.updateHtml() and self.updateData()

    #try and detect proper start and end date from sequence of numbers
    def findDates(self, numbers):
        dates = {}
        dates['start'] = False
        dates['end'] = False

        if(len(numbers) > 0):

            startDay = False
            startMonth = False 
            startYear = False

            endDay = False
            endMonth = False
            endYear = False

            for number in numbers:
                if(len(number) <= 2):
                    if(startDay == False):
                        startDay = number
                    elif(startMonth == False):
                        startMonth = number
                    elif(endDay == False):
                        endDay = number
                    elif(endMonth == False):
                        endMonth = number
                elif(len(number) == 4):
                    if(endDay == False):
                        startYear = number
                    else:
                        endYear = number


            if(endDay != False):
                if(endYear == False and startYear != False):
                    endYear = startYear
                elif(startYear == False and endYear != False):
                    startYear = endYear

            if(startDay != False and startMonth != False and startYear != False):
                dates['start'] = datetime.datetime(int(startYear), int(startMonth), int(startDay))
            if(endDay != False and endMonth != False and endYear != False):
                dates['end'] = datetime.datetime(int(endYear), int(endMonth), int(endDay))

        return dates