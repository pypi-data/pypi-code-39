from datetime import date, datetime, timedelta
from collections import OrderedDict
import random

def customHourSlicing(startDate, endDate, sliceSize):
    startDate = datetime.strptime(startDate,"%Y-%m-%d")
    endDate = datetime.strptime(endDate,"%Y-%m-%d")
    delta=timedelta(hours=sliceSize)
    d = startDate
    list=[]
    while d<(endDate+timedelta(days=1)):
        if (d + delta - timedelta(minutes=1))>(endDate+timedelta(days=1)):
            list.append((datetime.strftime(d,"%Y-%m-%d %H:%M"),datetime.strftime(endDate+timedelta(days=1) - timedelta(minutes=1),"%Y-%m-%d %H:%M")))
        else:
            list.append((datetime.strftime(d,"%Y-%m-%d %H:%M"),datetime.strftime(d + delta - timedelta(minutes=1),"%Y-%m-%d %H:%M")))
        d +=delta
    return list

def hourlySlicing(startDate, endDate):
    list = customHourSlicing(startDate, endDate, 1)
    return list

def customSlicing(startDate, endDate, sliceSize):
    endDate = datetime.strftime(datetime.strptime(endDate,"%Y-%m-%d"),"%Y-%m-%d")
    delta=timedelta(days=sliceSize)
    d = datetime.strptime(startDate,"%Y-%m-%d")
    list=[]
    while d <= datetime.strptime(endDate,"%Y-%m-%d"):
        sliceStart = (datetime.strftime(d,"%Y-%m-%d"))
        sliceEnd = datetime.strftime((d+delta-timedelta(1)),"%Y-%m-%d")
        if sliceEnd>endDate:
            sliceEnd=endDate
        else:
            pass
        list.append((sliceStart,sliceEnd))
        d += delta
    return list

# Function to split date time ranges into daily microbatches
def dailySlicing(startDate,endDate):
    list = customSlicing(startDate, endDate, 1)
    return list

# Function to split date time ranges into weekly microbatches
def weeklySlicing(startDate,endDate):
    endDate = datetime.strftime(datetime.strptime(endDate,"%Y-%m-%d"),"%Y-%m-%d")
    delta=timedelta(days=7)
    d = datetime.strptime(startDate,"%Y-%m-%d")
    list=[]
    while d <= datetime.strptime(endDate,"%Y-%m-%d"):
        if d+timedelta(days=6) >= datetime.strptime(endDate,"%Y-%m-%d"):
            list.append((datetime.strftime(d,"%Y-%m-%d"),datetime.strftime(datetime.strptime(endDate,"%Y-%m-%d"),"%Y-%m-%d")))
        else:
            list.append((datetime.strftime(d,"%Y-%m-%d"),datetime.strftime(d+timedelta(days=6),"%Y-%m-%d")))
        d += delta
    return list

# Function to split date time ranges into monthly microbatches
def monthlySlicing(startDate, endDate):
    dates = [startDate, endDate]
    start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
    total_months = lambda dt: dt.month + 12 * dt.year
    mlist = []
    for tot_m in range(total_months(start)-1, total_months(end)):
        y, m = divmod(tot_m, 12)
        if tot_m == total_months(start)-1:
            mlist.append(dates[0])
        else:
            mlist.append(datetime(y, m + 1, 1).strftime("%Y-%m-%d"))
    mlist.append(datetime.strftime(end, "%Y-%m-%d"))
    listoflists=[]
    for i in range(len(mlist)-1):
        if i==(len(mlist)-2):
            listoflists.append((mlist[i],mlist[i+1]))
        else:
            listoflists.append((mlist[i],datetime.strftime(datetime.strptime(mlist[i+1], "%Y-%m-%d")-timedelta(1), "%Y-%m-%d")))
    return listoflists

def yearlySlicing(startDate, endDate):
    startYear = datetime.strftime(datetime.strptime(startDate,"%Y-%m-%d"),"%Y")
    endYear = datetime.strftime(datetime.strptime(endDate,"%Y-%m-%d"),"%Y")
    list=[]
    for year in range(int(startYear),int(endYear)+1):
        if year==int(startYear):
            list.append((startDate,'{}-12-31'.format(year)))
        elif year==int(endYear):
            list.append(('{}-01-01'.format(year),endDate))
        else:
            list.append(('{}-01-01'.format(year),'{}-12-31'.format(year)))
    return list

def simericalSlicing(startDate,endDate,slices):
    startDate = datetime.strptime(startDate,"%Y-%m-%d")
    endDate = datetime.strptime(endDate,"%Y-%m-%d")
    delta=(endDate-startDate)/(slices)
    d = startDate
    list = []
    while d < endDate:
        if (d+delta)>endDate:
            list.append((datetime.strftime(d,"%Y-%m-%d"),datetime.strftime(endDate,"%Y-%m-%d")))
        else:
            list.append((datetime.strftime(d,"%Y-%m-%d"),datetime.strftime(d+delta,"%Y-%m-%d")))
        d += delta
    return list

def approximateSimericalSlicing(startDate,endDate,slices):
    startDateSlice = datetime.strptime(startDate,"%Y-%m-%d")
    endDateSlice = datetime.strptime(endDate,"%Y-%m-%d")
    delta=(endDateSlice-startDateSlice)/(slices)
    if delta.seconds>=43200:
        sliceSize = delta.days+1
    else:
        sliceSize = delta.days
    list = customSlicing(startDate, endDate, sliceSize)
    return list

def randomSlice(startDate,endDate, level='hour'):
    startDateSlice = datetime.strptime(startDate,"%Y-%m-%d")
    endDateSlice = datetime.strptime(endDate,"%Y-%m-%d")
    delta=(endDateSlice-startDateSlice)
    d=startDateSlice
    list=[]
    if level=='hour':
        timeDiff = delta.days*86400 + delta.seconds
        while True:
            randDelta = timedelta(seconds=random.randint(1,timeDiff))
            if d+randDelta>endDateSlice:
                list.append((datetime.strftime(d,"%Y-%m-%d %H:%M"),datetime.strftime(endDateSlice,"%Y-%m-%d %H:%M")))
                break
            else:
                list.append((datetime.strftime(d,"%Y-%m-%d %H:%M"),datetime.strftime(d+randDelta,"%Y-%m-%d %H:%M")))
            d += randDelta + timedelta(seconds=60)
    elif level=='day':
        timeDiff = delta.days
        while True:
            randDelta = timedelta(days=random.randint(1,timeDiff))
            if d+randDelta>endDateSlice:
                list.append((datetime.strftime(d,"%Y-%m-%d"),datetime.strftime(endDateSlice,"%Y-%m-%d")))
                break
            else:
                list.append((datetime.strftime(d,"%Y-%m-%d"),datetime.strftime(d+randDelta,"%Y-%m-%d")))
            d += randDelta + timedelta(seconds=60)
    else:
        pass
    return list

# Function to split a function date ranges into smaller microbatches
def batch_process(function, startDate,endDate, frequency, **kwargs ):
    if frequency=='DAILY':
        dates = dailySlicing(startDate,endDate)
    elif frequency=='WEEKLY':
        dates = weeklySlicing(startDate,endDate)
    elif frequency=='MONTHLY':
        dates = monthlySlicing(startDate, endDate)
    list=[]
    for i in range(len(dates)):
        result = function(startDate = dates[i][0],endDate = dates[i][1], **kwargs )
        list.append(result)
    return list
