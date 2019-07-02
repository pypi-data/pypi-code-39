

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
import sys


filename=sys.argv[1]
filename2='/global/cscratch1/sd/jiabin/jetcount/V/'+filename[2:-4]+'V.nc'
print filename2
rootgrp=Dataset(filename,'r')
U=rootgrp.variables['U'][:]
lat=rootgrp.variables['lat'][:]
lon=rootgrp.variables['lon'][:]
#plev=rootgrp.variables['plev'][:]
rootgrp2=Dataset(filename2,'r')
V=rootgrp2.variables['V'][:]

latrange=np.arange(384,683)
lonrange=np.arange(192,513)
#lonindex=np.array([192,224,256,288,320,352,384,416,448,480,512])

def getregion200mb(inputarray):
    V2=inputarray[:,9,latrange,:]
    V3=V2[:,:,lonrange]
    return V3

def windspeedcalc(Uarray,Varray):
    wind=np.sqrt(np.square(Uarray)+np.square(Varray))
    maskeasterly=Upick<0
    windmasked=ma.masked_array(wind,mask=maskeasterly)
    return windmasked


def getmax(windinput):
    maxwind=np.amax(windinput,axis=1)
    return maxwind


def getmaxloc(windinput):
    maxargument=np.argmax(wind,axis=1)
    reallat=lat[latrange[maxargument]]
    return reallat

timestring=filename.split('.')[3]
datestring=timestring[0:-6]

Upick=getregion200mb(U)
Vpick=getregion200mb(V)
wind=windspeedcalc(Upick,Vpick)


maxwind_strength=getmax(wind)
maxwind_lat=getmaxloc(wind)

maxwindname=datestring+'maxwind.txt'
maxlocname=datestring+'maxwindlat.txt'

np.savetxt(maxwindname, maxwind_strength, delimiter=',',newline='\n' ) 
np.savetxt(maxlocname, maxwind_lat, delimiter=',',newline='\n' ) 




