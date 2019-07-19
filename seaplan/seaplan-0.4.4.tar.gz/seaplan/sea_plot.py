#!/usr/bin/env python3
""" 
Plotting routines for seaplan
"""
########### STANDARD LIBRARIES
import math
from datetime import datetime
########## SCIPY LIBRARIES
import numpy as np
from scipy.io import netcdf
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from pylab import cm
########## CUSTOM LIBRARIES
from .shading import set_shade

########### CONSTANTS
font_size=7
text_offset=0.05 # degrees from station
text_bbox=dict(boxstyle="round",pad=0.1,edgecolor='none',facecolor='white', alpha=0.5)
#############################################################################

def plot_map(events,orig_stations,params):
    # Plot basemap
    mp=params['map']
    m=plot_basemap(mp['grid'],mp['bounds'],mp.get('bathy_map',False),orig_stations)
    #m=plot_basemap(params['map'],orig_stations)
    iLeg=0
    legSyms=['k-','r-','b-','g-'] # WILL CHANGE COLOR AT EVERY "NEWLEG" event  
    prev_event=events[0].copy()
    for event in events:
        if event['station'] in orig_stations:
          cross_visited_stations(m,event)
        # Update leg # on "NEWLEG" event action  
        if 'action' in event:
            if event['action']=="NEWLEG":
                iLeg=iLeg+1
        if params['map']['plot_past_tracks'] or (event['arrival']['time'] > datetime.now()) :
            plot_track(m,event,prev_event,iLeg,legSyms)
        plot_event(m,event)
        prev_event=event.copy()
    dt= events[-1]['arrival']['time'] - events[0]['departure']['time']
    fig,base_name=close_map(params,dt)
    fig.savefig(f'{base_name}.png',dpi=150)

##############################################################################
#def plot_basemap(params,stations,debug=False) :
def plot_basemap(grid,bounds,bathy_map,stations,debug=False) :
  """ Set up map, plot coastlines (plus bathy if requested) and stations 
  
  Inputs:
    grid: dict with 'x' and 'y' keys
    bounds [list]: [minlon,maxlon,minlat,maxlat]
    bathy_map [boolean]: True: use etopo bathy map, False: no bathy map
              [str]:     filename of netcdf bathymetry file
    stations [dict]: Stations dictionary (keys='type','lon','lat')
    """

  if debug:
    print("In plot_basemap()")
#   grid_x=params['grid']['x']
#   grid_y=params['grid']['y']
#   lonrange= params['bounds'][0:2]
#   latrange= params['bounds'][2:4]
  grid_x=grid['x']
  grid_y=grid['y']
  lon_min,lon_max,lat_min,lat_max= bounds[0],bounds[1],bounds[2],bounds[3]
  # Plot coastlines
  if debug:
    print("Plotting coastlines")
  try:
    m=Basemap(lon_min,lat_min,lon_max,lat_max,projection="merc",resolution='h')
  except:
    print('  mpl_toolkit Basemap high resolution coastline not found, trying intermediate')
    try:
      m=Basemap(lon_min,lat_min,lon_max,lat_max,projection="merc",resolution='i')
    except:
      print('  mpl_toolkit Basemap intermediate resolution coastline not found, using low')
      m=Basemap(lon_min,lat_min,lon_max,lat_max,projection="merc",resolution='l')
  if debug:
    print("Plotting parallels and meridians")
  m.drawparallels(np.arange(math.floor(lat_min/grid_y)*grid_y,math.ceil(lat_max/grid_y)*grid_y,grid_y),labels=[1,0,0,0]) # draw parallels
  m.drawmeridians(np.arange(math.floor(lon_min/grid_x)*grid_x,math.ceil(lon_max/grid_x)*grid_x,grid_x),labels=[0,0,0,1]) # draw meridians
  #if 'bathy_map' in params:
  if not bathy_map:
        pass
  elif isinstance(bathy_map,str):
        # Read in bathy data and make shaded version
        if debug:
            print(f'Plotting bathymetry map {bathy_map}"')
        f=netcdf.netcdf_file(bathy_map,'r')
        lon=f.variables['x'][:].copy()
        lat=f.variables['y'][:].copy()
        z=f.variables['z'][:].copy()
        [xx,yy]=np.meshgrid(lon,lat)
        f.close()
        z_shade = set_shade(np.nan_to_num(z),cmap=cm.jet,scale=2.0,azdeg=0)   
        # Get indices corresponding to map ranges (necessary because extent in imshow leaves an offset)
        ixmin=np.flatnonzero((lon>=lon_min)).min()
        ixmax=np.flatnonzero((lon<=lon_max)).max()
        iymin=np.flatnonzero((lat>=lat_min)).min()
        iymax=np.flatnonzero((lat<=lat_max)).max()
        m.imshow(0.5*z_shade[iymin:iymax,ixmin:ixmax]+0.5)
        m.contour(xx,yy,z,[-5000,-4000,-3000,-2000,-1000,-1],latlon=True,colors='k',linestyles='solid',linewidths=1)
        #m.contour(xx,yy,z,[-2500,-1500,-750,-500,-250],latlon=True,colors='k',linestyles='solid',linewidths=1)
        m.fillcontinents()
  else:
        if debug:
            print(f'Plotting etopo bathymetry map')
        m.etopo()
  m.drawcoastlines(linewidth=3.0, color="black")
  #m.drawcountries()
    
  # plot stations and their names
  if debug:
      print(f'Plotting stations')
  for name,station in stations.items():
      ms=5
      if station['type']=='WayPoint':
          sym='k.'
      elif station['type']=='Operation':
          continue
      elif station['type']=='Survey':
          continue
      elif station['type']=='BB' :
          sym='ro'
          ms=10
      else:
          sym='ro'
      m.plot(station['lon'],station['lat'],sym,markersize=ms,latlon=True)
      #m.plot(event['lon'],event['lat'],'k+',latlon=True)
      x,y = m(station['lon']+text_offset,station['lat'])
      plt.text(x,y,name,fontsize=font_size,va='center',color='gray')
    
  return m

#############################################################################
def plot_track(m,event,prev_event,iLeg,legSyms,debug=False) :
  if debug:
    print("In plot_track()")
  iLeg=iLeg%len(legSyms)
  if event['dist_from_previous'] > 0:
    x,y = m([event['lon'], prev_event['lon']],
                  [event['lat'],prev_event['lat']])
    plt.plot( x, y,legSyms[iLeg])
    plt.arrow(x[1],y[1],.6*(x[0]-x[1]),.6*(y[0]-y[1]),head_width=1000,length_includes_head=True)
#############################################################################
def cross_visited_stations(m,event,debug=False) :
  """ plot a cross if departure_time is specified & before current time """
  if debug:
    print("In cross_visited_stations()")
  if 'depart_time' in event:
    if datetime.strptime(event['depart_time'],'%Y-%m-%dT%H:%M') < datetime.now():
      x,y = m(event['lon'],event['lat'])
      plt.plot( x, y,'kx',markersize=12,linewidth=3)
#############################################################################
def plot_event(m,event,debug=False) :
  if debug:
    print("In plot_event()")
  if event['type']=='Operation':
    m.plot(event['lon'],event['lat'],'r+',markersize=8,lw=5.0,latlon=True)
    x,y = m(event['lon'], event['lat']-text_offset)
    plt.text(x,y,event['station'],fontsize=font_size,va='top',ha='center',
              color='red',bbox=text_bbox)
  else:
    # Station or WayPoint
    m.plot(event['lon'],event['lat'],'+',markersize=5,lw=3.0,latlon=True)
    x,y = m(event['lon']+text_offset, event['lat'])
    if event['hours']!=0:
      plt.text(x,y,event['station'],fontsize=font_size,va='center',
              color='black',bbox=text_bbox)
#############################################################################              
def close_map(params,timedelta_total,debug=False) :
    """ Saves map to a file """
    if debug:
        print("In close_map()")
    base_name=params['file'].split('.')[0]
    plt.title('{}: {:.0f} days {:.0f}h (speed={:g}, latency={:g}h)'\
                      .format(base_name,timedelta_total.days,timedelta_total.seconds/3600.,\
                              params['timing']['ship_speed.kn_i'], \
                              params['timing']['ship_latency.h']),\
                              fontsize=12)
    fig1=plt.gcf()  # Necessary to be able to save after "show" (which creates new figure)
    if params['map']['show_plot']:
        plt.show()
    return fig1,base_name
