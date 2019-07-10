#HSMPY3 Code
import math
from datetime import datetime
import pandas as pd
import arcpy
import os
import hsmpy3.common as common
import sys, csv, json, subprocess
import json
import xmltodict
import numpy as np
import urllib.request
import hsmpy3.network as network
import matplotlib.pyplot as plt
from time import gmtime, strftime
import scipy
import numpy
import matplotlib
import astropy
import pytz
import warnings
from matplotlib import cbook
from matplotlib.colors import Normalize
from matplotlib.colors import LinearSegmentedColormap
from numpy import ma
from matplotlib import colors as mcolors
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable


warnings.filterwarnings('ignore')

class domains(object):
#CRASH CATEGORY
    COUNTY     = {'name':'COUNTY'    ,'alias':'County'                            ,'type':'SHORT','field_length':5,'codes':{
        1:'Adams',
        2:'Alexander',
        3:'Bond',
        4:'Boone',
        5:'Brown',
        6:'Bureau',
        7:'Calhoun',
        8:'Carroll',
        9:'Cass',
        10:'Champaign',
        11:'Christian',
        12:'Clark',
        13:'Clay',
        14:'Clinton',
        15:'Coles',
        16:'Cook',
        17:'Crawford',
        18:'Cumberland',
        19:'DeKalb',
        20:'DeWitt',
        21:'Douglas',
        22:'DuPage',
        23:'Edgar',
        24:'Edwards',
        25:'Effingham',
        26:'Fayette',
        27:'Ford',
        28:'Franklin',
        29:'Fulton',
        30:'Gallatin',
        31:'Greene',
        32:'Grundy',
        33:'Hamilton',
        34:'Hancock',
        35:'Hardin',
        36:'Henderson',
        37:'Henry',
        38:'Iroquois',
        39:'Jackson',
        40:'Jasper',
        41:'Jefferson',
        42:'Jersey',
        43:'JoDaviess',
        44:'Johnson',
        45:'Kane',
        46:'Kankakee',
        47:'Kendall',
        48:'Knox',
        49:'Lake',
        50:'LaSalle',
        51:'Lawrence',
        52:'Lee',
        53:'Livingston',
        54:'Logan',
        55:'McDonough',
        56:'McHenry',
        57:'McLean',
        58:'Macon',
        59:'Macoupin',
        60:'Madison',
        61:'Marion',
        62:'Marshall',
        63:'Mason',
        64:'Massac',
        65:'Menard',
        66:'Mercer',
        67:'Monroe',
        68:'Montgomery',
        69:'Morgan',
        70:'Moultrie',
        71:'Ogle',
        72:'Peoria',
        73:'Perry',
        74:'Piatt',
        75:'Pike',
        76:'Pope',
        77:'Pulaski',
        78:'Putnam',
        79:'Randolph',
        80:'Richland',
        81:'Rock Island',
        82:'St. Clair',
        83:'Saline',
        84:'Sangamon',
        85:'Schuyler',
        86:'Scott',
        87:'Shelby',
        88:'Stark',
        89:'Stephenson',
        90:'Tazewell',
        91:'Union',
        92:'Vermilion',
        93:'Wabash',
        94:'Warren',
        95:'Washington',
        96:'Wayne',
        97:'White',
        98:'Whiteside',
        99:'Will',
        100:'Williamson',
        101:'Winnebago',
        102:'Woodford'}}
    DATE       = {'name':'DATE'      ,'alias':'Date'                              ,'type':'DATE','codes':{}}
    NO_VEH     = {'name':'NO_VEH'    ,'alias':'Number of Vehicles'                ,'type':'SHORT','codes':{}}
    CITY       = {'name':'CITY'      ,'alias':'City'                              ,'type':'TEXT','codes':{}}
    CITY_CLASS = {'name':'CITY_CLASS','alias':'City Class'                        ,'type':'SHORT','codes':{
        0:'Unincorporated',
        3:'Chicago',
        4:'Population under 2500',
        5:'2500 - 5000',
        6:'5000 - 10000',
        7:'10000 - 25000',
        8:'25000 - 50000',
        9:'Over 50000'}}
    TOWNSHIP   = {'name':'TOWNSHIP'  ,'alias':'Township'                          ,'type':'TEXT','codes':{}}
    AGENCY     = {'name':'AGENCY'    ,'alias':'Investigating Agency'        ,'type':'SHORT','codes':{
        0:'None',
        1:'City Police',
        2:'County Sheriff',
        3:'State Police',
        4:'All others',
        9:'Unknown'}}
    INT_REL    = {'name':'INT_REL'   ,'alias':'Intersection Related'  ,'type':'SHORT','codes':{
        0:' ',
        1:'Yes'}}
    FUNC_CLASS = {'name':'FUNC_CLASS','alias':'Functional Class'          ,'type':'SHORT','codes':{
        1:'Interstate', #10
        2:'Freeway and Expressway', #20
        3:'Other Principal Arterial', #30
        4:'Minor Arterial',  #40+70
        5:'Major Collector', #50+80
        6:'Minor Collector', #55
        7:'Local Road or Street', #60+90
        10:'Interstate', #1
        20:'Freeway and Expressway', #2
        30:'Other Principal Arterial', #3
        40:'Minor Arterial (Non-Urban)', #4
        50:'Major Collector (Non-Urban)', #5
        55:'Minor Collector (Non-Urban)', #6
        60:'Local Road or Street (Non-Urban)', #7
        70:'Minor Arterial (Urban)', #4
        80:'Collector (Urban)', #5
        90:'Local road or Street (Urban)' #7
        }}
    TWAY_CLASS = {'name':'TWAY_CLASS','alias':'Trafficway Class'                  ,'type':'SHORT','codes':{
        0:'Unmarked Highway rural',
        1:'Controlled rural',
        2:'State numbered rural',
        3:'County and local roads rural',
        4:'Toll roads rural',
        5:'Controlled urban',
        6:'State numbered urban',
        7:'Unmarked highway urban',
        8:'City streets urban',
        9:'Toll roads urban'}}
    TWAY_DESC  = {'name':'TWAY_DESC' ,'alias':'Trafficway Description'            ,'type':'SHORT','codes':{
        1:'Two Way: Not divided', 
        2:'Two Way: Divided, no median barrier',
        2:'Two Way: Divided, with median barrier (not raised)',
        3:'Two Way: Divided, with median barrier',
        4:'Two Way: Center turn lane', 
        5:'Other: One-way or ramp', 
        6:'Other: Alley or driveway',
        7:'Other: 7    Parking lot',
        8:'Other: Other',
        9:'Other: Unknown',
        10:'Other: One-Way', 
        11:'Other: Ramp',
        12:'Other: Alley',
        13:'Other: Driveway'}}
    TCONT_DEV  = {'name':'TCONT_DEV' ,'alias':'Traffic Control Device Type'       ,'type':'SHORT','codes':{
        1:'No controls',
        2:'Stop sign, flasher',
        3:'Traffic signal',
        4:'Yield',
        5:'Police, flagman',
        6:'RR crossing gate',
        7:'Other RR crossing',
        8:'School zone',
        9:'No passing',
        10:'Other regulatory sign',
        11:'Other warning sign',
        12:'Lane use marking',
        13:'Other',
        14:'Delineators',
        99:'Unknown'}}
    TCONT_CON  = {'name':'TCONT_CON' ,'alias':'Traffic Control Device Condition'  ,'type':'SHORT','codes':{
        1:'No controls', 
        2:'Not functioning',
        3:'Functioning improperly',
        4:'Functioning properly', 
        5:'Worn reflective material', 
        6:'Missing',
        7:'Other',
        9:'Unknown'}}
    SURF_CON   = {'name':'SURF_CON'  ,'alias':'Road Surface Conditions'           ,'type':'SHORT','codes':{
        1:'Dry', 
        2:'Wet',
        3:'Snow or slush',
        4:'Ice', 
        5:'Sand, mud, dirt', 
        6:'Other',
        9:'Unknown'}}
    ALIGN      = {'name':'ALIGN'     ,'alias':'Alignment Type'                    ,'type':'SHORT','codes':{
        1:'Straight and level', 
        2:'Straight on grade',
        3:'Straight on hillcrest',
        4:'Curve, level', 
        5:'Curve on grade', 
        6:'Curve on hillcrest',
        9:'Unknown'}}
    DEFECT     = {'name':'DEFECT'    ,'alias':'Road Defects'                      ,'type':'SHORT','codes':{
        1:'No defects', 
        2:'Construction zone',
        3:'Maintenance zone',
        4:'Utility work zone', 
        5:'Work zone – unknown', 
        6:'Shoulders',
        7:'Rut, holes',
        8:'Worn surface',
        9:'Debris on roadway',
        10:'Other', 
        99:'Unknown'}}
    LIGHT      = {'name':'LIGHT'     ,'alias':'Light Condition'                   ,'type':'SHORT','codes':{
        1:'Daylight', 
        2:'Dawn',
        3:'Dusk',
        4:'Darkness', 
        5:'Darkness, lighted road', 
        9:'Unknown'}}
    SUN_ANG    = {'name':'SUN_ANG'   ,'alias':'Sun Angle'                         ,'type':'DOUBLE','codes':{}}
    DAY_NIGHT  = {'name':'DAY_NIGHT' ,'alias':'Day or Night'                      ,'type':'SHORT','codes':{1:'Dawn',2:'Day',3:'Dusk',4:'Night'}}
    WEATHER    = {'name':'WEATHER'   ,'alias':'Weather Conditions'                ,'type':'SHORT','codes':{
        1:'Clear', 
        2:'Rain',
        3:'Snow',
        4:'Fog, smoke, haze', 
        5:'Sleet, hail', 
        6:'Severe cross wind',
        7:'Other',
        8:'Cloudy, overcast',
        9:'Unknown'}}
    COL_TYPE   = {'name':'COL_TYPE'  ,'alias':'Collision Type'                    ,'type':'SHORT','codes':{
        1:'Pedestrian',
        2:'Pedalcyclist',
        3:'Train',
        4:'Animal',
        5:'Overturned',
        6:'Fixed object',
        7:'Other object',
        8:'Other non-collision',
        9:'Parked Motor vehicle',
        10:'Turning',
        11:'Rear-end',
        12:'Sideswipe-same direction',
        13:'Sideswipe-opposite direction',
        14:'Head-on',
        15:'Angle'}}
    CAUSE_1    = {'name':'CAUSE_1'   ,'alias':'Primary Cause'    ,'type':'SHORT','codes':{
        1:'Exceeding authorized speed limit',
        2:'Failing to yield right-of way',
        3:'Following too closely',
        4:'Improper overtaking, passing',
        5:'Driving on wrong side, wrong way',
        6:'Improper turning, no signal',
        7:'Turning right on red',
        8:'Under the influence of alcohol, drugs(use when arrest is effected)',
        10:'Equipment – vehicle condition',
        11:'Weather',
        12:'Road engineering, surface, marking defects',
        13:'Road construction, maintenance',
        14:'Vision obscured (signs, tree limbs, buildings, etc.)',
        15:'Driving skills, knowledge & experience',
        16:'Not in Dictionary',
        17:'Physical condition of driver',
        18:'Unable to determine',
        19:'Had been drinking (use when arrest is not made)',
        20:'Improper lane usage',
        21:'Animal',
        22:'Disregarding yield sign',
        23:'Disregarding stop sign',
        24:'Disregarding other traffic signs',
        25:'Disregarding traffic signals',
        26:'Disregarding road markings',
        27:'Exceeding safe speed for conditions',
        28:'Failing to reduce speed to avoid crash',
        29:'Passing stopped school bus',
        30:'Improper backing',
        32:'Evasive action due to animal, object, non-motorist',
        40:'Distraction – from outside vehicle',
        41:'Distraction – from inside vehicle',
        42:'Distraction – operating a wireless phone',
        42:'Distraction – electronic communication device (cell phone, texting, etc.)',
        43:'Distraction – other electronic device (navigation device, DVD player, etc.)',
        44:'Not in Dictionary',
        45:'Cell phone use other than texting',
        50:'Operating vehicle in erratic, reckless, careless, negligent or aggressive manner',
        60:'Motorcycle advancing legally on red light',
        61:'Bicycle advancing legally on red light',
        99:'Not applicable'}}
    CAUSE_2    = {'name':'CAUSE_2'   ,'alias':'Secondary Cause'  ,'type':'SHORT','codes':CAUSE_1['codes']}       
    HIT_RUN    = {'name':'HIT_RUN'   ,'alias':'Hit and Run'            ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    WZ_REL     = {'name':'WZ_REL'    ,'alias':'Work Zone Related'                 ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    WZ_OCCUR   = {'name':'WZ_OCCUR'  ,'alias':'Occurred in Work Zone'     ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    WZ_TYPE    = {'name':'WZ_TYPE'   ,'alias':'Type of Work Zone'                 ,'type':'SHORT','codes':{
        1:'Blank (Crash in Designated Work Zone was "No")', 
        2:'Construction',
        3:'Maintenance',
        4:'Utility',
        5:'Unknown Work Zone Type'}}
    WZ_WORKER  = {'name':'WZ_WORKER' ,'alias':'Workers Present'         ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    X_COOR     = {'name':'X_COOR'    ,'alias':'X coordinates'         ,'type':'DOUBLE','codes':{}}
    Y_COOR     = {'name':'Y_COOR'    ,'alias':'Y coordinates'         ,'type':'DOUBLE','codes':{}}
    LAT        = {'name':'LAT'       ,'alias':'Latitude'                          ,'type':'DOUBLE','codes':{}}
    LON        = {'name':'LON'       ,'alias':'Longitude'                         ,'type':'DOUBLE','codes':{}}
    KABCO      = {'name':'KABCO'     ,'alias':'KABCO'                             ,'type':'TEXT','codes':{}}
    K          = {'name':'K'         ,'alias':'K Injuries'                        ,'type':'SHORT','codes':{}}
    A          = {'name':'A'         ,'alias':'A Injuries'                        ,'type':'SHORT','codes':{}}
    B          = {'name':'B'         ,'alias':'B Injuries'                        ,'type':'SHORT','codes':{}}
    C          = {'name':'C'         ,'alias':'C Injuries'                        ,'type':'SHORT','codes':{}}
    O          = {'name':'O'         ,'alias':'O Injuries'                        ,'type':'SHORT','codes':{}}
    MP         = {'name':'MP'        ,'alias':'Milepost'                          ,'type':'DOUBLE','codes':{}}
    OFFSET     = {'name':'OFFSET'    ,'alias':'Offset'                            ,'type':'DOUBLE','codes':{}}
    EA_RD      = {'name':'EA_RD'     ,'alias':'Roadway Departure EA'              ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_IM      = {'name':'EA_IM'     ,'alias':'Impaired EA'                       ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_IN      = {'name':'EA_IN'     ,'alias':'Intersection EA'                   ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_DF      = {'name':'EA_DF'     ,'alias':'Distracted_Fatigued_Drwosy EA'     ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_TN      = {'name':'EA_TN'     ,'alias':'Railroad Crossing EA'              ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_WZ      = {'name':'EA_WZ'     ,'alias':'Workzone EA'                       ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_SA      = {'name':'EA_SA'     ,'alias':'Speeding_Aggressive EA'            ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_OD      = {'name':'EA_OD'     ,'alias':'Older Driver EA'                   ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_YD      = {'name':'EA_YD'     ,'alias':'Younger Driver EA'                 ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_HV      = {'name':'EA_HV'     ,'alias':'Heavy Vehicle EA'                  ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_MC      = {'name':'EA_MC'     ,'alias':'Motorcycle EA'                     ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_UO      = {'name':'EA_UO'     ,'alias':'Unrestrained EA'                   ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_PD      = {'name':'EA_PD'     ,'alias':'Pedestrian EA'                     ,'type':'SHORT','codes':{0:' ',1:'Yes'}}
    EA_PC      = {'name':'EA_PC'     ,'alias':'Pedalcyclist EA'                   ,'type':'SHORT','codes':{0:' ',1:'Yes'}}

#PERSON CATEGORY    
    PER_TYPE    = {'name':'PER_TYPE'   ,'alias':'Person Type'                       ,'type':'SHORT','codes':{1:'Driver', 
        2:'Pedestrian',
        3:'Pedalcyclist',
        4:'Equestrian', 
        5:'Occupant of non-motorized vehicle', 
        6:'Noncontact vehicle',
        7:'Passenger'}}
    DOB         = {'name':'DOB'      ,'alias':'Date of Birth'              ,'type':'DATE','codes':{}}
    AGE         = {'name':'AGE'      ,'alias':'Age'                        ,'type':'SHORT','codes':{}}
    SEX         = {'name':'SEX'      ,'alias':'Sex'                        ,'type':'TEXT','codes':{}}
    INJ_SEV     = {'name':'INJ_SEV'  ,'alias':'Injury Severity'            ,'type':'SHORT','codes':{
        0:'No indication of injury',
        1:'C-injury',
        2:'B-injury',
        3:'A-injury',
        4:'Fatality'}}
    SEAT_POS    = {'name':'SEAT_POS' ,'alias':'Seating Position'           ,'type':'SHORT','codes':{
        1:'Driver', 
        2:'Center front',
        3:'Passenger',
        4:'Second row left', 
        5:'Second row center', 
        6:'Second row right',
        7:'Enclosed passengers',
        8:'Exposed passengers',
        9:'Unknown position',
        10:'Third row left',
        11:'Third row center',
        12:'Third row right'}}
    SAF_EQI     = {'name':'SAF_EQI'  ,'alias':'Safety Equipment'                  ,'type':'SHORT','codes':{
        1:'None present', 
        2:'Safety belt used',
        3:'Safety belt not used',
        4:'Helmet used', 
        5:'Helmet not used', 
        6:'Child restraint used',
        7:'Child restraint used improperly',
        8:'Child restraint not used',
        9:'Usage unknown'}}
    AIRBAG      = {'name':'AIRBAG'   ,'alias':'Airbag Deployment'          ,'type':'SHORT','codes':{
        1:'With seat belt', 
        2:'Without seat belt',
        3:'Not applicable',
        4:'Did not deploy', 
        5:'Deployed, front', 
        6:'Deployed, side',
        7:'Deployed other (knee, air belt, etc.)',
        8:'Deployed, combination',
        9:'Deployment unknown'}}
    EJECT       = {'name':'EJECT'    ,'alias':'Ejection'  ,'type':'SHORT','codes':{
        1:'None', 
        2:'Totally ejected',
        3:'Partially ejected',
        4:'Trapped, extricated', 
        9:'Unknown',
        0:'Unknown'}} 
    DR_LIC_ST   = {'name':'DR_LIC_ST' ,'alias':'Drivers License State'     ,'type':'TEXT','codes':{}}
    DR_ACTION   = {'name':'DR_ACTION' ,'alias':'Driver Action'           ,'type':'SHORT','codes':{
        1:'None', 
        2:'Failed to Yield',
        3:'Disregarded control devices',
        4:'Too fast for conditions', 
        5:'Improper turn', 
        6:'Wrong way, side',
        7:'Followed too closely',
        8:'Improper lane change',
        9:'Improper backing',
        10:'Improper passing',
        11:'Improper parking',
        12:'License restrictions',
        13:'Stopped school bus',
        14:'Emergency vehicle on call',
        15:'Evading police vehicle',
        16:'Other',
        44:'Texting',
        45:'Cell phone use other than texting',
        99:'Unknown'}}    
    DR_VISION   = {'name':'DR_VISION' ,'alias':'Driver Vision'        ,'type':'SHORT','codes':{
        1:'Not obscured', 
        2:'Windshield (water, ice)',
        3:'Trees, plants',
        4:'Buildings', 
        5:'Embankment', 
        6:'Signboard',
        7:'Hillcrest',
        8:'Parked vehicles',
        9:'Moving vehicle',
        10:'Blinded-headlights',
        11:'Blinded-sunlight',
        12:'Blowing materials',
        13:'Other',
        99:'Unknown'}}    
    DR_CON      = {'name':'DR_CON'    ,'alias':'Driver Physical Condition'        ,'type':'SHORT','codes':{
        1:'Normal', 
        2:'Impaired-alcohol',
        3:'Impaired-drugs',
        4:'Illness',
        4:'Illness, fainted',        
        5:'Asleep, fainted', 
        6:'Medicated',
        7:'Had been drinking',
        8:'Fatigued',
        8:'Fatigued, asleep',
        9:'Other, unknown',
        9:'Unknown',
        10:'Other',
        11:'Emotional (depressed, angry, distrubed)',
        12:'Removed by EMS',
        88:'Not Reported'}}    
    BAC         = {'name':'BAC'       ,'alias':'Blood Alcohol Concentration'      ,'type':'SHORT','codes':{
        95:'Test refused',
        96:'Test not offered',
        97:'Test performed, results unknown'}}
    CELL_USE    = {'name':'CELL_USE'  ,'alias':'Cellphone Usage'                  ,'type':'SHORT','codes':{0:'No',1:'Yes'}}    
    PD_ACTION   = {'name':'PD_ACTION' ,'alias':'Pedestrian Action' ,'type':'SHORT','codes':{
        3:'Ped, pedal act.: turning left', 
        4:'Ped, pedal act.: turning right',
        20:'Ped, pedal act.: enter from drive or alley',
        50:'Ped, pedal act.: no action', 
        51:'Ped, pedal act.: crossing: with signal', 
        52:'Ped, pedal act.: crossing: against signal',
        53:'Enter, leave, cross: school bus (within 50 ft)',
        54:'Enter, leave, cross: parked vehicle',
        55:'Enter, leave, cross: not at intersection',
        56:'Walk, ride: with traffic',
        57:'Walk, ride: against traffic',
        58:'Walk, ride: to or from disabled vehicle',
        59:'Other: waiting for school bus',
        60:'Other: playing, working on vehicle',
        61:'Other: playing in roadway',
        62:'Other: standing in roadway',
        63:'Other: working in roadway',
        64:'Other: other action',
        65:'Other: intoxicated ped or pedal',
        99:'Other: unknown, NA'}}    
    PD_LOC      = {'name':'PD_LOC'    ,'alias':'Pedestrian Location','type':'SHORT','codes':{
        1:'In roadway', 
        2:'In crosswalk',
        3:'Not in available crosswalk',
        4:'Crosswalk not available', 
        5:'Driveway access', 
        6:'Not in roadway',
        7:'Bikeway',
        9:'Unknown, NA'}}
    PD_VIS      = {'name':'PD_VIS'    ,'alias':'Pedestrian Visibility','type':'SHORT','codes':{
        1:'No contrasting clothing', 
        2:'Contrasting clothing',
        3:'Reflective material',
        4:'Other light source used'}} 
    EMS125      = {'name':'EMS125'    ,'alias':'Emergency Medical Services'        ,'type':'TEXT','codes':{}}
    HOSPITAL    = {'name':'HOSPITAL'  ,'alias':'Hospital'                          ,'type':'TEXT','codes':{}}    
    
#VEHICLE CATEGORY    
    NO_OCC     = {'name':'NO_OCC'    ,'alias':'Number of Occupants'       ,'type':'SHORT','codes':{}}
    VEHT   = {'name':'VEHT'      ,'alias':'Vehicle Type'                      ,'type':'SHORT','codes':{
        1:'Passenger car', 
        2:'Pickup truck',
        3:'Van, mini-van',
        4:'Bus up to 15 passengers', 
        5:'Bus over 15 passengers', 
        6:'Truck – single unit',
        7:'Tractor with semi-trailer',
        8:'Tractor without semi-trailer)',
        9:'Farm equipment',
        10:'Motorcycle (over 150 cc)',
        11:'Motor driven cycle', 
        12:'Snowmobile',
        13:'All-terrain vehicle (ATV)',
        14:'Other vehicle with trailer',
        15:'Sport utility vehicle (SUV)',        
        16:'Other', 
        20:'Autocycle',
        99:'Unknown, NA'}}
    VEHU    = {'name':'VEHU'      ,'alias':'Vehicle Use'                       ,'type':'SHORT','codes':{
        1:'Not in use', 
        2:'Personal',
        3:'Driver education',
        4:'Ambulance', 
        5:'Fire', 
        6:'Police',
        7:'School bus',
        8:'CTA (Chicago Transit Authority)',
        9:'Mass transit',
        10:'Other transit',
        11:'Military', 
        12:'Agriculture',
        13:'Tow truck',
        14:'Construction, maintenance',
        15:'House trailer',        
        16:'Camper, RV - towed, multi-unit', 
        17:'Camper, RV – single unit',
        18:'Taxi, for hire',
        20:'Commercial – multi-unit',
        21:'Commercial – single unit',
        22:'State owned',
        25:'Rideshare (Uber, Lyft, etc.)',
        24:'Lawn care, Landscaping',
        98:'Other',
        99:'Unknown, NA'}}
    MANV    = {'name':'MANV'    ,'alias':'Vehicle Maneuver'                 ,'type':'SHORT','codes':{
        1:'Straight ahead', 
        2:'Passing, overtaking',
        3:'Turning left',
        4:'Turning right', 
        5:'Turning on red', 
        6:'U-turn',
        7:'Starting in traffic',
        8:'Slow, stop – left turn',
        9:'Slow, stop – right turn',
        10:'Slow, stop – load, unload',
        11:'Slow, stop in traffic', 
        12:'Driving wrong way',
        13:'Changing lanes',
        14:'Avoiding vehicles or objects',
        15:'Skidding or control loss',        
        16:'Entering traffic lane from parking', 
        17:'Leaving traffic lane to park',
        18:'Merging',
        19:'Divering',
        20:'Enter from drive or alley',
        21:'Parked',
        22:'Parked in traffic lane',
        23:'Backing',
        24:'Driverless',
        25:'Other',
        26:'Negotiating a curve',
        99:'Unknown, NA'}}
    DIRP       = {'name':'DIRP'       ,'alias':'Vehicle Direction'      ,'type':'SHORT','codes':{
        1:'North', 
        2:'Northeast',
        3:'East',
        4:'Southeast', 
        5:'South', 
        6:'Southwest',
        7:'West',
        8:'Northwest',
        9:'Unknown'}}
    EXC_SPL    = {'name':'EXC_SPL'   ,'alias':'Exceed Speed Limit'        ,'type':'SHORT','codes':{
        0:'No',
        1:'Yes'}}
    EVNT1      = {'name':'EVNT1'     ,'alias':'Event 1'           ,'type':'SHORT','codes':{
        1:'Ran off the roadway', 
        2:'Overturn',
        3:'Fire, explosion',
        4:'Immersion', 
        5:'Jackknife', 
        6:'Cargo shift, loss',
        7:'Separation',
        8:'Downhill runaway',
        9:'Other non-collision',
        11:'Motor vehicle in traffic', 
        12:'Pedestrian',
        13:'Pedalcyclist',
        14:'Railway train',
        15:'Deer',        
        16:'Other animal', 
        17:'Falling load',
        18:'Hit parked vehicle',
        19:'Thrown or falling object',
        20:'Other object',
        21:'Crash cushion',
        22:'Guardrail face',
        23:'Guardrail end',
        24:'Concrete median barrier',
        25:'Bridge support',
        26:'Bridge end',
        27:'Bridge rail',
        28:'Bridge underside',
        29:'Traffic signal',
        30:'Light support',
        31:'Utility pole',
        32:'Delineator post',
        33:'Railroad signal, gates',
        34:'Other pole or post',
        35:'Culvert',
        36:'Curb',
        37:'Ditch, embankment',
        38:'Snowbank',
        39:'Fence',
        40:'Mailbox',
        41:'Tree or shrub',
        42:'Building, structure',
        43:'Other fixed object',
        44:'Cable barrier',
        99:'Unknown'}} 
    EVNT2      = {'name':'EVNT2'     ,'alias':'Event 2'           ,'type':'SHORT','codes':EVNT1['codes']}    
    EVNT3      = {'name':'EVNT3'     ,'alias':'Event 3'         ,'type':'SHORT','codes':EVNT1['codes']}
    LOC1       = {'name':'LOC1'      ,'alias':'Event 1 Location'        ,'type':'SHORT','codes':{
        1:'On pavement (roadway)', 
        2:'Off pavement – left',
        3:'Off pavement – right',
        4:'Intersection', 
        5:'Other', 
        9:'Unknown'}}
    LOC2       = {'name':'LOC2'      ,'alias':'Event 2 Location'        ,'type':'SHORT','codes':LOC1['codes']}          
    LOC3       = {'name':'LOC3'      ,'alias':'Event 3 Location'      ,'type':'SHORT','codes':LOC1['codes']}    
    MHE        = {'name':'MHE'       ,'alias':'Most Harmful Event'                ,'type':'SHORT','codes':EVNT1['codes']}    
    MHE_LOC    = {'name':'MHE_LOC'   ,'alias':'Most Harmful Event Location'       ,'type':'SHORT','codes':LOC1['codes']}
    MHE_NO     = {'name':'MHE_NO'    ,'alias':'Most Harmful Event Number'         ,'type':'SHORT','codes':{}}    
    FRST_CONT  = {'name':'FRST_CONT' ,'alias':'First Contact'         ,'type':'SHORT','codes':{
        0:'None', 
        1:'Front',
        2:'Right front quarter panel',
        3:'Right side center',
        4:'Right back quarter panel', 
        5:'Rear', 
        6:'Left rear quarter panel',
        7:'Left side center',
        8:'Left front quarter panel',
        9:'Roof',
        10:'Under carriage',
        11:'Total (All areas)',
        12:'Other',
        52:'Contact with Towing vehicle',
        99:'Unknown'}}
    VEHD    = {'name':'VEHD'   ,'alias':'Vehicle Defects'                   ,'type':'SHORT','codes':{
        1:'None', 
        2:'Brakes',
        3:'Steering',
        4:'Engine, motor', 
        5:'Suspension', 
        6:'Tires',
        7:'Exhaust',
        8:'Lights',
        9:'Signals',
        10:'Windows',
        11:'Restraint system', 
        12:'Wheels',
        13:'Trailer coupling',
        14:'Cargo',
        15:'Fuel system',        
        16:'Other', 
        99:'Unknown, NA'}}
    TOW        = {'name':'TOW'       ,'alias':'Vehicle Tow Status'                ,'type':'SHORT','codes':{
        0:'No',
        1:'Yes'}}
    FIRE_IND   = {'name':'FIRE_IND'  ,'alias':'Vehicle Fire'           ,'type':'SHORT','codes':{
        0:'No',
        1:'Yes'}}
    HAZMAT     = {'name':'HAZMAT'    ,'alias':'Veh Leaking Hazard Material'       ,'type':'SHORT','codes':{
        0:'No',
        1:'Yes'}}
    CV_IND    = {'name':'CV_IND'   ,'alias':'Commercial Vehicle Indicator'         ,'type':'SHORT','codes':{
        0:'No',
        1:'Yes'}}
    V_YEAR   = {'name':'V_YEAR'  ,'alias':'Vehicle Year'                      ,'type':'SHORT','codes':{}}
    V_MAKE   = {'name':'V_MAKE'  ,'alias':'Vehicle Make'                      ,'type':'TEXT','codes':{}}
    V_MODEL  = {'name':'V_MODEL' ,'alias':'Vehicle Model'                     ,'type':'TEXT','codes':{}}
    VIN11      = {'name':'VIN11'     ,'alias':'Vehicle Identification Number'     ,'type':'TEXT','codes':{}}
    
#roadway linkage

    INVENTORY  = {'name':'INVENTORY' ,'alias':'Inventory'                         ,'type':'TEXT','codes':{}}
    RID        = {'name':'RID'       ,'alias':'Route ID'                          ,'type':'TEXT','codes':{}}
    BEG_STA    = {'name':'BEG_STA'   ,'alias':'Begin Station'                     ,'type':'DOUBLE','codes':{}}        
    END_STA    = {'name':'END_STA'   ,'alias':'End Station'                       ,'type':'DOUBLE','codes':{}}    
    BMP        = {'name':'BMP'       ,'alias':'Begin Milepost'                    ,'type':'DOUBLE','codes':{}}        
    EMP        = {'name':'EMP'       ,'alias':'End Milepost'                      ,'type':'DOUBLE','codes':{}}    
    LENGTH     = {'name':'LENGTH'    ,'alias':'Length (Mile)'                     ,'type':'DOUBLE','codes':{}}    
    
    KEY_RT_APN = {'name':'KEY_RT_APN','alias':'Key Route Appurtenance No.'        ,'type':'LONG','codes':{}}
    KEY_RT_APP = {'name':'KEY_RT_APP','alias':'Key Route Appurtenance'            ,'type':'SHORT','codes':{
        0:'Mainline',
        1:'Alternate', 
        2:'Spur',
        3:'Wye',
        4:'Ramp', 
        5:'Frontage Road',
        6:'Temporary Connector',
        7:'Collector-Distributor'}}
    KEY_RT_NBR = {'name':'KEY_RT_NBR','alias':'Key Route Number'                  ,'type':'SHORT','codes':{}}    
    KEY_RT_SEG = {'name':'KEY_RT_SEG','alias':'Key Route Segment'                 ,'type':'TEXT','codes':{}}    
    KEY_RT_SUF = {'name':'KEY_RT_SUF','alias':'Key Route Suffix'                  ,'type':'TEXT','codes':{}}        
    KEY_RT_TYP = {'name':'KEY_RT_TYP' ,'alias':'Key Route Type'                   ,'type':'SHORT','codes':{
        0:'Municipal Street System (MUN)',
        1:'FA Interstate (FAI)', 
        2:'FA Primary (FAP)',
        3:'FA Secondary (FAS)',
        4:'State Bond Issue (SBI)', 
        5:'County Highway (CH)', 
        6:'House, Senate Bill (H,SB)',
        7:'Township Road (TR)',
        8:'Other Road (OR)',
        9:'FA Urban (FAU)'}}
        
    ROAD_NAME  = {'name':'ROAD_NAME' ,'alias':'Road Name'                         ,'type':'TEXT','codes':{}}    
    
    MARKED_RT  = {'name':'MARKED_RT' ,'alias':'Marked Route 1'                    ,'type':'TEXT','codes':{}}
    MARKED_RT2 = {'name':'MARKED_RT2','alias':'Marked Route 2'                    ,'type':'TEXT','codes':{}}
    MARKED_RT3 = {'name':'MARKED_RT3','alias':'Marked Route 3'                    ,'type':'TEXT','codes':{}}
    MARKED_RT4 = {'name':'MARKED_RT4','alias':'Marked Route 4'                    ,'type':'TEXT','codes':{}}
    MRK_RT_TYP = {'name':'MRK_RT_TYP','alias':'Marked Route Type 1'               ,'type':'TEXT','codes':{}}
    MRK_RT_TY2 = {'name':'MRK_RT_TY2','alias':'Marked Route Type 2'               ,'type':'TEXT','codes':{}}
    MRK_RT_TY3 = {'name':'MRK_RT_TY3','alias':'Marked Route Type 3'               ,'type':'TEXT','codes':{}}
    MRK_RT_TY4 = {'name':'MRK_RT_TY4','alias':'Marked Route Type 4'               ,'type':'TEXT','codes':{}}
    
#classification
    ACC_CNTL   = {'name':'ACC_CNTL'  ,'alias':'Access Control'                    ,'type':'SHORT','codes':{
        0:'Uncontrolled',
        1:'Partial control',
        2:'Full control'}}
    TRK_RT    = {'name':'TRK_RT'   ,'alias':'Truck Route Designation'             ,'type':'SHORT','codes':{
        0:'Unknown',
        1:'Class I',
        2:'Class II',
        3:'Class III',
        4:'Parkway'}}    
    BLT        = {'name':'BLT'       ,'alias':'Built By'                          ,'type':'TEXT','codes':{
        '0':'Unknown',
        '1':'State',
        '2':'City, town or village by agreement with State',
        '3':'State and county',
        '4':'County',
        '5':'Township or road district',
        '6':'City, town or village',
        '7':'Park district or State Division of Parks and Memorials',
        '8':'Other governmental unit',
        '9':'Private',
        'X':'Proposed or designated roads',
        'A':'Joint-county and city'}}
    #CH and CLASSIFY?

#volume
    AADT       = {'name':'AADT'      ,'alias':'AADT'                          ,'type':'LONG','codes':{}}    
    SU_VOL     = {'name':'SU_VOL'    ,'alias':'Single Unit Volume'            ,'type':'LONG','codes':{}}
    MU_VOL     = {'name':'MU_VOL'    ,'alias':'Multiple Unit Volume'          ,'type':'LONG','codes':{}}
    HCV        = {'name':'HCV'       ,'alias':'Heavy Commercial Volume'       ,'type':'LONG','codes':{}}

    AADT_EST   = {'name':'AADT_EST'  ,'alias':'AADT Establish'                ,'type':'SHORT','codes':{0:'No',1:'Yes'}}
    SU_EST     = {'name':'SU_EST'    ,'alias':'Single Unit Volume Est'        ,'type':'SHORT','codes':{0:'No',1:'Yes'}}
    MU_EST     = {'name':'MU_EST'    ,'alias':'Multiple Unit Volume Est'      ,'type':'SHORT','codes':{0:'No',1:'Yes'}}

    AADT_YR    = {'name':'AADT_YR'   ,'alias':'AADT Year'                       ,'type':'SHORT','codes':{}}
    HCV_MU_YR  = {'name':'HCV_MU_YR' ,'alias':'Single & Multi Unit Volume Year' ,'type':'SHORT','codes':{}}
        
#jurisdiction
    DIST       = {'name':'DIST'      ,'alias':'District'                          ,'type':'SHORT','codes':{}}    
#INV_CO seems redudant to line below
    COUNTY_ADJ = {'name':'COUNTY_ADJ','alias':'Adjacent County'                   ,'type':'SHORT','codes':{}}    
    COUNTY_NAM = {'name':'COUNTY_NAM','alias':'County Name'                       ,'type':'SHORT','codes':{}}        
    COUNTY_HWY = {'name':'COUNTY_HWY','alias':'County Highway Name'               ,'type':'TEXT','codes':{}}
    
    MUNI       = {'name':'MUNI'      ,'alias':'Municipality Number'               ,'type':'SHORT','codes':{}}    
    MUNI_ADJ   = {'name':'MUNI_ADJ'  ,'alias':'Adjacent Municipality'             ,'type':'SHORT','codes':{}}    
    MUNI_NAME  = {'name':'MUNI_NAME' ,'alias':'Municipality'                      ,'type':'SHORT','codes':{}}    
    
    TWP        = {'name':'TWP'       ,'alias':'Township or Road District'         ,'type':'TEXT','codes':{}}    
    TWP_ADJ    = {'name':'TWP_ADJ'   ,'alias':'Adjacent Township or Road District','type':'TEXT','codes':{}}    
    TWP_NAME   = {'name':'TWP_NAME'  ,'alias':'Township Name'                     ,'type':'TEXT','codes':{}}    
    
    MPO        = {'name':'MPO'       ,'alias':'Metropolitan Planning Org Area'    ,'type':'SHORT','codes':{
        540:'Bloomington-Normal',
        865:'Carbondale',
        990:'Champaign-Urbana',
        1051:'Chicago',
        1395:'Danville',
        1410:'Decatur',
        1435:'De Kalb-Sycamore',
        1615:'East Dubuque',
        1660:'East St. Louis',
        2915:'Kankakee',
        4590:'Peoria',
        4965:'Rockford',
        4970:'Rock Island-Moline',
        5400:'South Beloit-Rockton',
        5480:'Springfield'}}  
    
    CONG       = {'name':'CONG'      ,'alias':'Congressional District'            ,'type':'SHORT','codes':{}}
    CONG_ADJ   = {'name':'CONG_ADJ'  ,'alias':'Adjacent Congressional District'   ,'type':'SHORT','codes':{}}
    
    PL_AGY     = {'name':'PL_AGY'    ,'alias':'Planning Agency'                   ,'type':'SHORT','codes':{
        0:'NA',
        1:'Chicago', 
        2:'North Shore',
        3:'Northwest',
        4:'North Central', 
        5:'Central',    
        6:'Southwest',
        7:'South',
        8:'Lake', 
        9:'McHenry',
        10:'Kane',
        11:'DuPage',
        12:'Will'}}
    PL_AGY_ADJ = {'name':'PL_AGY_ADJ','alias':'Adjacent Planning Agency'          ,'type':'SHORT','codes':PL_AGY['codes']}
    
    REP        = {'name':'REP'       ,'alias':'Representative District'           ,'type':'SHORT','codes':{}}
    REP_ADJ    = {'name':'REP_ADJ'   ,'alias':'Adjacent Representative District'  ,'type':'SHORT','codes':{}}
    
    SPEC_SYS   = {'name':'SPEC_SYS'  ,'alias':'Special Systems'                   ,'type':'SHORT','codes':{
        0:'Does not apply',
        4:'Strategic Highway Network (StraHNet) (23 U.S.C. 103(b)(2)(c))',
        5:'National forest highway (23 U.S.C. 101(a))',
        6:'National forest development road or trail (23 U.S.C. 101(a))',
        7:'Great River Road (GRR) (23 U.S.C. 148)',
        8:'Strategic Regional Arterial (SRA)'}}    
    NON_ATTAIN = {'name':'NON_ATTAIN' ,'alias':'Nonattainment Area'               ,'type':'SHORT','codes':{
        0:'Not in an ozone nonattainment area',
        1051:'Chicago Ozone Nonattainment Area',
        1660:'St. Louis Ozone Nonattainment Area'}}    
    
    JUR_TYPE    = {'name':'JUR_TYPE'   ,'alias':'Jurisdiction Type'                 ,'type':'TEXT','codes':{
1: 'Illinois Division of Highways',
2: 'Other State Agency',
3: 'County',
4: 'Municipality',
5: 'Federal Agency',
6: 'Adjacent County',
7: 'Private (Including Toll Authorities)',
8: 'Adjacent Township or Road District',
9: 'Township or Road District',
40: 'Adjacent Municipality',
88: 'Other',
99: 'Unknown'
        }}
    JUR_1      = {'name':'JUR_1'     ,'alias':'Jurisdiction Type 1'                    ,'type':'SHORT','codes':JUR_TYPE['codes']}
    JUR_2      = {'name':'JUYR_2'    ,'alias':'Jurisdiction Type 2'                    ,'type':'SHORT','codes':JUR_TYPE['codes']}

    NHS        = {'name':'NHS'       ,'alias':'National Highway System'           ,'type':'SHORT','codes':{
        0:'Not National Highway System',
        1:'National Highway System not an NHS Connector',
        2:'NHS Connector Major Airport',
        3:'NHS Connector Major Port Facility',
        4:'NHS Connector Major Amtrak Station',
        5:'NHS Connector Major Rail & Truck Terminal',
        6:'NHS Connector Major Intercity Bus Terminal',
        7:'NHS Connector Public Transit or Multi-modal Passenger Terminal',
        8:'NHS Connector Pipeline Terminal',
        9:'NHS Connector Major Ferry Terminal'}}    
    
    URBAN      = {'name':'URBAN'     ,'alias':'Urban Area'                        ,'type':'TEXT','codes':{}}
    URB_LOC    = {'name':'URB_LOC'   ,'alias':'Urban Area'                        ,'type':'TEXT','codes':{}}

#pavement
#unsure what LOW means and the type
    CRS_LOW     = {'name':'CRS_LOW'   ,'alias':'Condition Rating ____'             ,'type':'SHORT','codes':{}}
    CRS_OPP     = {'name':'CRS_OPP'   ,'alias':'Against Condition Rating'          ,'type':'FLOAT','codes':{
9:'Awarded, new or near new',
8:'Excellent',
7:'Good',
6:'Fair',
5:'Marginal',
4:'Poor',
3:'Intolerable',
2:'Crucial',
1:'Critical',
0:'Not collected'}}
    CRS_WITH    = {'name':'CRS_WITH'  ,'alias':'With Condition Rating'             ,'type':'FLOAT','codes':CRS_OPP['codes']}
    CRS_YR      = {'name':'CRS_YR'    ,'alias':'Condition Rating Year'             ,'type':'SHORT','codes':{}}
   
    DTRESS_OPP  = {'name':'DTRESS_OPP','alias':'Against Pavement Distress'         ,'type':'TEXT','codes':{}}
    DTRESS_WTH  = {'name':'DTRESS_WTH','alias':'With Pavement Distress'            ,'type':'TEXT','codes':{}}

#unsure what LOW means and the type   
    FAULT_LOW   = {'name':'FAULT_LOW' ,'alias':'Faulting ____'                     ,'type':'SHORT','codes':{}}
    FAULT_OPP   = {'name':'FAULT_OPP' ,'alias':'Against Faulting Height'           ,'type':'DOUBLE','codes':{}}
    FAULT_WITH  = {'name':'FAULT_WITH','alias':'With Faulting Height'              ,'type':'DOUBLE','codes':{}}
   
    IRI_LOW     = {'name':'IRI_LOW'   ,'alias':'International Roughness Index ---' ,'type':'SHORT','codes':{}}
    IRI_OPP     = {'name':'IRI_OPP'   ,'alias':'Against Internatl Roughness Index' ,'type':'SHORT','codes':{}}
    IRI_WITH    = {'name':'IRI_WITH'  ,'alias':'With International Roughness Index','type':'SHORT','codes':{}}
   
#unsure what LOW means and the type
    RUT_LOW     = {'name':'RUT_LOW'   ,'alias':'Rut_____'                          ,'type':'SHORT','codes':{}}
    RUT_OPP     = {'name':'RUT_OPP'   ,'alias':'Against Rut Depth'                 ,'type':'DOUBLE','codes':{}}
    RUT_WITH    = {'name':'RUT_WITH'  ,'alias':'With Rut Depth '                   ,'type':'DOUBLE','codes':{}}

#cross section
    LANES      = {'name':'LANES'     ,'alias':'Number of Lanes'                     ,'type':'SHORT','codes':{}}
    LN_WTH     = {'name':'LN_WTH'    ,'alias':'Lane Width'                          ,'type':'SHORT','codes':{}}
    LN_SPC     = {'name':'LN_SPC'    ,'alias':'Number of Special Lanes'             ,'type':'SHORT','codes':{}}
    LN_SPC_TYP = {'name':'LN_SPC_TYP','alias':'Special Lane Type'                   ,'type':'TEXT','codes':{
'0': 'No special lane',
'1': 'Right and left turn lanes',
'2': 'Right turn lane',
'3': 'Left turn lane',
'4': 'Bi-directional turn lane',
'5': 'Reversible lane',
'6': 'Truck climbing lane',
'7': 'Ramp to ramp connectors (auxiliary)',
'8': 'Scale lane/rest area lane',
'9': 'Toll booth lane',
'A': 'Bi-directional and Right turn lanes'
        }}        
    LN_SPC_WTH = {'name':'LN_SPC_WTH'   ,'alias':'Special Lane Width'                ,'type':'SHORT','codes':{}}    
    I_SHD1_TYP = {'name':'I_SHD1_TYP','alias':'Inside Shoulder Type 1'            ,'type':'SHORT','codes':{
        0:'Not applicable', 
        1:'Earth',
        2:'Sod',
        3:'Aggregate', 
        4:'Surface treated', 
        5:'Bituminous',
        6:'Concrete-untied',
        7:'Concrete-tied', 
        8:'V gutter',
        9:'Curb and gutter'}}
    I_SHD1_WTH = {'name':'I_SHD1_WTH','alias':'Inside Shoulder Width 1'           ,'type':'SHORT','codes':{}}    
    I_SHD2_TYP = {'name':'I_SHD2_TYP','alias':'Inside Shoulder Type 2'            ,'type':'SHORT','codes':{
        0:'Not applicable', 
        1:'Earth',
        2:'Sod',
        3:'Aggregate', 
        4:'Surface treated', 
        5:'Bituminous',
        6:'Concrete-untied', 
        8:'V gutter',
        9:'Curb and gutter'}}
    I_SHD2_WTH = {'name':'I_SHD2_WTH','alias':'Inside Shoulder Width 2'           ,'type':'SHORT','codes':{}}    
    O_SHD1_TYP = {'name':'O_SHD1_TYP','alias':'Outside Shoulder Type 1'            ,'type':'SHORT','codes':I_SHD1_TYP['codes']}
    O_SHD1_WTH = {'name':'O_SHD1_WTH','alias':'Outside Shoulder Width 1'           ,'type':'SHORT','codes':{}}    
    O_SHD2_TYP = {'name':'O_SHD2_TYP','alias':'Outside Shoulder Type 2'            ,'type':'SHORT','codes':I_SHD2_TYP['codes']}
    O_SHD2_WTH = {'name':'O_SHD2_WTH','alias':'Outside Shoulder Width 2'           ,'type':'SHORT','codes':{}}    
    
    #not all code numbers included in IRIS for SURFACE1
    SURF_TYP   = {'name':'SURF_TYP'  ,'alias':'Surface Type'                      ,'type':'SHORT','codes':{
        10:'Unimproved', 
        20:'Graded and Drained',
        100:'Soil-Surfaced, Without dust palliative treatment',
        110:'Soil-Surfaced, With dust palliative (oiled)',
        200:'Gravel or Stone, Without dust palliative treatment',
        210:'Gravel or Stone, With dust palliative treatment',
        300:'Low Type Bituminous, Bituminous Surface-Treated',
        309:'Low Type Bituminous, ---',
        400:'Low Type Bituminous, Mixed Bituminous',
        410:'Low Type Bituminous, Bituminous Penetration',
        500:'High Type Bituminous (flexible base), Bituminous Surface Treated (Mixed or Penetrated)',
        501:'High Type Bituminous (flexible base), Over PCC - Rubblized - Reinforcement unknown',
        510:'High Type Bituminous (flexible base), Over PCC - Rubblized - No reinforcement',
        520:'High Type Bituminous (flexible base), Over PCC - Rubblized - Partial reinforcement',
        525:'High Type Bituminous (flexible base), Over PCC - Rubblized - With No or Partial Reinforcement - But having Hinged Joints',
        530:'High Type Bituminous (flexible base), Over PCC - Rubblized - Full reinforcement',
        540:'High Type Bituminous (flexible base), Over PCC - Rubblized - Continuous reinforcement',
        550:'High Type Bituminous (flexible base), Bituminous Concrete (other than Class I), Sheet Asphalt or Rock Asphalt',
        560:'High Type Bituminous (flexible base), Bituminous Concrete Pavement (Full-Depth)',
        565:'High Type Bituminous (flexible base), ----',
        600:'High Type Bituminous (rigid base), Over PCC - Reinforcement unknown',
        610:'High Type Bituminous (rigid base), Over PCC - No reinforcement',
        615:'High Type Bituminous (rigid base), Over PCC - No reinforcement but having short panels and dowels',
        620:'High Type Bituminous (rigid base), Over PCC - Partial reinforcement',
        625:'High Type Bituminous (rigid base), Over PCC - With No or Partial Reinforcement - But having Hinged Joints',
        630:'High Type Bituminous (rigid base), Over PCC - Full reinforcement',
        640:'High Type Bituminous (rigid base), Over PCC - Continuous reinforcement',
        650:'High Type Bituminous (rigid base), Over Brick, Block, Steel, or similar material',
        700:'Portland Cement Concrete (PCC), Reinforcement unknown',
        710:'Portland Cement Concrete (PCC), No reinforcement',
        720:'Portland Cement Concrete (PCC), Partial reinforcement',
        725:'Portland Cement Concrete (PCC), With No or Partial reinforcement but having Hinged Joints',
        730:'Portland Cement Concrete (PCC), Full reinforcement',
        740:'Portland Cement Concrete (PCC), Continuous reinforcement',
        760:'Portland Cement Concrete (PCC), Non-Reinforced over PCC - Reinforcement unknown',
        762:'Portland Cement Concrete (PCC), Reinforced over PCC - Reinforcement unknown',
        765:'Portland Cement Concrete (PCC), Non-Reinforced over PCC - No reinforcement',
        767:'Portland Cement Concrete (PCC), Reinforced over PCC - No reinforcement',
        770:'Portland Cement Concrete (PCC), Non-Reinforced over PCC - Partial reinforcement',
        772:'Portland Cement Concrete (PCC), Reinforced over PCC - Partial reinforcement',
        775:'Portland Cement Concrete (PCC), Non-Reinforced over PCC - With No or Partial reinforcement but having Hinged Joints',
        777:'Portland Cement Concrete (PCC), Reinforced over PCC - With No or Partial reinforcement but having Hinged Joints',
        780:'Portland Cement Concrete (PCC), Non-Reinforced over PCC - Full reinforcement',
        782:'Portland Cement Concrete (PCC), Reinforced over PCC - Full reinforcement',
        790:'Portland Cement Concrete (PCC), Non-Reinforced over PCC - Continuous reinforcement',
        792:'Portland Cement Concrete (PCC), Reinforced over PCC - Continuous reinforcement',
        800:'Brick, Block or Other',
        935:'Not in Dictionary',
        936:'Not in Dictionary',
        942:'Not in Dictionary',
        952:'Not in Dictionary',
        953:'Not in Dictionary',
        954:'Not in Dictionary',
        956:'Not in Dictionary',
        957:'Not in Dictionary',
        962:'Not in Dictionary',
        967:'Not in Dictionary',
        968:'Not in Dictionary',
        971:'Not in Dictionary',
        972:'Not in Dictionary',
        973:'Not in Dictionary',
        974:'Not in Dictionary',
        975:'Not in Dictionary',
        976:'Not in Dictionary',
        978:'Not in Dictionary',
        982:'Not in Dictionary',
        983:'Not in Dictionary',
        984:'Not in Dictionary',
        985:'Not in Dictionary',
        986:'Not in Dictionary',
        987:'Not in Dictionary',
        2:'Sod',
        3:'Aggregate', 
        4:'Surface treated', 
        5:'Bituminous',
        6:'Concrete-untied', 
        8:'V gutter',
        9:'Curb and gutter',
        0:'Unknown'}}
    SURF_WTH   = {'name':'SURF_WTH'  ,'alias':'Surface Width'                     ,'type':'SHORT','codes':{}}
    SURF_YR    = {'name':'SURF_YR'   ,'alias':'Surface Year'                      ,'type':'SHORT','codes':{}}
    
    MED_TYP    = {'name':'MED_TYP'   ,'alias':'Median Type'                       ,'type':'SHORT','codes':{
        0:'No median', 
        1:'Unprotected - sod, treated earth or gravel',
        2:'Curbed - any raised median except M-2.12',
        3:'Positive barrier - barriers which positively preclude vehicle crossover into opposing lanes', 
        4:'Rumble strip or chatter bar', 
        5:'Painted (excludes bi-directional turn lanes)',
        6:'High Tension Cable Median Barrier (HTC)', 
        7:'M-2.12 Traversable Median - asphalt or concrete having a low profile (typically 2 inches or less) curb'}}
    MED_WTH    = {'name':'MED_WTH'   ,'alias':'Median Width'                      ,'type':'SHORT','codes':{}}
    
#maintenance
    MNT_TYPE   = {'name':'MED_WTH'   ,'alias':'Median Width'                      ,'type':'SHORT','codes':{}}
    MNT_1      = {'name':'MNT_1'     ,'alias':'Maintenance Responsibility 1'      ,'type':'SHORT','codes':{
        1:'Illinois Division of Highways', 
        2:'Other State Agency',
        3:'County',
        4:'Municipality', 
        5:'Federal Agency', 
        6:'Adjacent County',
        7:'Private (including Toll authorities)',
        8:'Adjacent township or road district',
        9:'Township or road district',
        40:'Adjacent municipality',
        70:'Not open to public travel',
        88:'Other',
        99:'Unknown'}}
    MNT_2      = {'name':'MNT_2'     ,'alias':'Maintenance Responsibility 2'      ,'type':'SHORT','codes':MNT_1['codes']}        
    MNT_SECT   = {'name':'MNT_SECT'  ,'alias':'Maintenance Section'               ,'type':'SHORT','codes':{}}    
    MNT_DIST   = {'name':'MNT_DIST'  ,'alias':'District Maintenance'              ,'type':'SHORT','codes':{
        1:'Schaumburg',
        2:'Dixon',
        3:'Ottawa',
        4:'Peoria',
        5:'Paris',
        6:'Springfield',
        7:'Effingham',
        8:'Collinsville',
        9:'Carbondale'}}
#traffic control
    OP_1_2_WAY = {'name':'OP_1_2_WAY','alias':'1 or 2 Way Operation'              ,'type':'SHORT','codes':{
        1:'One-way',
        2:'Two-way',
        3:'One-way reversible',
        4:'Two-way reversible'}}
    PRK_LT     = {'name':'PRK_LT'    ,'alias':'Parking Restrictions Left'         ,'type':'SHORT','codes':{
        0:'Undetermined',
        1:'No parking',
        2:'Parallel parking',
        3:'Diagonal parking',
        4:'Other'}}
    PRK_RT     = {'name':'PRK_RT'    ,'alias':'Parking Restrictions Right'        ,'type':'SHORT','codes':PRK_LT['codes']}
    SP_LIM     = {'name':'SP_LIM'    ,'alias':'Speed Limit'            ,'type':'SHORT','codes':{}}        
    TOLL       = {'name':'TOLL'      ,'alias':'Toll Facility Type'                ,'type':'SHORT','codes':{
        0:'Not Toll',
        1:'State',
        2:'County',
        3:'City',
        4:'Other Public',
        5:'Private',
        6:'Illinois Toll Highway Commission'}}
    PG         = {'name':'PG'        ,'alias':'Peer Group'                        ,'type':'TEXT','codes':{
          'S1':"State – Rural Two-Lane Highway",
          'S2':'State – Rural Multilane Undivided Highway',
          'S3':'State – Rural Multilane Divided Highway',
          'S4':'State – Rural Freeway, 4 Lanes',
          'S5':'State – Rural Freeway, 6+ Lanes',
          'S6':'State – Urban Two-Lane Highway',
          'S7':'State – Urban One-Way Arterial',
          'S8':'State – Urban Multilane Undivided Highway',
          'S9':'State – Urban Multilane Divided Highway',
          'S10':'State – Urban Freeway, 4 Lanes',
          'S11':'State – Urban Freeway, 6 Lanes',
          'S12':'State – Urban Freeway, 8+ Lanes',
          'S13':'State – Private Roads',
          'S14':'State – Ramps/CD Roads',
          'S15':'State – Other',
          'L1':'Local - Rural Two-Lane Highway',
          'L2':'Local - Urban One-Way Arterial',
          'L3':'Local - Urban Two-Lane Highway',
          'L4':'Local - Urban Multilane Undivided Highway',
          'L5':'Local - Urban Multilane Divided Highway',
          'L6':'Local - Other'}}        

#other - could not do K2 or GAP        
    HPMS_SECT   = {'name':'HPMS_SECT','alias':'Highway Perform Monitoring System' ,'type':'SHORT','codes':{}}

    #Intersections
    TRAF_CONT = {'name':'TRAF_CONT','alias':'Traffic Control Type' ,'type':'TEXT','codes':{
'N': 'Not an Intersection',
'0': 'No Traffic Control Devices on any approach',
'9': 'Not determined',
'1': '1 or 2 Way Stop - Main Rt Stops – No Flashing',
'3': '1 or 2 Way Stop - Main Rt Stops - With Flashing',
'A': '1 or 2 Way Stop - X Rt Stops – No Flashing',
'B': '1 or 2 Way Stop - X Rt Stops – With flashing',
'2': 'All Way Stop - No Flashing',
'4': 'All Way Stop – With Flashing',
'5': 'Traffic signals - 2 Phase fixed',
'6': 'Traffic signals - 2 Phase actuated',
'7': 'Traffic signals - Multi-Phase fixed',
'8': 'Traffic signals - Multi-Phase actuated',
'Y': 'Inventoried Route Yields',
}}
    TCON_TYP = {'name':'TCON_TYP','alias':'Traffic Control Type' ,'type':'SHORT','codes':{
1: 'Minor Stop',
2: 'All Way Stop',
3: 'Signalized',
4: 'Yeild',
5: 'No Control Device',
6: 'Unknown'
}}
    LEG_COUNT    = {'name':'LEG_COUNT'          ,'alias':'Leg Count' ,'type':'SHORT','codes':{}}
    HAS_FLASH    = {'name':'HAS_FLASH'          ,'alias':'Has Flashers' ,'type':'SHORT','codes':{}}
    MULTI_PHASE  = {'name':'MULTI_PHASE'        ,'alias':'Is Multi Phase' ,'type':'SHORT','codes':{}}
    ACTUATED     = {'name':'ACTUATED'           ,'alias':'Is Actuated' ,'type':'SHORT','codes':{}}
    MajorRoadN   = {'name':'MajorRoadN'         ,'alias':'Major Leg Name' ,'type':'TEXT','codes':{}}
    MinorRoadN   = {'name':'MinorRoadN'         ,'alias':'Minor Leg Name' ,'type':'TEXT','codes':{}}

# Read HSIP Data
def IsNan(value):
            try:
                if math.isnan(value):
                    return(True)
            except:
                pass
            try:
                if value == 'nan':
                    return(True)
            except:
                pass
            try:
                if value == None:
                    return(True)
            except:
                pass
            return(False)
def ConvertHSIP(value,Type):
        def TryDateFormat(value,Format):
            try:
                value = str(value)
                return(datetime.strptime(value,Format))
            except:
                return(False)
        if Type == 'currency':
            if IsNan(value):
                return(0)
            try:
                value = str(value)
                #value = value.split('.')[0]
                return(float(value.replace('$','').replace(' ','').replace(',','').replace('-','0')))
            except:
                #print(Type,value)
                return(0)
        if Type == 'date':
            if IsNan(value):
                return(None)
            value = str(value)
            value = value.lstrip()
            value = value.split(',')[0]
            Res = False
            for Format in ['%m/%d/%Y','%m/%d/%Y %H:%M','%Y','%Y-%m-%d %H:%M:%S','%Y-%m-%d']:
                Res = TryDateFormat(value,Format)
                if not not Res:
                    return(Res)
            #print(Type,value)
            return(None)
        if Type == 'bool':
            if IsNan(value):
                return(None)
            value = str(value)
            value = value.rstrip()
            value = value.lstrip()
            value = str(value).lower()
            if value in ['false','no','n','0.0']:
                return(False)
            if value in ['true','yes','1.0']:
                return(True)
            #print(Type,value)
            return(None)
        if Type == 'float':
            if IsNan(value):
                return(0)
            try:
                return(float(value))
            except:
                #print(Type,value)
                return(0)
        if Type == 'int':
            if IsNan(value):
                return(0)
            try:
                return(int(value))
            except:
                #print(Type,value)
                return(0)
        if Type == 'district':
            if IsNan(value):
                return(None)
            try:
                return(int(value[-1]))
            except:
                #print(Type,value)
                return(None)
        return(value)
def ReadHSIPData(ExcelFile):
    df = pd.read_excel(ExcelFile)

    FDict = {c:{'type':'String'} for c in list(df.columns)}

    FDict['District'].update({'type':'district'})
    FDict['County'  ].update({'type':'county'})

    for field in ['Cost Est','Is Intersection','Is Segment','Is Local Project','Systematic Improvements']:
        FDict[field].update({'type':'bool'})

    for field in ['Length','Mile Station From','Mile Station To','Length NA','Total Length of Rtes.',
                  'Latitude','Longitude','Benefit Cost Ratio']:
        FDict[field].update({'type':'float'})

    for field in ['Lanes','SpeedLimit','AADTIntersection','AADTSegment','Fiscal Year','HSIP ID']:
        FDict[field].update({'type':'int'})
    
    for field in ['Estimated Project Cost','Requested HSIP Funding Amount','ApprovedAmt','FundBseAmt','FundHrrrAmt',
                  'FundHsipAmt','FundLocalAmt','Total Award Amount','HSIP AWARD AMOUNT']:
        FDict[field].update({'type':'currency'})

    for field in ['Targeted Letting Date','Letting Date','Award Date','Central HSIP Approval Date','Created','Date Submitted',
                  'Modified','Completion Date']:
        FDict[field].update({'type':'date'})

    NDF = pd.DataFrame()
    for c in list(df.columns):
        NDF[c] = [ConvertHSIP(i,FDict[c]['type']) for i in list(df[c])]
    return(NDF)
def ReadHSIPData_csv(CSVFile):
    df = pd.read_csv(CSVFile)

    FDict = {c:{'type':'String'} for c in list(df.columns)}

    FDict['District'].update({'type':'district'})
    FDict['County'  ].update({'type':'county'})

    for field in ['CostEst','IntersectionIncl','SegmentIncl','IsLocalProject','SystematicImprovements']:
        if field in FDict.keys():
            FDict[field].update({'type':'bool'})

    for field in ['Length','Mile Station From','Mile Station To','Length NA','Total Length of Rtes.',
                  'Latitude','Longitude','BenefitCostRatio']:
        if field in FDict.keys():
            FDict[field].update({'type':'float'})

    for field in ['Lanes','SpeedLimit','AADTIntersection','AADTSegment','FiscalYear','HSIPID']:
        if field in FDict.keys():
            FDict[field].update({'type':'int'})
    
    for field in ['EstimatedProjectCost','RequestedHSIPFundingAmount','ApprovedAmt','FundBseAmt','FundHrrrAmt',
                  'FundHsipAmt','FundLocalAmt','TotalAwardAmount','HSIPAWARDAMOUNT']:
        if field in FDict.keys():
            FDict[field].update({'type':'currency'})

    for field in ['TargetedLettingDate','LettingDate','AwardDate','CentralHSIPApprovalDate','Created','DateSubmitted',
                  'Modified','CompletionDate']:
        if field in FDict.keys():
            FDict[field].update({'type':'date'})
    String = ['AllSelectedImprovements','']
    NDF = pd.DataFrame()
    for c in list(df.columns):
        NDF[c] = [ConvertHSIP(i,FDict[c]['type']) for i in list(df[c])]
    return(NDF)
def CreateHSIPDataFrame(HSIPFile,Years):
    HSIP_DF = pd.DataFrame()
    if os.path.splitext(HSIPFile)[1].lower()[1:] == 'csv':
        HSIP_DF = ReadHSIPData_csv(HSIPFile)
    if os.path.splitext(HSIPFile)[1].lower()[1:] in ['xls','xlsx','xlsm']:
        HSIP_DF = ReadHSIPData(HSIPFile)
    if len(HSIP_DF) == 0:
        return HSIP_DF
    HSIP_DF = HSIP_DF.drop_duplicates(keep='first')
    droplist = []
    for i,r in HSIP_DF.iterrows():
        if not int(r['HSIP ID'])>200000000:
            droplist.append(i)
    HSIP_DF = HSIP_DF.drop(droplist)
    HSIP_DF = HSIP_DF.sort_values(by = ['HSIP ID','Central HSIP Approval Date'])
    HSIP_DF = HSIP_DF.drop_duplicates(subset = ['HSIP ID'], keep='first')
    HSIP_DF = AddBeforeAfterDates(HSIP_DF,Years)
    HSIP_DF.index = HSIP_DF['HSIP ID']
    HSIP_DF['Seg_Input'] = 0
    HSIP_DF['Int_Input'] = 0
    HSIP_DF['Miss_Loc'] = ''
    HSIP_DF['Miss_Base'] = ''
    HSIP_DF['Miss_Att'] = ''
    HSIP_DF['Miss_Crash'] = ''
    for year in Years:
        HSIP_DF['BaseRoute_' + str(year)] = 0
        HSIP_DF['BaseInt_' + str(year)] = 0
        HSIP_DF['BaseTable_' + str(year)] = 0
        HSIP_DF['SegAtt_' + str(year)] = None
        HSIP_DF['IntPoints_' + str(year)] = None
        HSIP_DF['IntTables_' + str(year)] = None
        HSIP_DF['SegCrash_' + str(year)] = None
        HSIP_DF['IntCrash_' + str(year)] = None
    for per in ['Before','After']:
        for sev in ['K','A','B']:
            for met in ['OC','EC']:
                HSIP_DF['_'.join([per[0],sev,met])] = 0.0
    HSIP_DF['EUAC'] = 0.0
    HSIP_DF['EUAB_OC'] = 0.0
    HSIP_DF['EUAB_EC'] = 0.0
    HSIP_DF['BC_OC'] = 0.0
    HSIP_DF['BC_EC'] = 0.0
    return(HSIP_DF)
def AddBeforeAfterDates(HSIP_DF,Years):
    BeforePeriod = []
    AfterPeriod  = []
    ConstPeriod  = []
    for i,hsip in HSIP_DF.iterrows():
        if hsip['Letting Date'].year>2003 and hsip['Letting Date'].year<2017 and hsip['Completion Date'].year>2003 and hsip['Completion Date'].year<2017:
            BeforePeriod.append(';'.join([str(y) for y in Years if y<hsip['Letting Date'].year]))
            AfterPeriod.append (';'.join([str(y) for y in Years if y>hsip['Completion Date'].year]))
            ConstPeriod.append (';'.join([str(y) for y in Years if y>=hsip['Letting Date'].year and y<=hsip['Completion Date'].year]))
        else:
            BeforePeriod.append('')
            AfterPeriod.append('')
            ConstPeriod.append('')
    HSIP_DF['BeforePeriod'] = BeforePeriod
    HSIP_DF['AfterPeriod'] = AfterPeriod
    HSIP_DF['ConstPeriod'] = ConstPeriod
    return(HSIP_DF)
def AddBeforeAfterDates_Contract(HSIP_DF,Years):
    BeforePeriod = []
    AfterPeriod  = []
    ConstPeriod  = []
    for i,hsip in HSIP_DF.iterrows():
        if hsip['AwardDate'].year>2003 and hsip['AwardDate'].year<2017 and hsip['CompletionDate'].year>2003 and hsip['CompletionDate'].year<2017:
            BeforePeriod.append(';'.join([str(y) for y in Years if y<hsip['AwardDate'].year]))
            AfterPeriod.append (';'.join([str(y) for y in Years if y>hsip['CompletionDate'].year]))
            ConstPeriod.append (';'.join([str(y) for y in Years if y>=hsip['AwardDate'].year and y<=hsip['CompletionDate'].year]))
        else:
            BeforePeriod.append('')
            AfterPeriod.append('')
            ConstPeriod.append('')
    HSIP_DF['BeforePeriod'] = BeforePeriod
    HSIP_DF['AfterPeriod'] = AfterPeriod
    HSIP_DF['ConstPeriod'] = ConstPeriod
    return(HSIP_DF)
def HSIP_DF_From_XML(HSIPFolder):
    def ReadHSIPXML(Filename):
        import xml.etree.cElementTree as etree
        def CleanTag(tag):
            a = tag.find('}') + 1
            t = tag[a:]
            return(t)
        def CleanText(text):
            t = text
            try:t = str(text)
            except:pass
            try:t = t.strip()
            except:pass
            try:t = t.encode('ascii', 'ignore').decode('ascii')
            except:pass
            try:t.replace('\u2019','')
            except: pass
            return(t)
        DC = {}
        context = iter(etree.iterparse(Filename, events=('start', 'end')))
        _, root = next(context) # get root element
        for event, elem in context:
            if event == 'end' and not CleanTag(elem.tag) in ["Attachment","UpdateVersionValues"]:
                DC.update({CleanTag(elem.tag):{1:CleanText(elem.text)}})
                root.clear() # preserve memory
        return(pd.DataFrame.from_dict(DC))
    def list_files(dirc,extension=''):                                                                                                  
        import os                                                                                                             
        r = []                                                                                                            
        subdirs = [x[0] for x in os.walk(dirc)]                                                                            
        for subdir in subdirs:                                                                                            
            files = os.walk(subdir).__next__()[2]                                                                             
            if (len(files) > 0):                                                                                          
                for file in files: 
                    if extension == '':
                        r.append(subdir + "/" + file)                                                                         
                    else:
                        #print(os.path.splitext(subdir + "/" + file)[1])
                        if os.path.splitext(subdir + "/" + file)[1][1:] == extension:
                        
                            r.append(subdir + "/" + file)                                                                         
        return r  
    df = pd.DataFrame()
    for xmlfn in list_files(HSIPFolder,'xml'):
        try:
            d = ReadHSIPXML(xmlfn)
            df = pd.concat([df,d], axis=0)
        except:
            print(xmlfn[len(HSIPFolder)+1:],os.path.getsize(xmlfn))
    df.drop_duplicates(subset=df.columns, keep=False)
    df = df.sort_values(by = ['HSIPID','CentralHSIPApprovalDate'])
    df = df.drop_duplicates(subset = ['HSIPID'], keep='first')
    df.index = df.HSIPID
    droplist = []
    for i,r in df.iterrows():
        try:
            if not int(r['HSIPID'])>200000000:
                droplist.append(i)
        except:
            droplist.append(i)
    df = df.drop(droplist)
    df.index = [int(i) for i in df.HSIPID]
    
    FDict = {c:{'type':'String'} for c in list(df.columns)}

    FDict['District'].update({'type':'district'})

    for field in ['IsLocalProject','SystematicImprovements']:
        FDict[field].update({'type':'bool'})

    #for field in ['Length','Mile Station From','Mile Station To','Length NA','Total Length of Rtes.',
    #              'Latitude','Longitude','Benefit Cost Ratio']:
    #    FDict[field].update({'type':'float'})

    #for field in ['Lanes','SpeedLimit','AADTIntersection','AADTSegment','Fiscal Year','HSIP ID']:
    #    FDict[field].update({'type':'int'})
    
    for field in ['ApprovedAmt','EstimatedProjectCost','FundBseAmt','FundHrrrAmt','FundHsipAmt','FundLocalAmt','FundRailAmt','RequestedHSIPFundAmt']:
        FDict[field].update({'type':'currency'})

    for field in ['AwardDate','CentralHSIPApprovalDate','CompletionDate','FiscalYear','FundingFiscalYear','LetDate','CentralHSIPDenialDate']:
        FDict[field].update({'type':'date'})

    NDF = pd.DataFrame()
    for c in list(df.columns):
        NDF[c] = [ConvertHSIP(i,FDict[c]['type']) for i in list(df[c])]
    
    NDF.index = [int(i) for i in NDF.HSIPID]
    return(NDF)
def MaxDate(DateList):
    MDate = datetime(2000,1,1)
    Out = ''
    for d in DateList:
        try:
            if d>MDate:
                if Out == '':
                    Out = d
                else:
                    if d>Out:
                        Out = d
        except:
            pass
    return(Out)
def MinDate(DateList):
    MDate = datetime(2000,1,1)
    Out = ''
    for d in DateList:
        try:
            if d>MDate:
                if Out == '':
                    Out = d
                else:
                    if d<Out:
                        Out = d
        except:
            pass
    return(Out)
def AddToList(i,DFDict):
    List = []
    for f in DFDict.keys():
        if i in DFDict[f].index and f in DFDict[f].columns:
            #try:
                if pd.DataFrame(DFDict[f].loc[i]).shape[1]==1:
                    List.append(DFDict[f].loc[i][f])
                if pd.DataFrame(DFDict[f].loc[i]).shape[1]>1:
                    List.extend(DFDict[f].loc[i][f])
            #except:
                #pass
    #if List == []:
    #    List = [pd._libs.tslib.NaTType()]
    return(List)
def FindBestComb(FY,AP,LT,AW,CM):
    df = pd.DataFrame(columns=['FYear','App','Let','Award','Comp'])
    j = 0
    for fy in FY:
        for ap in AP:
            for lt in LT:
                for aw in AW:
                    for cm in CM:
                        df.loc[j]=[pd.to_datetime(d, errors = 'coerce') for d in  [fy,ap,lt,aw,cm]]
                        j += 1
    df['Let_App'] = df['Let']-df['App']
    df['Award_Let'] = df['Award']-df['Let']
    df['Comp_Award'] = df['Comp']-df['Award']
    df = df.sort_values(by='Comp',ascending=False)
    df = df.sort_values(by='App',ascending=True)
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    for j,k in df.iterrows():
        try:
            if k['Let_App'].days>0 and k['Let_App'].days<365:
                c1.append(1)
            elif k['Let_App'].days>365:
                c1.append(2)
            else:
                c1.append(3)
        except:
            c1.append(3)

        try:
            if k['Award_Let'].days>0 and k['Award_Let'].days<90:
                c2.append(1)
            elif k['Award_Let'].days>90:
                c2.append(2)
            else:
                c2.append(3)
        except:
            c2.append(3)

        try:
            if k['Comp_Award'].days>0 and k['Comp_Award'].days<365:
                c3.append(1)
            elif k['Comp_Award'].days>365:
                c3.append(2)
            else:
                c3.append(3)
        except:
            c3.append(3)

        try:
            if k['Award'].year==k['FYear'].year:
                c4.append(1)
            elif k['Award'].year>k['FYear'].year:
                c4.append(2)
            else:
                c4.append(3)
        except:
            c4.append(3)
    df['Let_App_C'] = c1
    df['Award_Let_C'] = c2
    df['Comp_Award_C'] = c3
    df['Fy_Award_C'] = c4
    df = df.sort_values(by=['Comp_Award_C','Award_Let_C','Let_App_C','Fy_Award_C'])
    return([df.iloc[0]['FYear'],df.iloc[0]['App'],df.iloc[0]['Let'],df.iloc[0]['Award'],df.iloc[0]['Comp']])
def Ex_WPPS_HSIPID(s,HSIP_DF,XML_DF):
        s = str(s)
        l = s.split(' ')
        l = [s for s in l if s != '']
        l = [s.replace(',','') for s in l]
        for i in l:
            if len(i)==9:
                try:
                    j = int(i)
                    if j in XML_DF['HSIPID']:
                        return(j)
                except:
                    pass
            if i in list(HSIP_DF['Federal Project No.']):
                f1 = list(set(HSIP_DF[HSIP_DF['Federal Project No.'] == i].index))
                if len(f1)==1:
                    return(f1[0])
def HSIP_DF_WPPS_Ob(WPPS_Path,HSIP_DF,XML_DF):
    
    df = pd.read_excel(WPPS_Path,skiprows=2)
    df.drop_duplicates(subset=df.columns, keep=False)
    df['HSIP ID'] = [Ex_WPPS_HSIPID(s,HSIP_DF,XML_DF) for s in df['HSIP Number']]
    df.index = df['HSIP ID']
    droplist = []
    for i,r in df.iterrows():
        try:
            if not int(r['HSIP ID'])>200000000:
                droplist.append(i)
        except:
            droplist.append(i)
    df = df.drop(droplist)
    df.index = [int(i) for i in df['HSIP ID']]
    df = df.sort_index()
    
    FDict = {c:{'type':'String'} for c in list(df.columns)}

    #for field in ['Cost Est','Is Intersection','Is Segment','Is Local Project','Systematic Improvements']:
    #    FDict[field].update({'type':'bool'})

    #for field in ['Length','Mile Station From','Mile Station To','Length NA','Total Length of Rtes.',
    #              'Latitude','Longitude','Benefit Cost Ratio']:
    #    FDict[field].update({'type':'float'})

    #for field in ['Lanes','SpeedLimit','AADTIntersection','AADTSegment','Fiscal Year','HSIP ID']:
    #    FDict[field].update({'type':'int'})
    
    for field in ['AwardAmount','CompletionAmount','DetailFundingAmount']:
        FDict[field].update({'type':'currency'})

    for field in ['LettingDate','AwardDate','CompletionDate','ProgYr']:
        FDict[field].update({'type':'date'})

    NDF = pd.DataFrame()
    for c in list(df.columns):
        NDF[c] = [ConvertHSIP(i,FDict[c]['type']) for i in list(df[c])]
    
    NDF.index = [int(i) for i in NDF['HSIP ID']]
    return(NDF)
def HSIP_DF_WPPS_Pr(WPPS_Path,HSIP_DF,XML_DF):
    df = pd.read_excel(WPPS_Path,skiprows=2)
    df.drop_duplicates(subset=df.columns, keep=False)
    df['HSIP ID'] = [Ex_WPPS_HSIPID(s,HSIP_DF,XML_DF) for s in df['HSIP Number']]
    df.index = df['HSIP ID']
    droplist = []
    for i,r in df.iterrows():
        try:
            if not int(r['HSIP ID'])>200000000:
                droplist.append(i)
        except:
            droplist.append(i)
    df = df.drop(droplist)
    df.index = [int(i) for i in df['HSIP ID']]
    df = df.sort_index()
    
    FDict = {c:{'type':'String'} for c in list(df.columns)}

    #for field in ['Cost Est','Is Intersection','Is Segment','Is Local Project','Systematic Improvements']:
    #    FDict[field].update({'type':'bool'})

    #for field in ['Length','Mile Station From','Mile Station To','Length NA','Total Length of Rtes.',
    #              'Latitude','Longitude','Benefit Cost Ratio']:
    #    FDict[field].update({'type':'float'})

    #for field in ['Lanes','SpeedLimit','AADTIntersection','AADTSegment','Fiscal Year','HSIP ID']:
    #    FDict[field].update({'type':'int'})
    
    #for field in ['AwardAmount','CompletionAmount','DetailFundingAmount']:
    #    FDict[field].update({'type':'currency'})

    #for field in ['LettingDate','AwardDate','CompletionDate','ProgYr']:
    #    FDict[field].update({'type':'date'})

    NDF = pd.DataFrame()
    for c in list(df.columns):
        NDF[c] = [ConvertHSIP(i,FDict[c]['type']) for i in list(df[c])]
    
    NDF.index = [int(i) for i in NDF['HSIP ID']]
    return(NDF)
def ExtractCN(V):
        try:
            if math.isnan(V):
                return ('')
            else:
                return(str(V))
        except:
            return(str(V))
def GetContNumFromWPPS(df,i):
    if df[df.index == i].shape[0] == 1:
        return([ExtractCN(df.loc[i]['ActionNbr'])])
    else:
        return([ExtractCN(f) for f in list(df.loc[i]['ActionNbr'])])
def Joined_HSIP_DF(XML_DF,HSIP_DF,WPPS_Ob_DF,WPPS_Pr_DF):
    HSIP_Joined = pd.DataFrame(columns=['HSIPID','FedHSIPID','StateJobNum','ContNums','FiscalYear',
                                        'District','IsLocal','IsSystemic','TargetCrashType','EmphasisArea','ApprAmnt'])
    HSIP_Joined.HSIPID = XML_DF.HSIPID
    HSIP_Joined.index = HSIP_Joined.HSIPID
    HSIP_Joined = HSIP_Joined.sort_index()
    for i,r in HSIP_Joined.iterrows():
        i = int(i)
        district = XML_DF.loc[i]['District']
        local = XML_DF.loc[i]['IsLocalProject']
        systemic = XML_DF.loc[i]['SystematicImprovements']
        TCT = []
        CF = ['PredominantCrashTypeAngle','PredominantCrashTypeAnimal', 'PredominantCrashTypeFixedObj','PredominantCrashTypeHeadOn',
              'PredominantCrashTypeOtherNonCollision','PredominantCrashTypeOtherObj','PredominantCrashTypeOverturned',
              'PredominantCrashTypeParkedMotorVeh','PredominantCrashTypePedalcyclist','PredominantCrashTypePedestrian',
              'PredominantCrashTypeRearEnd','PredominantCrashTypeSideSwipeOppDir','PredominantCrashTypeSideSwipeSameDir',
              'PredominantCrashTypeTrain','PredominantCrashTypeTurning']
        for cf in CF:
            if XML_DF.loc[i][cf]=='true':
                TCT.append(cf[20:])
        targetcrash = ';'.join(TCT)
        
        ApprAmnt = 0
        try:
            ApprAmnt = int(XML_DF.loc[i]['ApprovedAmt'])
        except: pass
        if ApprAmnt==0:
            try:
                ApprAmnt = int(HSIP_DF.loc[i]['ApprovedAmt'])
            except: pass
        
        FY = XML_DF.loc[i]['FundingFiscalYear']
        try:
            FY = int(FY.year)
        except:
            pass


        EA = ['SHSPEmphasisArea-AlcoholRel','SHSPEmphasisArea-BeltsProtection','SHSPEmphasisArea-DrBehavAwar',
              'SHSPEmphasisArea-HwyRRGradeXX','SHSPEmphasisArea-InfoSys','SHSPEmphasisArea-Intersections',
              'SHSPEmphasisArea-LargeTrucks','SHSPEmphasisArea-RoadDepart','SHSPEmphasisArea-VulnerUsers','SHSPEmphasisArea-WorkZones']
        TCT = []
        for ea in EA:
            if XML_DF.loc[i][ea]=='true':
                TCT.append(ea[17:])
        eaList = ';'.join(TCT)
    
        fedid = ''
        stateid = ''
        contlist = []
        if i in HSIP_DF.index:
            fedid = HSIP_DF.loc[i]['Federal Project No.']
            stateid = HSIP_DF.loc[i]['State Job Number']
            c = ExtractCN(HSIP_DF.loc[i]['Contract No.'])
            cl = c.split(',')
            cl = [c.replace(' ','') for c in cl]
            contlist.extend(cl)
            if district == 0:
                district = HSIP_DF.loc[i]['District']
        if i in WPPS_Ob_DF.index:
            contlist.extend(GetContNumFromWPPS(WPPS_Ob_DF,i))
        if i in WPPS_Pr_DF.index:
            contlist.extend(GetContNumFromWPPS(WPPS_Pr_DF,i))
        contlist = list(set(contlist))
        contlist = [c for c in contlist if c != '']
        HSIP_Joined.set_value(str(i),'FedHSIPID',fedid)
        HSIP_Joined.set_value(str(i),'StateJobNum',stateid)
        HSIP_Joined.set_value(str(i),'ContNums',';'.join(contlist))
        HSIP_Joined.set_value(str(i),'IsLocal',local)
        HSIP_Joined.set_value(str(i),'IsSystemic',systemic)
        HSIP_Joined.set_value(str(i),'District',district)
        HSIP_Joined.set_value(str(i),'TargetCrashType',targetcrash)
        HSIP_Joined.set_value(str(i),'EmphasisArea',eaList)
        HSIP_Joined.set_value(str(i),'ApprAmnt',ApprAmnt)
        HSIP_Joined.set_value(str(i),'FiscalYear',FY)
    HSIP_Joined = pd.merge(HSIP_Joined,XML_DF[['HSIPID','AllSelectedImprovements',
                                               'ProposedImprovements-Eng','RuralOrUrban']],on='HSIPID')
    HSIP_Joined.index = HSIP_Joined.HSIPID
    HSIP_Joined = HSIP_Joined.sort_index()
    return(HSIP_Joined)
def Joined_Contract_DF(HSIP_Joined,WPPS_Ob_DF,WPPS_Pr_DF,Data_Dir,Years):
    Cont_DF = pd.DataFrame()
    cont_num = []
    cont_num_dict = {}
    for i,r in HSIP_Joined.iterrows():
        s = r.ContNums
        if s != '':
            l = s.split(';')
            for j in l:
                if j in cont_num_dict.keys():
                    cont_num_dict[j].append(i)
                else:
                    cont_num_dict.update({j:[i]})
            cont_num.extend(l)
    cont_num = list(set(cont_num))
    cont_num.sort()
    Cont_DF['ContNum'] = cont_num
    Cont_DF['HSIPIDs'] = [';'.join(cont_num_dict[c]) for c in cont_num ]
    Cont_DF.index = cont_num

    LT = []
    AW = []
    CM = []
    AWA = []
    CMA = []
    D20 = []
    D21 = []
    D22 = []
    D15 = []
    D10 = []
    D28 = []
    St = []
    for i,r in Cont_DF.iterrows():
        if i in list(WPPS_Ob_DF.ActionNbr):
            LT.append(max(list(set(WPPS_Ob_DF[WPPS_Ob_DF.ActionNbr==i]['LettingDate']))))
            AW.append(list(set(WPPS_Ob_DF[WPPS_Ob_DF.ActionNbr==i]['AwardDate']))[0])
            CM.append(list(set(WPPS_Ob_DF[WPPS_Ob_DF.ActionNbr==i]['CompletionDate']))[0])
            aw = [v for v in list(set(WPPS_Ob_DF[WPPS_Ob_DF.ActionNbr==i]['AwardAmount'])) if v>0]
            if aw == []:
                aw = 0
            else:
                aw = aw[0]
            AWA.append(aw)
            aw = [v for v in list(set(WPPS_Ob_DF[WPPS_Ob_DF.ActionNbr==i]['CompletionAmount'])) if v>0]
            if aw == []:
                aw = 0
            else:
                aw = aw[0]
            CMA.append(aw)
            D20.append(sum(list(set(WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i) & (WPPS_Ob_DF.OPPFund=='D20')]['DetailFundingAmount']))))
            D21.append(sum(list(set(WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i) & (WPPS_Ob_DF.OPPFund=='D21')]['DetailFundingAmount']))))
            D22.append(sum(list(set(WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i) & (WPPS_Ob_DF.OPPFund=='D22')]['DetailFundingAmount']))))
            D15.append(sum(list(set(WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i) & (WPPS_Ob_DF.OPPFund=='D15')]['DetailFundingAmount']))))
            D10.append(sum(list(set(WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i) & (WPPS_Ob_DF.OPPFund=='D10')]['DetailFundingAmount']))))
            D28.append(sum(list(set(WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i) & (WPPS_Ob_DF.OPPFund=='D28')]['DetailFundingAmount']))))
            if WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i)].shape[1]>1:
                t1 = [ExtractCN(t) for t in list(set(WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i)]['ActionType']))]
            else:
                t1 = ExtractCN(WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i)]['ActionType'])
        else:
            t1 = ['']
            LT.append(np.datetime64('NaT'))
            AW.append(np.datetime64('NaT'))
            CM.append(np.datetime64('NaT'))
            AWA.append(0)
            CMA.append(0)
            D20.append(0)
            D21.append(0)
            D22.append(0)
            D15.append(0)
            D10.append(0)
            D28.append(0)
        if i in list(WPPS_Pr_DF.ActionNbr):
            if WPPS_Pr_DF[(WPPS_Pr_DF.ActionNbr==i)].shape[0]>1:
                t2 = [ExtractCN(t) for t in list(set(WPPS_Pr_DF[(WPPS_Pr_DF.ActionNbr==i)]['ActionType']))]
            else:
                t2 = [ExtractCN(WPPS_Pr_DF[(WPPS_Pr_DF.ActionNbr==i)]['ActionType'].item())]
        else:
            t2 = ['']
        t1.extend(t2)
        t1 = list(set(t1))
        t = ''
        if 'O' in t1:
            t = 'O'
        elif 'C' in t1:
            t = 'C'
        St.append(t)
        
    Cont_DF['LastLettingDate'] = LT
    Cont_DF['AwardDate'] = AW
    Cont_DF['CompletionDate'] = CM
    Cont_DF['AwardAmount'] = AWA
    Cont_DF['CompletionAmount'] = CMA
    Cont_DF['D20'] = D20
    Cont_DF['D21'] = D21
    Cont_DF['D22'] = D22
    Cont_DF['D15'] = D15
    Cont_DF['D10'] = D10
    Cont_DF['D28'] = D28
    #Cont_DF['HSIPSources'] = Cont_DF['D20']+Cont_DF['D21']+Cont_DF['D22']+Cont_DF['D28']
    Cont_DF['Status'] = St

    Cont_DF = Cont_DF.sort_values(by=['CompletionDate','AwardDate'],ascending=False)    
    DownloadData = False
    if DownloadData:
        url = 'http://www.idot.illinois.gov/Assets/uploads/files/Doing-Business/Specialty-Lists/Highways/Design-&-Environment/Coded-Pay-Items/011918/CodedPayItems%20Hwy%2020180119.xls'
        file_name = os.path.join(Data_Dir, 'Pay_Item_Codebook_20180119.xls')
        urllib.request.urlretrieve(url, file_name)
        PayItem_DF1 = pd.read_excel(file_name)
        PayItem_DF1.columns = ['PAY_ITEM','DESCRIPTION','UNIT','ABBREVIATION','S']
        PayItem_DF1.index = PayItem_DF1.PAY_ITEM

        url = 'https://idot.illinois.gov/Assets/uploads/files/Doing-Business/Specialty-Lists/Highways/Design-&-Environment/Coded-Pay-Items/August-8-2017/CodedPayItemsLRS-20170804.xls'
        file_name = os.path.join(Data_Dir, 'Pay_Item_Codebook_20170804.xls')
        urllib.request.urlretrieve(url, file_name)
        PayItem_DF2 = pd.read_excel(file_name)
        PayItem_DF2.columns = ['PAY_ITEM','DESCRIPTION','UNIT','ABBREVIATION','S']
        PayItem_DF2.index = PayItem_DF2.PAY_ITEM
        nl = []
        det = []
        for i,r in Cont_DF.iterrows():
            try:
                n,df=ScrapeContract(i,[PayItem_DF1,PayItem_DF2])
                print(n)
                df.to_excel(os.path.join(Data_Dir,i+'.xls'))
                nl.append(n)
                det.append(df)
            except:
                nl.append('')
                det.append(pd.DataFrame())
        Cont_DF['PayItemDF'] = det
        Cont_DF['ContractorName'] = nl
    imps = []
    for i,r in Cont_DF.iterrows():
        t1 = ['']
        if i in list(WPPS_Pr_DF.ActionNbr):
            if WPPS_Pr_DF[(WPPS_Pr_DF.ActionNbr==i)].shape[0]>1:
                for t in list(set(WPPS_Pr_DF[(WPPS_Pr_DF.ActionNbr==i)]['Improvements'])):
                    t1.extend(t.split(','))
            else:
                t1.extend(WPPS_Pr_DF[(WPPS_Pr_DF.ActionNbr==i)]['Improvements'].item().split(','))
        if i in list(WPPS_Ob_DF.ActionNbr):
            if WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i)].shape[0]>1:
                for t in list(set(WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i)]['Improvements'])):
                    t1.extend(t.split(','))
            else:
                t1.extend(WPPS_Ob_DF[(WPPS_Ob_DF.ActionNbr==i)]['Improvements'].item().split(','))
        t1 = list(set(t1))
        t1 = [s.lstrip().rstrip() for s in t1 if not s == '']
        #print(t1)
        imps.append(list(set(t1)))
    Cont_DF['Impr_WPPS'] = [';'.join(t) for t in imps]
    Dist = []
    Local = []
    EA = []
    Sys = []
    imps = []
    CC = []  #Cost Category
    FS = []
    FSL = ['D10','D15','D20','D21','D22','D28']
    for i,r in Cont_DF.iterrows():
        dist = []
        local = False
        ea = []
        imp = []
        hsiplist = r.HSIPIDs.split(';')
        syst = False
        for hsip in hsiplist:
            if HSIP_Joined.loc[hsip]['IsSystemic']:
                syst = True
            if HSIP_Joined.loc[hsip]['IsLocal']:
                local = True
            imp.extend(HSIP_Joined.loc[hsip]['AllSelectedImprovements'].split(';'))
            dist.append(HSIP_Joined.loc[hsip]['District'])
            ea.extend(HSIP_Joined.loc[hsip]['EmphasisArea'].split(';'))
        Dist.append(';'.join(str(t) for t in list(set(dist))))
        Local.append(local)
        Sys.append(syst)
        imps.append(';'.join([s for s in list(set(imp)) if s!= '']))
        EA.append(';'.join([s for s in list(set(ea)) if s!= '']))
        if r.CompletionAmount<100000:
            CC.append('Low')
        else:
            if r.CompletionAmount<1000000:
                CC.append('Mid')
            else:
                CC.append('High')
        df = pd.DataFrame([r[c] for c in FSL],FSL)
        fs = list(df[df[0]==max(df[0])].index)[0]
        if max(df[0])==0:
            fs = ''
        FS.append(fs)
    Cont_DF['District'] = Dist
    #Cont_DF['IsLocal'] = Local
    Cont_DF['EA'] = EA
    Cont_DF['IsSystemic'] = Sys
    Cont_DF['Imp_HSIP'] = imps
    Cont_DF['CostCat'] = CC
    Cont_DF['FundSource'] = FS
    Cont_DF['Duration'] = Cont_DF.CompletionDate- Cont_DF.AwardDate
    Cont_DF = AddBeforeAfterDates_Contract(Cont_DF,Years)

    return(Cont_DF)
def ScrapeContract(cont,PayItem_DFList):
    from urllib.request import urlopen
    base_url = 'http://neonweba.cmcf.state.il.us:8080/dot/dtgbcmna?contract='
    html = urlopen(base_url+cont).read().decode('utf-8')
    l = pd.read_html(html)
    if len(l)==2:
        df1,df2 = l
    else:
        print(l[0].loc[2].item())
    ContractorName = df1.iloc[3].item()[18:]
    df2.columns = ['PAY_ITEM','UNIT_PRICE','AWARDED_QTY','AWARDED_AMT','ADJUSTED_QTY','ADJUSTED_AMT','COMPLETED_QTY','COMPLETED_AMT']
    for i,r in df2.iterrows():
        for c in ['UNIT_PRICE','AWARDED_QTY','AWARDED_AMT','ADJUSTED_QTY','ADJUSTED_AMT','COMPLETED_QTY','COMPLETED_AMT']:
            s = str(r[c])
            if '-' in s:
                s = s.replace('-','')
                v = float(s) * (-1)
            else:
                v = float(s)
            df2.set_value(i,c,v)
    l = []
    for i,r in df2.iterrows():
        Found = False
        for PayDF in PayItem_DFList:
            if r.PAY_ITEM in PayDF.index:
                l.append(PayDF.loc[r.PAY_ITEM]['DESCRIPTION'])
                Found = True
                break
        if not Found:
            l.append('')
    df2['PAY_ITEM_CODE'] = l
    return([ContractorName,df2])
def Joined_Loc_DF(WPPS_Pr_DF):
    Loc_DF = pd.DataFrame(columns=['Year','INVENTORY','BEG_STA','END_STA','ContNum'])
    Year = []
    INVENTORY = []
    BEG_STA = []
    END_STA = []
    ContNum = []
    WPPS_Num = []
    for i,r in WPPS_Pr_DF.iterrows():
        try:
            year = int(r.ProgYear)
            inv = str(r.GISRouteKey)
            beg = float(r.BeginStatn)
            end = float(r.EndStatn)
            cont = str(r.ActionNbr)
            wppsnum = str(r.PPSNbr)
            if len(inv) == 17 and not math.isnan(beg) and not math.isnan(end) and len(cont)>3:
                Year.append(year)
                INVENTORY.append(inv)
                BEG_STA.append(beg)
                END_STA.append(end)
                ContNum.append(cont)
                WPPS_Num.append(wppsnum)
        except:
            pass
    Loc_DF['Year'] = Year
    Loc_DF['INVENTORY'] = INVENTORY
    Loc_DF['BEG_STA'] = BEG_STA
    Loc_DF['END_STA'] = END_STA
    Loc_DF['ContNum'] = ContNum
    Loc_DF['Length'] = Loc_DF['END_STA'] - Loc_DF['BEG_STA']
    Loc_DF['PPSNbr'] = WPPS_Num
    Loc_DF = Loc_DF.drop_duplicates(subset=['Year', 'INVENTORY', 'BEG_STA', 'END_STA', 'ContNum'])
    return(Loc_DF)
def GeocodeWPPS(DF,GDB,Output,IRIS_Route):
    df = DF[['Year','INVENTORY','BEG_STA','END_STA','ContNum','HSIPIDs']]
    Main_GDB = GDB
    MergeList = []
    for year in list(set(df.Year)):
        df1 = df[df.Year==year]
        df1 = df1.sort_values(by=['INVENTORY','BEG_STA'])
        Table_FN = Main_GDB + '\\WPPS_'+str(year)
        SegFC = Main_GDB + '\\WPPS_Seg_' + str(year)
        arcpy.Delete_management(Table_FN)
        arcpy.CreateTable_management(out_path=Main_GDB,out_name=os.path.basename(Table_FN))
        arcpy.AddField_management(in_table=Table_FN,field_name='INVENTORY',field_type='Text',field_length=17)
        arcpy.AddField_management(in_table=Table_FN,field_name='BEG_STA',field_type='Double',field_length=10)
        arcpy.AddField_management(in_table=Table_FN,field_name='END_STA',field_type='Double',field_length=10)
        arcpy.AddField_management(in_table=Table_FN,field_name='ContNum',field_type='Text',field_length=10)
        arcpy.AddField_management(in_table=Table_FN,field_name='HSIPIDs',field_type='Text',field_length=300)
        uc= arcpy.InsertCursor(Table_FN)
        for i,r in df1.iterrows():
            row = uc.newRow()
            #print(r.INVENTORY)
            row.setValue('INVENTORY',r.INVENTORY)
            row.setValue('BEG_STA',r.BEG_STA)
            row.setValue('END_STA',r.END_STA)
            row.setValue('ContNum',r.ContNum)
            row.setValue('HSIPIDs',r.HSIPIDs)
            uc.insertRow(row)
        del uc
        arcpy.Delete_management(SegFC)
        network.CreateRouteEventLayer(AttTable=Table_FN,Sites_Routes=IRIS_Route[year],
                                             BMP='BEG_STA',EMP='END_STA',Fields=['ContNum'],
                                             Output=SegFC,RouteID='INVENTORY')
        arcpy.Delete_management(Table_FN)
        MergeList.append(SegFC)
    SegFC = Output
    arcpy.Delete_management(SegFC)
    arcpy.Merge_management(inputs=MergeList,output=SegFC)
    arcpy.DeleteField_management(SegFC,['BEG_STA','END_STA'])
    for fc in MergeList:
        arcpy.Delete_management(fc)
    return(Output)
def GeocodeContracts(DF,GDB,IntOut,SegOut):
    df = DF[['IntLoc','SegLoc','INVENTORY','ContNum','HSIPIDs','LocSrc']]
    Main_GDB = GDB
    df1 = df[[(not b) for b in df.IntLoc.isnull()]]
    Int_FC = Main_GDB + '\\' + IntOut
    arcpy.Delete_management(Int_FC)
    arcpy.management.CreateFeatureclass(out_path=Main_GDB,out_name=os.path.basename(Int_FC),geometry_type='POINT',spatial_reference=common.NAD1983IL)
    arcpy.AddField_management(in_table=Int_FC,field_name='ContNum',field_type='Text',field_length=10)
    arcpy.AddField_management(in_table=Int_FC,field_name='HSIPIDs',field_type='Text',field_length=300)
    arcpy.AddField_management(in_table=Int_FC,field_name='LocSrc',field_type='Text',field_length=10)
    uc= arcpy.InsertCursor(Int_FC)
    for i,r in df1.iterrows():
        for pnt in r.IntLoc:
            row = uc.newRow()
            #print(r.INVENTORY)
            row.setValue('ContNum',r.ContNum)
            row.setValue('HSIPIDs',r.HSIPIDs)
            row.setValue('LocSrc',r.LocSrc)
            row.Shape = pnt
            uc.insertRow(row)
    del uc

    df1 = df[[(not b) for b in df.SegLoc.isnull()]]
    Seg_FC = Main_GDB + '\\' + SegOut
    arcpy.Delete_management(Seg_FC)
    arcpy.management.CreateFeatureclass(out_path=Main_GDB,out_name=os.path.basename(Seg_FC),geometry_type='POLYLINE',spatial_reference=common.NAD1983IL,has_m='ENABLED')
    arcpy.AddField_management(in_table=Seg_FC,field_name='INVENTORY',field_type='Text',field_length=17)
    arcpy.AddField_management(in_table=Seg_FC,field_name='BEG_STA',field_type='Double',field_length=10)
    arcpy.AddField_management(in_table=Seg_FC,field_name='END_STA',field_type='Double',field_length=10)
    arcpy.AddField_management(in_table=Seg_FC,field_name='ContNum',field_type='Text',field_length=10)
    arcpy.AddField_management(in_table=Seg_FC,field_name='HSIPIDs',field_type='Text',field_length=300)
    arcpy.AddField_management(in_table=Seg_FC,field_name='LocSrc',field_type='Text',field_length=10)
    uc= arcpy.InsertCursor(Seg_FC)
    for i,r in df1.iterrows():
        for pl,inv in zip(r.SegLoc,r.INVENTORY):
            row = uc.newRow()
            row.setValue('INVENTORY',inv)
            row.Shape = pl
            row.setValue('BEG_STA',pl.firstPoint.M)
            row.setValue('END_STA',pl.lastPoint.M)
            row.setValue('ContNum',r.ContNum)
            row.setValue('HSIPIDs',r.HSIPIDs)
            uc.insertRow(row)
    del uc
def AddPayItemTabletoGDB(Main_GDB,XLSList,Table_FN):
    PayDF = pd.DataFrame()
    for xls in XLSList:
        df = pd.read_excel(xls)
        df['ContNum'] = os.path.basename(xls).split('.')[0]
        PayDF = pd.concat([PayDF,df])
    PayDF = PayDF.replace(float('NaN'),'')
    PayDF = PayDF.sort_values(by=['ContNum','COMPLETED_AMT'],ascending=False)
    arcpy.Delete_management(Table_FN)
    arcpy.CreateTable_management(out_path=Main_GDB,out_name=os.path.basename(Table_FN))
    arcpy.AddField_management(in_table=Table_FN,field_name='ContNum',field_type='Text',field_length=10)
    arcpy.AddField_management(in_table=Table_FN,field_name='PAY_ITEM',field_type='Text',field_length=20)
    arcpy.AddField_management(in_table=Table_FN,field_name='Name',field_type='Text',field_length=400)
    arcpy.AddField_management(in_table=Table_FN,field_name='UNIT_PRICE',field_type='Double')
    arcpy.AddField_management(in_table=Table_FN,field_name='AWARDED_QTY',field_type='Double')
    arcpy.AddField_management(in_table=Table_FN,field_name='AWARDED_AMT',field_type='Double')
    arcpy.AddField_management(in_table=Table_FN,field_name='ADJUSTED_QTY',field_type='Double')
    arcpy.AddField_management(in_table=Table_FN,field_name='ADJUSTED_AMT',field_type='Double')
    arcpy.AddField_management(in_table=Table_FN,field_name='COMPLETED_QTY',field_type='Double')
    arcpy.AddField_management(in_table=Table_FN,field_name='COMPLETED_AMT',field_type='Double')
    uc= arcpy.InsertCursor(Table_FN)
    for i,r in PayDF.iterrows():
        row = uc.newRow()
        row.setValue('ContNum',r.ContNum)
        row.setValue('PAY_ITEM',r.PAY_ITEM)
        row.setValue('Name',r.PAY_ITEM_CODE)
        row.setValue('UNIT_PRICE',r.UNIT_PRICE)
        row.setValue('AWARDED_QTY',r.AWARDED_QTY)
        row.setValue('AWARDED_AMT',r.AWARDED_AMT)
        row.setValue('ADJUSTED_QTY',r.ADJUSTED_QTY)
        row.setValue('ADJUSTED_AMT',r.ADJUSTED_AMT)
        row.setValue('COMPLETED_QTY',r.COMPLETED_QTY)
        row.setValue('COMPLETED_AMT',r.COMPLETED_AMT)
        uc.insertRow(row)
    del uc
    return(Table_FN)
def AddHSIPTableToGDB(Main_GDB,HSIP_Joined,Table_FN):
    arcpy.Delete_management(Table_FN)
    arcpy.CreateTable_management(out_path=Main_GDB,out_name=os.path.basename(Table_FN))
    arcpy.AddField_management(in_table=Table_FN,field_name='HSIPID',field_type='Text',field_length=20)
    arcpy.AddField_management(in_table=Table_FN,field_name='FedHSIPID',field_type='Text',field_length=30)
    arcpy.AddField_management(in_table=Table_FN,field_name='StateJobNum',field_type='Text',field_length=40)
    arcpy.AddField_management(in_table=Table_FN,field_name='ContNums',field_type='Text',field_length=80)
    arcpy.AddField_management(in_table=Table_FN,field_name='District',field_type='Single')
    arcpy.AddField_management(in_table=Table_FN,field_name='IsLocal',field_type='Single')
    arcpy.AddField_management(in_table=Table_FN,field_name='IsSystemic',field_type='Single')
    arcpy.AddField_management(in_table=Table_FN,field_name='TargetCrashType',field_type='Text',field_length=200)
    arcpy.AddField_management(in_table=Table_FN,field_name='EmphasisArea',field_type='Text',field_length=100)
    arcpy.AddField_management(in_table=Table_FN,field_name='AllSelectedImprovements',field_type='Text',field_length=400)
    arcpy.AddField_management(in_table=Table_FN,field_name='ProposedImprovements',field_type='Text',field_length=200)
    arcpy.AddField_management(in_table=Table_FN,field_name='Urban',field_type='Single')
    uc= arcpy.InsertCursor(Table_FN)
    for i,r in HSIP_Joined.iterrows():
        row = uc.newRow()
        row.setValue('HSIPID',r.HSIPID)
        row.setValue('FedHSIPID',r.FedHSIPID)
        row.setValue('StateJobNum',r.StateJobNum)
        row.setValue('ContNums',r.ContNums)
        row.setValue('District',int(r.District))
        row.setValue('IsLocal',{True:1,False:0}[r.IsLocal])
        row.setValue('IsSystemic',{True:1,False:0}[r.IsSystemic])
        row.setValue('TargetCrashType',r.TargetCrashType)
        row.setValue('EmphasisArea',r.EmphasisArea)
        row.setValue('AllSelectedImprovements',r.AllSelectedImprovements)
        row.setValue('ProposedImprovements',r['ProposedImprovements-Eng'])
        row.setValue('Urban',{'true':1,'false':0,'':0,'None':0}[r.RuralOrUrban])
        uc.insertRow(row)
    del uc
    return(Table_FN)
def AddContractTableToGDB(Main_GDB,Cont_DF,Table_FN):
    arcpy.Delete_management(Table_FN)
    arcpy.CreateTable_management(out_path=Main_GDB,out_name=os.path.basename(Table_FN))
    arcpy.AddField_management(in_table=Table_FN,field_name='ContNum',field_type='Text',field_length=15)
    arcpy.AddField_management(in_table=Table_FN,field_name='HSIPIDs',field_type='Text',field_length=300)
    arcpy.AddField_management(in_table=Table_FN,field_name='District',field_type='Text',field_length=10)
    arcpy.AddField_management(in_table=Table_FN,field_name='Status',field_type='Text',field_length=1)
    arcpy.AddField_management(in_table=Table_FN,field_name='LastLettingDate',field_type='Date')
    arcpy.AddField_management(in_table=Table_FN,field_name='AwardDate',field_type='Date')
    arcpy.AddField_management(in_table=Table_FN,field_name='DurationDays',field_type='Long')
    arcpy.AddField_management(in_table=Table_FN,field_name='CompletionDate',field_type='Date')
    arcpy.AddField_management(in_table=Table_FN,field_name='AwardAmount',field_type='Long')
    arcpy.AddField_management(in_table=Table_FN,field_name='CompletionAmount',field_type='Long')
    arcpy.AddField_management(in_table=Table_FN,field_name='D20',field_type='Long')
    arcpy.AddField_management(in_table=Table_FN,field_name='D21',field_type='Long')
    arcpy.AddField_management(in_table=Table_FN,field_name='D22',field_type='Long')
    arcpy.AddField_management(in_table=Table_FN,field_name='D10',field_type='Long')
    arcpy.AddField_management(in_table=Table_FN,field_name='D15',field_type='Long')
    arcpy.AddField_management(in_table=Table_FN,field_name='D28',field_type='Long')
    arcpy.AddField_management(in_table=Table_FN,field_name='FundSource',field_type='Text',field_length=10)
    arcpy.AddField_management(in_table=Table_FN,field_name='CostCat',field_type='Text',field_length=10)
    arcpy.AddField_management(in_table=Table_FN,field_name='IsSystemic',field_type='Single')
    arcpy.AddField_management(in_table=Table_FN,field_name='EA',field_type='Text',field_length=150)
    arcpy.AddField_management(in_table=Table_FN,field_name='Impr_WPPS',field_type='Text',field_length=200)
    arcpy.AddField_management(in_table=Table_FN,field_name='Imp_HSIP',field_type='Text',field_length=1200)
    uc= arcpy.InsertCursor(Table_FN)
    for i,r in Cont_DF.iterrows():
        row = uc.newRow()
        row.setValue('ContNum',r.ContNum)
        row.setValue('HSIPIDs',r.HSIPIDs)
        row.setValue('LastLettingDate',r.LastLettingDate)
        row.setValue('AwardDate',r.AwardDate)
        row.setValue('CompletionDate',r.CompletionDate)
        row.setValue('AwardAmount',r.AwardAmount)
        row.setValue('CompletionAmount',r.CompletionAmount)
        row.setValue('D20',r.D20)
        row.setValue('D21',r.D21)
        row.setValue('D22',r.D22)
        row.setValue('D10',r.D10)
        row.setValue('D15',r.D15)
        row.setValue('D28',r.D28)
        row.setValue('Status',r.Status)
        row.setValue('Impr_WPPS',r.Impr_WPPS)
        row.setValue('District',r.District)
        row.setValue('EA',r.EA)
        row.setValue('IsSystemic',{True:1,False:0}[r.IsSystemic])
        row.setValue('Imp_HSIP',r.Imp_HSIP)
        row.setValue('CostCat',{'Low':1,'Mid':2,'High':3}[r.CostCat])
        row.setValue('FundSource',r.FundSource)
        d = r.Duration.days
        if math.isnan(d):
            d = 0
        row.setValue('DurationDays',d)
        uc.insertRow(row)
    del uc
    return(Table_FN)
def DownloadPayItems():
    import urllib
    url = 'http://www.idot.illinois.gov/Assets/uploads/files/Doing-Business/Specialty-Lists/Highways/Design-&-Environment/Coded-Pay-Items/011918/CodedPayItems%20Hwy%2020180119.xls'
    file_name = 'Temp{}.xlsx'.format(strftime("%Y%m%d%H%M%S"))
    urllib.request.urlretrieve(url, file_name)
    PayItem_DF1 = pd.read_excel(file_name)
    os.remove(file_name)
    PayItem_DF1.columns = ['PAY_ITEM','DESCRIPTION','UNIT','ABBREVIATION','S']
    PayItem_DF1.index = PayItem_DF1.PAY_ITEM

    url = 'https://idot.illinois.gov/Assets/uploads/files/Doing-Business/Specialty-Lists/Highways/Design-&-Environment/Coded-Pay-Items/August-8-2017/CodedPayItemsLRS-20170804.xls'
    file_name = 'Temp{}.xlsx'.format(strftime("%Y%m%d%H%M%S"))
    urllib.request.urlretrieve(url, file_name)
    PayItem_DF2 = pd.read_excel(file_name)
    os.remove(file_name)
    PayItem_DF2.columns = ['PAY_ITEM','DESCRIPTION','UNIT','ABBREVIATION','S']
    PayItem_DF2.index = PayItem_DF2.PAY_ITEM
    return([PayItem_DF1,PayItem_DF2])
def ScrapeContractList(ContractList):
    payL = DownloadPayItems()
    RS_Cont_DF = pd.DataFrame()
    for c in ContractList:
        L = ScrapeContract(cont=c,PayItem_DFList=payL)
        df = L[1]
        df['ContNum'] = c
        df['Contractor'] = L[0]
        RS_Cont_DF = pd.concat([RS_Cont_DF,df])
    return(RS_Cont_DF)
# HSIP Spatial Analysis
def FindPG_Old():
    IRIS = r'C:\Users\mr068144\Downloads\IRIS\HWY2015_CH2M_Editions.mdb\HWY2015_CH2M_20180213'
    arcpy.AddField_management(IRIS,'PGMahdi','TEXT')
    for year in [2015]:
        #IRIS = os.path.join(IRISPath,'HWY'+str(year)+'.shp')
        PGDict = {}
        uc = arcpy.UpdateCursor(IRIS)
        for r in uc:
            OID = r.getValue('OBJECTID')
            JUR_TYPE   = r.getValue('JUR_TYPE')
            FUNC_CLASS     = r.getValue('FUNC_CLASS')
            URBAN      = r.getValue('URBAN')
            KEY_RT_TYP = r.getValue('KEY_RT_TYP')
            LANES        = r.getValue('LANES')
            LNS        = r.getValue('LNS')
            KEY_RT_APP = r.getValue('KEY_RT_APP')
            OP_1_2_WAY = r.getValue('OP_1_2_WAY')
            MED_TYP    = r.getValue('MED_TYP')
            MARKED_RT  = r.getValue('MARKED_RT')
            MARKED_RT2  = r.getValue('MARKED_RT2')
            MARKED_RT3  = r.getValue('MARKED_RT3')
            MARKED_RT4  = r.getValue('MARKED_RT4')
            FC         = FUNC_CLASS
            if JUR_TYPE in ['1','7']:
                PG = []
                if FUNC_CLASS != '1' and LANES == 2 and URBAN == '0000' and JUR_TYPE == '1' and KEY_RT_APP != '7' and KEY_RT_APP != '4':
                    PG.append(1)
                if FUNC_CLASS >= '3' and LANES > 2 and URBAN == '0000' and JUR_TYPE == '1' and MED_TYP == 0 and KEY_RT_APP != '7' and KEY_RT_APP != '4':
                    PG.append(2)
                if FUNC_CLASS >= '3' and LANES > 2 and URBAN == '0000' and JUR_TYPE == '1' and MED_TYP != 0 and KEY_RT_APP != '7' and KEY_RT_APP != '4':
                    PG.append(3)
                if FUNC_CLASS <= '2' and (LANES == 3 or LANES == 4) and URBAN == '0000' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(4)
                if FUNC_CLASS <= '2' and URBAN == '0000' and LANES >= 6 and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(5)
                if (FUNC_CLASS <= '4' or FUNC_CLASS == '7') and LANES <= 2 and URBAN != '0000' and OP_1_2_WAY == '2' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(6)
                if (FUNC_CLASS <= '4' or FUNC_CLASS == '7') and URBAN != '0000' and OP_1_2_WAY == '1' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(7)
                if (FUNC_CLASS == '3' or FUNC_CLASS == '4' or FUNC_CLASS == '7') and LANES > 2 and MED_TYP == 0 and URBAN != '0000' and OP_1_2_WAY == '2' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(8)
                if (FUNC_CLASS == '3' or FUNC_CLASS == '4' or FUNC_CLASS == '7') and LANES > 2 and MED_TYP != 0 and URBAN != '0000' and OP_1_2_WAY == '2' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(9)
                if FUNC_CLASS <= '2' and URBAN != '0000' and (LANES == 3 or LANES == 4) and OP_1_2_WAY == '2' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(10)
                if FUNC_CLASS <= '2' and URBAN != '0000' and (LANES == 5 or LANES == 6) and OP_1_2_WAY == '2' and JUR_TYPE == '1' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(11)
                if FC <= '20' and LNS >= 7 and URBAN != '0000' and JUR_TYPE == '1' and OP_1_2_WAY == '2' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(12)
                if JUR_TYPE == '7' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(13)
                if (JUR_TYPE == '1' or JUR_TYPE == '7') and (KEY_RT_APP == '4' or KEY_RT_APP == '7'):
                    PG.append(14)
                if PG==[]:
                    PG.append(15)
                PG = ['S' + str(i) for i in PG]
            else:
                PG = []
                if LANES == 2 and URBAN == '0000' and KEY_RT_APP != '4' and KEY_RT_APP != '7' and OP_1_2_WAY == '2' and MARKED_RT =='' and MARKED_RT2 == '' and MARKED_RT3 == '' and MARKED_RT4 == '':
                    PG.append(1)
                if URBAN != '0000' and KEY_RT_APP != '4' and KEY_RT_APP != '7' and OP_1_2_WAY == '1':
                    PG.append(2)
                if LANES <= 2 and URBAN != '0000' and KEY_RT_APP != '4' and KEY_RT_APP != '7' and OP_1_2_WAY == '2' and MARKED_RT =='' and MARKED_RT2 == '' and MARKED_RT3 == '' and MARKED_RT4 == '':
                    PG.append(3)
                if LANES > 2 and MED_TYP == 0 and URBAN != '0000' and OP_1_2_WAY == '2' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(4)
                if LANES > 2 and MED_TYP != 0 and URBAN != '0000' and OP_1_2_WAY == '2' and KEY_RT_APP != '4' and KEY_RT_APP != '7':
                    PG.append(5)
                if PG == []:
                    PG.append(6)
                PG = ['L' + str(i) for i in PG]
            PGDict.update({OID:PG})
            r.setValue('PGMahdi',PGConv[PG[0]])
            uc.updateRow(r)
    del uc,r
def FindPG(JUR_TYPE,URBAN,KEY_RT_APP,FCNAME,LNS,MED_TYP,OP_1_2_WAY):
    JUR_TYPE = int(JUR_TYPE)
    URBAN = str(URBAN)
    KEY_RT_APP = int(KEY_RT_APP)
    FCNAME = str(FCNAME)
    LNS = int(LNS)
    MED_TYP = int(MED_TYP)
    OP_1_2_WAY = int(OP_1_2_WAY)
    
    if JUR_TYPE in [1]:
        s1 = 'State'
    elif JUR_TYPE in [7]:
        s1 = 'Private'
    else:
        s1 = 'Local'
        
    if URBAN == '0000':
        s2 = 'Rural'
    else:
        s2 = 'Urban'
        
    if FCNAME in ['Interstate','Freeway and Expressway','Freeway and Expressway (Urban)']:
        s3 = 'Freeway'
    else:
        s3 = 'non-Freeway'
    
    if MED_TYP in [0]:
        s4 = 'undivided'
    else:
        s4 = 'divided'
    
    if KEY_RT_APP in [4,7]:
        s5 = 'RampCD'
    else:
        s5 = 'nonRampCD'
    
    if OP_1_2_WAY == 1:
        s6 = 'oneway'
    else:
        s6 = 'twoway'
    
    PG = 0
    if s1 == 'State':
        if s5 == 'nonRampCD':
            if s2 == 'Rural':
                if s3 == 'non-Freeway':
                    if LNS == 2:
                        PG = 'S1'
                    if LNS>2:
                        if s4 == 'undivided':
                            PG = 'S2'
                        else:
                            PG = 'S3'
                else: #Freeway
                    if LNS in [3,4]:
                        PG = 'S4'
                    if LNS>5:
                        PG = 'S5'
            else: #Urban
                if s6=='oneway':
                    PG = 'S7'
                else: #Twoway
                    if s3 == 'non-Freeway':
                        if LNS==2:
                            PG = 'S6'
                        if LNS>2:
                            if s4 == 'undivided':
                                PG = 'S8'
                            else:
                                PG = 'S9'
                    else: #Freeway
                        if LNS in [3,4]:
                            PG = 'S10'
                        if LNS in [5,6]:
                            PG = 'S11'
                        if LNS>=7:
                            PG = 'S12'
        else: #RampCD
            PG = 'S14'
    if s1 == 'Private':
        if s5 == 'nonRampCD':
            PG = 'S13'
        else: #RampCD
            PG = 'S14'
    if s1 in ['State','Private'] and PG == 0:
        PG = 'S15'
    if s1 == 'Local':
        if s5 == 'nonRampCD':
            if s2 == 'Rural':
                if LNS == 2 and s6 == 'twoway':
                    PG = 'L1'
            else: #Urban
                if s6 == 'oneway':
                    PG = 'L2'
                else: #twoway
                    if LNS <= 2:
                        PG = 'L3'
                    else:
                        if s4 == 'undivided':
                            PG = 'L4'
                        else:
                            PG = 'L5'
        if PG == 0:
            PG = 'L6'
    return(PG)
def FindPG_Cleaned(JUR_TYPE,URBAN,KEY_RT_APP,FCNAME,LNS,MED_TYP,OP_1_2_WAY):
    try:
        JUR_TYPE = int(JUR_TYPE)
        URBAN = int(URBAN)
        KEY_RT_APP = int(KEY_RT_APP)
        FCNAME = int(FCNAME)
        LNS = int(LNS)
        MED_TYP = int(MED_TYP)
        OP_1_2_WAY = int(OP_1_2_WAY)
    except:
        return()
    if JUR_TYPE in [1]:
        s1 = 'State'
    elif JUR_TYPE in [7]:
        s1 = 'Private'
    else:
        s1 = 'Local'
        
    if URBAN == 0:
        s2 = 'Rural'
    else:
        s2 = 'Urban'
        
    if FCNAME in [1,2]:
        s3 = 'Freeway'
    else:
        s3 = 'non-Freeway'
    
    if MED_TYP in [0]:
        s4 = 'undivided'
    else:
        s4 = 'divided'
    
    if KEY_RT_APP in [4,7]:
        s5 = 'RampCD'
    else:
        s5 = 'nonRampCD'
    
    if OP_1_2_WAY == 1:
        s6 = 'oneway'
    else:
        s6 = 'twoway'
    
    PG = 0
    if s1 == 'State':
        if s5 == 'nonRampCD':
            if s2 == 'Rural':
                if s3 == 'non-Freeway':
                    if LNS == 2:
                        PG = 'S1'
                    if LNS>2:
                        if s4 == 'undivided':
                            PG = 'S2'
                        else:
                            PG = 'S3'
                else: #Freeway
                    if LNS in [3,4]:
                        PG = 'S4'
                    if LNS>5:
                        PG = 'S5'
            else: #Urban
                if s6=='oneway':
                    PG = 'S7'
                else: #Twoway
                    if s3 == 'non-Freeway':
                        if LNS==2:
                            PG = 'S6'
                        if LNS>2:
                            if s4 == 'undivided':
                                PG = 'S8'
                            else:
                                PG = 'S9'
                    else: #Freeway
                        if LNS in [3,4]:
                            PG = 'S10'
                        if LNS in [5,6]:
                            PG = 'S11'
                        if LNS>=7:
                            PG = 'S12'
        else: #RampCD
            PG = 'S14'
    if s1 == 'Private':
        if s5 == 'nonRampCD':
            PG = 'S13'
        else: #RampCD
            PG = 'S14'
    if s1 in ['State','Private'] and PG == 0:
        PG = 'S15'
    if s1 == 'Local':
        if s5 == 'nonRampCD':
            if s2 == 'Rural':
                if LNS == 2 and s6 == 'twoway':
                    PG = 'L1'
            else: #Urban
                if s6 == 'oneway':
                    PG = 'L2'
                else: #twoway
                    if LNS <= 2:
                        PG = 'L3'
                    else:
                        if s4 == 'undivided':
                            PG = 'L4'
                        else:
                            PG = 'L5'
        if PG == 0:
            PG = 'L6'
    return(PG)

def AddBaseData(FCList,Years,IRIS_route,IRIS_table,Intersections,OutputDir,Distance="0.5 Miles"):
    def SelectionType(NewSelection):
        if NewSelection:
            return("NEW_SELECTION")
        else:
            return("ADD_TO_SELECTION")
    for year in Years:
        #RteFN = os.path.basename(IRIS_route[year]).split('.')[0]
        #IntFN = os.path.basename(Intersections[year]).split('.')[0]
        #TabFN = os.path.basename(IRIS_table[year]).split('.')[0]
        RteFN = 'HWY' + str(year) + '_route'
        IntFN = 'HWY' + str(year) + '_inter'
        TabFN = 'HWY' + str(year) + '_table'
        IRISRoute = common.CreateOutLayer('IRISRoute'+str(year)+str(np.random.normal()))
        IRISInter = common.CreateOutLayer('IRISInter'+str(year)+str(np.random.normal()))
        arcpy.MakeFeatureLayer_management(IRIS_route[year],IRISRoute)
        arcpy.MakeFeatureLayer_management(Intersections[year],IRISInter)
        Flag = True
        for FC in FCList:
            if int(str(arcpy.GetCount_management(FC)))>0:
                arcpy.SelectLayerByLocation_management(in_layer=IRISRoute, 
                                               overlap_type="WITHIN_A_DISTANCE", 
                                               select_features=FC, 
                                               search_distance=Distance, 
                                               selection_type=SelectionType(Flag), 
                                               invert_spatial_relationship="NOT_INVERT")
                arcpy.SelectLayerByLocation_management(in_layer=IRISInter, 
                                               overlap_type="WITHIN_A_DISTANCE", 
                                               select_features=FC, 
                                               search_distance=Distance, 
                                               selection_type=SelectionType(Flag), 
                                               invert_spatial_relationship="NOT_INVERT")
                Flag = False
        if not Flag:
            arcpy.Delete_management(os.path.join(OutputDir,RteFN))
            arcpy.FeatureClassToFeatureClass_conversion (IRISRoute, OutputDir, RteFN)
            arcpy.Delete_management(os.path.join(OutputDir,IntFN))
            arcpy.FeatureClassToFeatureClass_conversion (IRISInter, OutputDir, IntFN)
            INV = [r.getValue('RID') for r in arcpy.SearchCursor(os.path.join(OutputDir,RteFN))]
            arcpy.Delete_management(os.path.join(OutputDir,TabFN))
            arcpy.TableToTable_conversion(in_rows=IRIS_table[year], 
                                            out_path=OutputDir, 
                                            out_name=TabFN,
                                            where_clause = '"RID" IN (' + ','.join(["'" + str(inv) + "'" for inv in INV]) + ')')
            #arcpy.TableToTable_conversion(in_rows=IRIS_table[year], 
            #                                out_path=OutputDir, 
            #                                out_name=TabFN,
            #                                where_clause = '[INVENTORY] IN (' + ','.join(["'" + str(inv) + "'" for inv in INV]) + ')')
            print('Year: {},Routes: {}, Int: {}, RETable: {}'.format(year,
                                                                 int(str(arcpy.GetCount_management(os.path.join(OutputDir,RteFN)))),
                                                                 int(str(arcpy.GetCount_management(os.path.join(OutputDir,IntFN)))),
                                                                 int(str(arcpy.GetCount_management(os.path.join(OutputDir,TabFN))))
                                                                 ))
def CON_AddBaseData(WDir,HSMPY_PATH,FCList,Years,IRIS_route,IRIS_table,Intersections,OutputDir,Distance,Title):
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_AddBaseData.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
print("Add Base Data: " + "{}")
import os, sys
import atexit
#atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
FCList = {}
Years = {}
IRIS_route = {}
IRIS_table = {}
Intersections = {}
OutputDir = r"{}"
Distance = "{}"
sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
hsmpy3.il.AddBaseData(FCList,Years,IRIS_route,IRIS_table,Intersections,OutputDir,Distance)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Title,HSMPY_PATH,FCList,Years,IRIS_route,IRIS_table,Intersections,OutputDir,Distance)
    OutFile.write(pyfile)
    OutFile.close()
    SW_MINIMIZE = 6
    SW_HIDE = 0
    info = subprocess.STARTUPINFO()
    info.dwFlags = subprocess.STARTF_USESHOWWINDOW
    info.wShowWindow = SW_MINIMIZE
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN])
                #shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def CON_CreateMDBforHSIP(WDir,HSMPY_PATH,Title,HSIP_Seg,HSIP_Int):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_CreateMDB.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Title = "{}"
print("Create MDB: " + Title)
import os, sys
import atexit
#atexit.register(input, 'Press Enter to continue...')
WDir = r'{}'
HSMPY_PATH = r'{}'
HSIP_Seg = r'{}'
HSIP_Int = r'{}'
sys.path.append(HSMPY_PATH) 
import hsmpy
import arcpy

IntLayer = hsmpy.common.CreateOutLayer('IntLayer')
SegLayer = hsmpy.common.CreateOutLayer('SegLayer')
arcpy.MakeFeatureLayer_management(HSIP_Seg,SegLayer)
arcpy.MakeFeatureLayer_management(HSIP_Int,IntLayer)
arcpy.env.outputMFlag = "Enabled"
arcpy.env.outputZFlag = "Enabled"
p = str(Title)
FN = 'HSIP_' + p + '_GIS.mdb'
MDB = os.path.join(WDir,FN)
try: os.remove(MDB)
except: pass
try: arcpy.CreatePersonalGDB_management(out_folder_path=WDir,out_name=FN)
except: pass   
arcpy.SelectLayerByAttribute_management(IntLayer,'NEW_SELECTION','"HSIP_ID" = ' +  p )
arcpy.SelectLayerByAttribute_management(SegLayer,'NEW_SELECTION','"HSIP_ID" = ' +  p )
   
SegFC = MDB + '\\Seg_' + p
IntFC = MDB + '\\Int_' + p
arcpy.Delete_management(SegFC)
arcpy.Delete_management(IntFC)
arcpy.FeatureClassToFeatureClass_conversion (SegLayer, MDB, os.path.basename(SegFC))
arcpy.FeatureClassToFeatureClass_conversion (IntLayer, MDB, os.path.basename(IntFC))
print('Total Segments: ' + arcpy.GetCount_management(SegFC)[0])
print('Total Int: ' + arcpy.GetCount_management(IntFC)[0]) 
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Title,WDir,HSMPY_PATH,HSIP_Seg,HSIP_Int)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def CON_CreateGDBforHSIP(WDir,HSMPY_PATH,Title,HSIP_Seg,HSIP_Int):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_CreateGDB.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Title = "{}"
print("Create GDB: " + Title)
import os, sys
import atexit
#atexit.register(input, 'Press Enter to continue...')
WDir = r'{}'
HSMPY_PATH = r'{}'
HSIP_Seg = r'{}'
HSIP_Int = r'{}'
sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy

IntLayer = hsmpy3.common.CreateOutLayer('IntLayer')
SegLayer = hsmpy3.common.CreateOutLayer('SegLayer')
arcpy.MakeFeatureLayer_management(HSIP_Seg,SegLayer)
arcpy.MakeFeatureLayer_management(HSIP_Int,IntLayer)
arcpy.env.outputMFlag = "Enabled"
arcpy.env.outputZFlag = "Enabled"
p = str(Title)
FN = 'HSIP_' + p + '_GIS.gdb'
MDB = os.path.join(WDir,FN)
try: os.remove(MDB)
except: pass
try: arcpy.CreateFileGDB_management(out_folder_path=WDir,out_name=FN)
except: pass   
arcpy.SelectLayerByAttribute_management(IntLayer,'NEW_SELECTION',"ContNum = '" +  p + "'")
arcpy.SelectLayerByAttribute_management(SegLayer,'NEW_SELECTION',"ContNum = '" +  p + "'")
   
SegFC = MDB + '\\Seg_' + p
IntFC = MDB + '\\Int_' + p
arcpy.Delete_management(SegFC)
arcpy.Delete_management(IntFC)
arcpy.FeatureClassToFeatureClass_conversion (SegLayer, MDB, os.path.basename(SegFC))
arcpy.FeatureClassToFeatureClass_conversion (IntLayer, MDB, os.path.basename(IntFC))
print('Total Segments: ' + arcpy.GetCount_management(SegFC)[0])
print('Total Int: ' + arcpy.GetCount_management(IntFC)[0]) 
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Title,WDir,HSMPY_PATH,HSIP_Seg,HSIP_Int)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN])
                #shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def CON_Seg_PC_HSIP(WDir,HSMPY_PATH,GDB,Years,SPFPath,Title):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_AddPC.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Title = "{}"
print("Add Predicted Crashes: " + Title)
import os, sys
import pandas as pd
import atexit
#atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
GDB = r'{}'
Years = {}
SPFPath = r'{}'
sys.path.append(HSMPY_PATH) 
import hsmpy3
import numpy as np
import arcpy
SPF_DF = pd.read_excel(SPFPath,sheetname='Summary')
SPF_DF['PGNumber'] = [int(s.split('PeerGroup ')[1][:2]) for s in SPF_DF.PG]
for year in Years:
    p = str(Title)
    SegFC = GDB + '\\Seg_' + p + '_' + str(year)
    IntFC = GDB + '\\Int_' + p + '_' + str(year) + '_points'
    NumSeg = 0
    NumInt = 0
    try: NumSeg = int(str(arcpy.GetCount_management(SegFC)))
    except: pass
    try: NumInt = int(str(arcpy.GetCount_management(IntFC)))
    except: pass
    if NumSeg > 0:
        try: hsmpy3.il.AddRoadway_PC(SegFC,SPF_DF)
        except: pass
        try:
    	    print('Seg: ' + str(year) + ', K: ' + str(np.mean([r.getValue('K_EC') for r in arcpy.SearchCursor(SegFC)])) +
        	      ', A: ' + str(np.mean([r.getValue('A_EC') for r in arcpy.SearchCursor(SegFC)])) +
            	  ', B: ' + str(np.mean([r.getValue('B_EC') for r in arcpy.SearchCursor(SegFC)]))
    	    )
        except:
            print('Seg: ' + str(year) + ' Failed')
       
    if NumInt > 0:
        try: hsmpy3.il.AddInt_PC(IntFC,SPF_DF)
        except: pass
        try:
            print('Int: ' + str(year) + ', K: ' + str(np.mean([r.getValue('K_EC') for r in arcpy.SearchCursor(IntFC)])) +
        	  ', A: ' + str(np.mean([r.getValue('A_EC') for r in arcpy.SearchCursor(IntFC)])) +
        	  ', B: ' + str(np.mean([r.getValue('B_EC') for r in arcpy.SearchCursor(IntFC)]))
    	    )
        except: 
            print('Int: ' + str(year) + ' Failed')
        
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Title,HSMPY_PATH,GDB,Years,SPFPath)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN])
                #shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def ExpectedCrash(PC,k,OC):
    w = 1.0/(1+k*PC)
    EC = PC*w + OC*(1-w)
    return(EC)
def PredictedCrash(SPF_DF,Severity = 'K',Type='Roadway',Jur='State',PG = 1,L = 0,AADT = 0,AADT_Major = 0,AADT_Minor = 0):
    df = SPF_DF[(SPF_DF.Type==Type) & (SPF_DF.State==Jur) & (SPF_DF.Severity == Severity) & (SPF_DF.PGNumber == PG)]
    Npred = 0
    k = 0
    if Jur == 'State':
        if Type == 'Roadway':
            Npred = L * math.exp(df.a.item()) * AADT ** df.b.item()
            k = df.k.item() / L
        else:
            Npred = math.exp(df.a.item()) * AADT_Major ** df.b.item() * AADT_Minor ** df.c.item()
            k = df.k.item()
    else:
        if Type == 'Roadway':
            Npred = L * math.exp(df.a.item()) * AADT ** df.b.item() /(1 + math.exp(df.c.item() + AADT * df.d.item()))
            k = df.k.item() / L
        else:
            Npred = math.exp(df.a.item()) * AADT_Major ** df.b.item() * AADT_Minor ** df.c.item() / (1 + exp(df.d.item() + AADT_Major * df.e.item() + AADT_Minor * df.f.item()))
            k = df.k.item()
    return({'Pred': Npred,'k':k})
def AddRoadway_PC(FC,SPF_DF):
    arcpy.AddField_management(FC,'K_PC','Double')
    arcpy.AddField_management(FC,'A_PC','Double')
    arcpy.AddField_management(FC,'B_PC','Double')
    arcpy.AddField_management(FC,'K_k','Double')
    arcpy.AddField_management(FC,'A_k','Double')
    arcpy.AddField_management(FC,'B_k','Double')
    arcpy.AddField_management(FC,'K_EC','Double')
    arcpy.AddField_management(FC,'A_EC','Double')
    arcpy.AddField_management(FC,'B_EC','Double')
    uc = arcpy.UpdateCursor(FC)
    for r in uc:
        PG = r.getValue('PG')
        pg_j = {'S':'State','L':"Local"}[PG[:1]]
        pg_n = int(PG[1:])
        aadt = r.getValue('AADT')
        l = r.getValue('Shape').length/5280
        for sev in ['K','A','B']:
            pc = PredictedCrash(SPF_DF,Severity = sev,Type='Roadway',Jur=pg_j,PG = pg_n,L = l,AADT = aadt)
            oc = r.getValue(sev+'_OC')
            r.setValue(sev+'_PC',pc['Pred'])
            r.setValue(sev+'_k',pc['k'])
            r.setValue(sev+'_EC',ExpectedCrash(pc['Pred'],pc['k'],oc))
        uc.updateRow(r)
def AddInt_PC(FC,SPF_DF):
    arcpy.AddField_management(FC,'K_PC','Double')
    arcpy.AddField_management(FC,'A_PC','Double')
    arcpy.AddField_management(FC,'B_PC','Double')
    arcpy.AddField_management(FC,'K_k','Double')
    arcpy.AddField_management(FC,'A_k','Double')
    arcpy.AddField_management(FC,'B_k','Double')
    arcpy.AddField_management(FC,'K_EC','Double')
    arcpy.AddField_management(FC,'A_EC','Double')
    arcpy.AddField_management(FC,'B_EC','Double')
    uc = arcpy.UpdateCursor(FC)
    for r in uc:
        PG = r.getValue('PeerGroup_CH2M_TJM')
        pg_j = {'S':'State','L':"Local"}[PG[:1]]
        pg_n = int(PG[-2:])
        aadt_major = r.getValue('AADT_Major')
        aadt_minor = r.getValue('AADT_Minor')
        for sev in ['K','A','B']:
            pc = PredictedCrash(SPF_DF,Severity = sev,Type='Intersection',Jur=pg_j,PG = pg_n,AADT_Major = aadt_major,AADT_Minor = aadt_minor)
            r.setValue(sev+'_PC',pc['Pred'])
            r.setValue(sev+'_k',pc['k'])
            oc = r.getValue(sev+'_OC')
            r.setValue(sev+'_EC',ExpectedCrash(pc['Pred'],pc['k'],oc))
        uc.updateRow(r)
def HSIP_FindMissingData(gdb,Years):
    p  = os.path.basename(gdb).split('_')[1]
    FN = os.path.join(os.path.dirname(gdb), 'HSIP_' + p + '_Status.json')  
    OutFile = open(FN, 'w')
    Mis_Base  = []
    Mis_Att   = []
    Mis_Crash = []
    Results = {'Seg_Input':0,'Int_Input':0}
    for year in Years:
        Results.update({'BaseRoute_' + str(year):0,
                        'BaseInt_'   + str(year):0,
                        'BaseTable_' + str(year):0,
                        'SegAtt_'    + str(year):None,
                        'SegCrash_'  + str(year):None,
                        'IntPoints_' + str(year):None,
                        'IntTables_' + str(year):None,
                        'IntCrash_'  + str(year):None})
    hsip_id = os.path.basename(gdb).split('_')[1]
    FCs = [gdb + '\\' + fc for fc in common.ListFCinGDBorMDB(gdb)]
    SegFC = gdb + '\\Seg_' + str(hsip_id)
    IntFC = gdb + '\\Int_' + str(hsip_id)
    if SegFC in FCs:
        Results.update({'Seg_Input':int(str(arcpy.GetCount_management(SegFC)))})
    if IntFC in FCs:
        Results.update({'Int_Input':int(str(arcpy.GetCount_management(IntFC)))})
    if Results['Seg_Input'] + Results['Int_Input']==0:
        json.dump(Results, OutFile)    
        OutFile.close()
        return(Results)
    for year in Years:
        BaseRoute = gdb + '\\' + 'HWY' + str(year) + '_route'
        BaseTab   = gdb + '\\' + 'HWY' + str(year) + '_inter'
        BaseInt   = gdb + '\\' + 'HWY' + str(year) + '_table'
        if BaseRoute in FCs:
            Results.update({'BaseRoute_' + str(year):int(str(arcpy.GetCount_management(BaseRoute)))})
        if BaseInt in FCs:
            Results.update({'BaseInt_' + str(year):int(str(arcpy.GetCount_management(BaseInt)))})
        if BaseTab in FCs:
            Results.update({'BaseTable_' + str(year):int(str(arcpy.GetCount_management(BaseTab)))})

        SegAtt    = gdb + '\\' + 'Seg_' + str(hsip_id) + '_' + str(year)
        SegCrash  = SegAtt + '_Crash'
        IntPoints = gdb + '\\' + 'Int_' + str(hsip_id) + '_' + str(year) + '_points'
        IntTables = gdb + '\\' + 'Int_' + str(hsip_id) + '_' + str(year) + '_tables'
        IntCrash  = IntPoints + '_Crash'
        if SegAtt in FCs:
            Results.update({'SegAtt_'    + str(year):int(str(arcpy.GetCount_management(SegAtt)))})
        if SegCrash in FCs:
            Results.update({'SegCrash_' + str(year):int(str(arcpy.GetCount_management(SegCrash)))})
        if IntPoints in FCs:
            Results.update({'IntPoints_' + str(year):int(str(arcpy.GetCount_management(IntPoints)))})
        if IntTables in FCs:
            Results.update({'IntTables_'  + str(year):int(str(arcpy.GetCount_management(IntTables)))})
        if IntCrash in FCs:
            Results.update({'IntCrash_'  + str(year):int(str(arcpy.GetCount_management(IntCrash)))})
    for year in Years:
        AttFlag = False
        CrashFlag = False
        if Results['BaseRoute_' + str(year)] ==0 or Results['BaseInt_' + str(year)] ==0 or Results['BaseTable_' + str(year)] ==0:
            Mis_Base.append(str(year))
        if Results['Seg_Input'] > 0:
            if Results['SegAtt_' + str(year)] is None:
                AttFlag = True
            if Results['SegCrash_' + str(year)] is None:
                CrashFlag = True
        if Results['Int_Input'] > 0:
            if Results['IntPoints_' + str(year)] is None or Results['IntTables_' + str(year)] is None:
                AttFlag = True
            if Results['IntCrash_' + str(year)] is None:
                CrashFlag = True
        if AttFlag:
            Mis_Att.append(str(year))
        if CrashFlag:
            Mis_Crash.append(str(year))
    json.dump(Results, OutFile)    
    OutFile.close()
    return(Results)
def CON_UpdateStatus(WDir,HSMPY_PATH,GDB,Years,Title):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_Status.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Title = "{}"
print("Update Status: " + Title)
import os, sys
import pandas as pd
import atexit
#atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
GDB = r'{}'
Years = {}
sys.path.append(HSMPY_PATH) 
import hsmpy3
import numpy as np
import arcpy
hsmpy3.il.HSIP_FindMissingData(GDB,Years)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Title,HSMPY_PATH,GDB,Years)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN])
                #shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)

#HSIP Results
def HSIP_SummarySheet_Contract(HSIP_DF,p,MDB,ExcelOut,Years,Fields):
    CrashCost = {'K':6245736 ,'A':336521 ,'B':123079 ,'C':69953 ,'PDO':11529 }
    CurYear = 2018
    Interest = 0.02
    TrafficGrowth = 0.01
    if not(len(HSIP_DF[HSIP_DF['ContNum'] ==  str(p)]['BeforePeriod'].item())>0 and len(HSIP_DF[HSIP_DF['ContNum'] ==  str(p)]['AfterPeriod'].item())>0):
        print('{}: Before-After Periods are not defined'.format(p))
    p = str(p)
    #FN = 'HSIP_' + p + '_GIS.mdb'
    #MDB = os.path.join(AnalysisDir,FN)
    SegFC = MDB + '\\Seg_' + p
    IntFC = MDB + '\\Int_' + p
    FN = ExcelOut
    try: os.remove(FN)
    except: pass
    writer = pd.ExcelWriter(FN, engine = 'openpyxl')
    
    BeforePeriod = [int(y) for y in HSIP_DF[HSIP_DF['ContNum'] ==  str(p)]['BeforePeriod'].item().split(';')]
    ConstPeriod  = [int(y) for y in HSIP_DF[HSIP_DF['ContNum'] ==  str(p)]['ConstPeriod' ].item().split(';')]
    AfterPeriod  = [int(y) for y in HSIP_DF[HSIP_DF['ContNum'] ==  str(p)]['AfterPeriod' ].item().split(';')]
    
    Project_df = HSIP_DF[HSIP_DF['ContNum'] ==  str(p)]
    Project_df = Project_df.transpose()
    Project_df = Project_df.sort_index()
    Project_df.to_excel(writer, sheet_name = 'ProjectDesc')
    
    NumSeg = 0
    NumInt = 0
    try: NumSeg = int(str(arcpy.GetCount_management(SegFC)))
    except: pass
    try: NumInt = int(str(arcpy.GetCount_management(IntFC)))
    except: pass
    if NumSeg==0 and NumInt == 0:
        print('{}: No Geocoded Location data'.format(p))
        
    PC_df = pd.DataFrame(columns = ['K_PC','A_PC','B_PC','K_EC','A_EC','B_EC'])
    i = 0
    for year in Years:
        PC_df.loc[i] = [0 for j in range(len(PC_df.columns))]
        i += 1
    PC_df.index = Years
    PC_df['Period'] = AssignPeriod(Years,{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
    
    SegAtt_df = pd.DataFrame()
    if NumSeg > 0:
        rdfCol = ['Year','INVENTORY','BEG_STA','END_STA']
        rdfCol.extend(Fields)
        for year in Years:
            RoadwayData = SegFC + '_' + str(year)
            try:
                rdf = common.AttributeTabletoDF(RoadwayData)
                rdf['Year'] = year
                SegAtt_df = pd.concat([SegAtt_df,rdf[rdfCol]])
                for c in ['K_PC','A_PC','B_PC','K_EC','A_EC','B_EC']:
                    if c in rdf.columns:
                        PC_df.set_value(year,c,PC_df.loc[year][c]+sum(list(rdf[c])))
            except:
                pass
        if len(SegAtt_df)>0:
            SegAtt_df['Period'] = AssignPeriod(list(SegAtt_df['Year']),{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
            SegAtt_df.to_excel(writer, sheet_name = 'Segment Attributes')

    IntPoint_df = pd.DataFrame()
    IntApprc_df = pd.DataFrame()
    if NumInt > 0:
        rdfCol = ['Year','SiteID','INVENTORY','MP']
        rdfCol.extend(Fields)
        rdfCol.append('ApprType')
        for year in Years:
            Intpoints = IntFC + '_' + str(year) + '_points'
            Inttables = IntFC + '_' + str(year) + '_tables'
            try:
                rdf1 = common.AttributeTabletoDF(Intpoints)
                rdf2 = common.AttributeTabletoDF(Inttables)
                rdf1['Year'] = year
                rdf2['Year'] = year
                IntPoint_df = pd.concat([IntPoint_df,rdf1[['Year','SiteID','TRAF_CONT','AADT_Major','AADT_Minor','PeerGroup_CH2M_TJM']]])
                IntApprc_df = pd.concat([IntApprc_df,rdf2[rdfCol]])
                for c in ['K_PC','A_PC','B_PC','K_EC','A_EC','B_EC']:
                    if c in rdf1.columns:
                        PC_df.set_value(year,c,PC_df.loc[year][c]+sum(list(rdf1[c])))
            except:
                pass
            
        if len(IntPoint_df)>0:
            IntPoint_df['Period'] = AssignPeriod(list(IntPoint_df['Year'])  ,{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
            IntPoint_df.to_excel(writer, sheet_name = 'IntPointAttr')
        if len(IntApprc_df)>0:
            IntApprc_df['Period'] = AssignPeriod(list(IntApprc_df['Year']),{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
            IntApprc_df.to_excel(writer, sheet_name = 'IntApproachAttr')
            
    if len(IntPoint_df) == 0 and len(SegAtt_df) == 0:
        print('{}: No Segment or Intersection attributes found'.format(p))
        
    df3 = DF_RawCrash(MDB,p,Years,BeforePeriod,AfterPeriod,ConstPeriod)        
    if len(df3) == 0:
        print('{}: No crash data'.format(p))
        return
    df3.to_excel(writer, sheet_name = 'RawCrash')
    
    df6 = CrashSevDF(df3,Years)
    df6['Period'] = AssignPeriod(list(df6.index),{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
    #df6.to_excel(writer, sheet_name = 'SegCrashSevAll')

    df7 = CrashSevDF(df3,BeforePeriod)
    df7.to_excel(writer, sheet_name = 'CrashSevBefore')
    
    df8 = CrashSevDF(df3,AfterPeriod)
    df8.to_excel(writer, sheet_name = 'CrashSevAfter')
    
    #constcost = HSIP_DF[HSIP_DF['ContNum']==str(p)]['CompletionAmount'].item()
    constcost = HSIP_DF[HSIP_DF['ContNum']==str(p)]['HSIPAmount'].item()
    #ServiceYears = 7
    ServiceYears = HSIP_DF[HSIP_DF['ContNum']==str(p)]['ServiceLife'].item()
    BenefitPeriod = range(ConstPeriod[-1]+1,ConstPeriod[-1]+ServiceYears+1)

    df9 = DF_BCDetail(Years,df6,PC_df,constcost,BeforePeriod,AfterPeriod,ConstPeriod,ServiceYears,Interest,TrafficGrowth,CrashCost)
    df9.to_excel(writer, sheet_name = 'BCDetails')

    df10 = DF_BCSummary(BeforePeriod,BenefitPeriod,df9)
    df10.to_excel(writer, sheet_name = 'BCSummary')
    print(df10.loc[2])
    #print('{}: Finished: BC_OC: {:0.2f}, BC_EC: {:0.2f}'.format(p,EUAB_OC/EUAC,EUAB_EC/EUAC))
    writer.save()

    writer.close()
def HSIP_SummarySheet(HSIP_DF,p,MDB,ExcelOut,Years,Fields):
    CrashCost = {'K':6245736 ,'A':336521 ,'B':123079 ,'C':69953 ,'PDO':11529 }
    CurYear = 2018
    Interest = 0.035
    TrafficGrowth = 0.01
    if not(len(HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]['BeforePeriod'].item())>0 and len(HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]['AfterPeriod'].item())>0):
        print('{}: Before-After Periods are not defined'.format(p))
    p = str(p)
    #FN = 'HSIP_' + p + '_GIS.mdb'
    #MDB = os.path.join(AnalysisDir,FN)
    SegFC = MDB + '\\Seg_' + p
    IntFC = MDB + '\\Int_' + p
    FN = ExcelOut
    try: os.remove(FN)
    except: pass
    writer = pd.ExcelWriter(FN, engine = 'openpyxl')
    
    BeforePeriod = [int(y) for y in HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]['BeforePeriod'].item().split(';')]
    ConstPeriod  = [int(y) for y in HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]['ConstPeriod' ].item().split(';')]
    AfterPeriod  = [int(y) for y in HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]['AfterPeriod' ].item().split(';')]
    
    Project_df = HSIP_DF[HSIP_DF['HSIP ID'] ==  int(p)]
    Project_df = Project_df.transpose()
    Project_df = Project_df.sort_index()
    Project_df.to_excel(writer, sheet_name = 'ProjectDesc')
    
    NumSeg = 0
    NumInt = 0
    try: NumSeg = int(str(arcpy.GetCount_management(SegFC)))
    except: pass
    try: NumInt = int(str(arcpy.GetCount_management(IntFC)))
    except: pass
    if NumSeg==0 and NumInt == 0:
        print('{}: No Geocoded Location data'.format(p))
        
    PC_df = pd.DataFrame(columns = ['K_PC','A_PC','B_PC','K_EC','A_EC','B_EC'])
    i = 0
    for year in Years:
        PC_df.loc[i] = [0 for j in range(len(PC_df.columns))]
        i += 1
    PC_df.index = Years
    PC_df['Period'] = AssignPeriod(Years,{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
    
    SegAtt_df = pd.DataFrame()
    if NumSeg > 0:
        rdfCol = ['Year','SiteID','INVENTORY','BEG_STA','END_STA']
        rdfCol.extend(Fields)
        for year in Years:
            RoadwayData = SegFC + '_' + str(year)
            try:
                rdf = common.AttributeTabletoDF(RoadwayData)
                rdf['Year'] = year
                SegAtt_df = pd.concat([SegAtt_df,rdf[rdfCol]])
                for c in ['K_PC','A_PC','B_PC','K_EC','A_EC','B_EC']:
                    if c in rdf.columns:
                        PC_df.set_value(year,c,PC_df.loc[year][c]+sum(list(rdf[c])))
            except:
                pass
        if len(SegAtt_df)>0:
            SegAtt_df['Period'] = AssignPeriod(list(SegAtt_df['Year']),{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
            SegAtt_df.to_excel(writer, sheet_name = 'Segment Attributes')

    IntPoint_df = pd.DataFrame()
    IntApprc_df = pd.DataFrame()
    if NumInt > 0:
        rdfCol = ['Year','SiteID','INVENTORY','MP']
        rdfCol.extend(Fields)
        rdfCol.append('ApprType')
        for year in Years:
            Intpoints = IntFC + '_' + str(year) + '_points'
            Inttables = IntFC + '_' + str(year) + '_tables'
            try:
                rdf1 = common.AttributeTabletoDF(Intpoints)
                rdf2 = common.AttributeTabletoDF(Inttables)
                rdf1['Year'] = year
                rdf2['Year'] = year
                IntPoint_df = pd.concat([IntPoint_df,rdf1[['Year','SiteID','TRAF_CONT','AADT_Major','AADT_Minor','PeerGroup_CH2M_TJM']]])
                IntApprc_df = pd.concat([IntApprc_df,rdf2[rdfCol]])
                for c in ['K_PC','A_PC','B_PC','K_EC','A_EC','B_EC']:
                    if c in rdf1.columns:
                        PC_df.set_value(year,c,PC_df.loc[year][c]+sum(list(rdf1[c])))
            except:
                pass
            
        if len(IntPoint_df)>0:
            IntPoint_df['Period'] = AssignPeriod(list(IntPoint_df['Year'])  ,{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
            IntPoint_df.to_excel(writer, sheet_name = 'IntPointAttr')
        if len(IntApprc_df)>0:
            IntApprc_df['Period'] = AssignPeriod(list(IntApprc_df['Year']),{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
            IntApprc_df.to_excel(writer, sheet_name = 'IntApproachAttr')
            
    if len(IntPoint_df) == 0 and len(SegAtt_df) == 0:
        print('{}: No Segment or Intersection attributes found'.format(p))
        
    df3 = DF_RawCrash(MDB,p,Years,BeforePeriod,AfterPeriod,ConstPeriod)        
    if len(df3) == 0:
        print('{}: No crash data'.format(p))
        return
    df3.to_excel(writer, sheet_name = 'RawCrash')
    #df4 = pd.DataFrame()
    #for year in BeforePeriod:
    #    SegCrashes = SegFC + '_' + str(year) + '_Crash'
    #    cdf = common.AttributeTabletoDF(SegCrashes)
    #    cdf['Year'] = year
    #    df4 = pd.concat([df4,cdf])
    #df4 = CrashTypeDF(df4)
    #df4.to_excel(writer, sheet_name = 'SegBeforeCrashType')
    
    #df5 = pd.DataFrame()
    #for year in AfterPeriod:
    #    SegCrashes = SegFC + '_' + str(year) + '_Crash'
    #    cdf = common.AttributeTabletoDF(SegCrashes)
    #    cdf['Year'] = year
    #    df5 = pd.concat([df5,cdf])
    #df5 = CrashTypeDF(df5)
    #df5.to_excel(writer, sheet_name = 'SegAfterCrashType')
    #PlotCrashType(df4,df5)
    
    df6 = CrashSevDF(df3,Years)
    df6['Period'] = AssignPeriod(list(df6.index),{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
    #df6.to_excel(writer, sheet_name = 'SegCrashSevAll')

    df7 = CrashSevDF(df3,BeforePeriod)
    df7.to_excel(writer, sheet_name = 'CrashSevBefore')
    
    df8 = CrashSevDF(df3,AfterPeriod)
    df8.to_excel(writer, sheet_name = 'CrashSevAfter')
    
    constcost = HSIP_DF[HSIP_DF['HSIP ID']==int(p)]['Total Award Amount'].item()
    ServiceYears = 7

    df9 = DF_BCDetail(Years,df6,PC_df,constcost,BeforePeriod,AfterPeriod,ConstPeriod,ServiceYears,Interest,TrafficGrowth,CrashCost)
    df9.to_excel(writer, sheet_name = 'BCDetails')

    df10 = DF_BCSummary(BeforePeriod,AfterPeriod,df9)
    df10.to_excel(writer, sheet_name = 'BCSummary')
    print(df10.loc[2])
    #print('{}: Finished: BC_OC: {:0.2f}, BC_EC: {:0.2f}'.format(p,EUAB_OC/EUAC,EUAB_EC/EUAC))
    writer.save()

    writer.close()
def DF_BCSummary(BeforePeriod,AfterPeriod,df9):
    df10 = pd.DataFrame(columns=['Period','BeginYear','EndYear',
                                 'K_OC','A_OC','B_OC','K_EC','A_EC','B_EC',
                                 'EUAC','EUAB_OC','EUAB_EC','BC_OC','BC_EC'])
    EUAC    = list(df9.loc[AfterPeriod]['EUAC'])[0]
    EUAB_OC = list(df9.loc[AfterPeriod]['EUAB_OC'])[0]
    EUAB_EC = list(df9.loc[AfterPeriod]['EUAB_EC'])[0]
    BC_EC = 0
    BC_OC = 0
    if EUAC!=0:
        BC_EC = EUAB_EC/EUAC
        BC_OC = EUAB_OC/EUAC

    df10.loc[1] = ['Before' , 
                   BeforePeriod[0],
                   BeforePeriod[-1],
                   np.mean([list(df9.loc[BeforePeriod]['K_OC'])]),
                   np.mean([list(df9.loc[BeforePeriod]['A_OC'])]),
                   np.mean([list(df9.loc[BeforePeriod]['B_OC'])]),
                   np.mean([list(df9.loc[BeforePeriod]['K_EC'])]),
                   np.mean([list(df9.loc[BeforePeriod]['A_EC'])]),
                   np.mean([list(df9.loc[BeforePeriod]['B_EC'])]),
                   0,0,0,0,0
                  ]
    df10.loc[2] = ['ServiceLife' , 
                   AfterPeriod[0],
                   AfterPeriod[-1],
                   np.mean([list(df9.loc[AfterPeriod]['K_OC'])]),
                   np.mean([list(df9.loc[AfterPeriod]['A_OC'])]),
                   np.mean([list(df9.loc[AfterPeriod]['B_OC'])]),
                   np.mean([list(df9.loc[AfterPeriod]['K_EC'])]),
                   np.mean([list(df9.loc[AfterPeriod]['A_EC'])]),
                   np.mean([list(df9.loc[AfterPeriod]['B_EC'])]),
                   EUAC,EUAB_OC,EUAB_EC,BC_OC,BC_EC
                  ]
    return(df10)
def DF_BCDetail(Years,df6,PC_df,constcost,BeforePeriod,AfterPeriod,ConstPeriod,ServiceYears,Interest,TrafficGrowth,CrashCost):
    df9 = pd.DataFrame(columns=['Period',
                                'K_OC','A_OC','B_OC','C_OC','PDO_OC',
                                'K_PC','A_PC','B_PC','K_EC','A_EC','B_EC',
                                'ConstCost',
                                'CrashCost_OC',
                                'CrashCost_EC'
                               ])
    df9['Period'] = list(df6.loc[Years]['Period'])
    df9['K_OC']   = list(df6.loc[Years]['K_Crashes'])
    df9['A_OC']   = list(df6.loc[Years]['A_Crashes'])
    df9['B_OC']   = list(df6.loc[Years]['B_Crashes'])
    df9['C_OC']   = list(df6.loc[Years]['C_Crashes'])
    df9['PDO_OC'] = list(df6.loc[Years]['PDO'])
    for c in ['K_PC','A_PC','B_PC','K_EC','A_EC','B_EC']:
        df9[c]   = list(PC_df.loc[Years][c])
    constcost1 = [0 for y in BeforePeriod]
    constcost2 = [constcost/len(ConstPeriod) for y in ConstPeriod]
    constcost3 = [0 for y in AfterPeriod]
    ccl = constcost1
    ccl.extend(constcost2)
    ccl.extend(constcost3)
    df9['ConstCost'] = ccl
    #df9['ConstCostPV'] = [TodayDollar(ccl[i],y,CurYear,Interest) for i,y in enumerate(Years)]
    df9['CrashCost_OC'] =   [sum([df9.loc[i][c+'_OC'].item()*CrashCost[c] for c in ['K','A','B']]) for i,y in enumerate(Years)]
    #df9['CrashCost_OCPV'] = [TodayDollar(df9.loc[i]['CrashCost_OC'].item(),y,CurYear,Interest) for i,y in enumerate(Years)]
    df9['CrashCost_EC'] =   [sum([df9.loc[i][c+'_EC'].item()*CrashCost[c] for c in ['K','A','B']]) for i,y in enumerate(Years)]
    #df9['CrashCost_ECPV'] = [TodayDollar(df9.loc[i]['CrashCost_EC'].item(),y,CurYear,Interest) for i,y in enumerate(Years)]
    df9.index = Years
    if ConstPeriod[-1]+ServiceYears+1>AfterPeriod[-1]+1:
        ServicePeriod = range(AfterPeriod[-1]+1,ConstPeriod[-1]+ServiceYears+1)
    else:
        ServicePeriod = []
    for i in ServicePeriod:
        df9.loc[i] = ['Service',
                  np.mean([list(df9.loc[AfterPeriod]['K_OC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['A_OC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['B_OC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['C_OC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['PDO_OC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['K_PC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['A_PC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['B_PC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['K_EC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['A_EC'])]),
                  np.mean([list(df9.loc[AfterPeriod]['B_EC'])]),
                  0,
                  np.mean([list(df9.loc[AfterPeriod]['CrashCost_OC'])]),
                  #TodayDollar(np.mean([list(df9.loc[AfterPeriod]['CrashCost_OC'])]),i,CurYear,Interest),
                  np.mean([list(df9.loc[AfterPeriod]['CrashCost_EC'])])
                  #TodayDollar(np.mean([list(df9.loc[AfterPeriod]['CrashCost_EC'])]),i,CurYear,Interest)
                     ]
    EUAC    = constcost * (1+Interest)**(2018-min(ConstPeriod))#* AP(Interest,ServiceYears)
    BenefitPeriod = range(ConstPeriod[-1]+1,ConstPeriod[-1]+ServiceYears+1)
    CrashBenefit_OC = np.mean([list(df9.loc[BeforePeriod]['CrashCost_OC'])]) - np.mean([list(df9.loc[BenefitPeriod]['CrashCost_OC'])])
    CrashBenefit_EC = np.mean([list(df9.loc[BeforePeriod]['CrashCost_EC'])]) - np.mean([list(df9.loc[BenefitPeriod]['CrashCost_EC'])])
    EUAB_OC = CrashBenefit_OC * ServiceYears # * FA(TrafficGrowth,ServiceYears) /ServiceYears
    EUAB_EC = CrashBenefit_EC * ServiceYears # FA(TrafficGrowth,ServiceYears) /ServiceYears
    #if EUAB_OC<0: EUAB_OC = 0
    #if EUAB_EC<0: EUAB_EC = 0
    df9.set_value(range(ConstPeriod[-1]+1,ConstPeriod[-1]+ServiceYears+1),'EUAC',EUAC)
    df9.set_value(range(ConstPeriod[-1]+1,ConstPeriod[-1]+ServiceYears+1),'EUAB_OC',EUAB_OC)
    df9.set_value(range(ConstPeriod[-1]+1,ConstPeriod[-1]+ServiceYears+1),'EUAB_EC',EUAB_EC)
    return(df9)
def RemoveTotals(df):
    df = df[[c for c in df.columns if c!='Total']]
    df = df.loc[[i for i in df.index if i!='Total']]
    return(df)
def CreateEmptyCSDF(Years):
    CSDF = pd.DataFrame(columns = ['K_Crashes','A_Crashes','B_Crashes','C_Crashes','Fatalities','A_Injuries','B_Injuries','C_Injuries','PDO','Wet_Weather','Not_Lighted'])
    i = 0
    for year in Years:
        CSDF.loc[i] = [0 for j in range(len(CSDF.columns))]
        i += 1
    CSDF.index = Years
    return(CSDF)
def AddCrashSevValues(DF,year,SiteCrash):
    DF.loc[year]['K_Crashes']   += len([1 for i,r in SiteCrash.iterrows() if r['Crash_injury_severity']=='Fatal Crash'    and int(r['Crash_Year'])==year-2000])
    DF.loc[year]['A_Crashes']   += len([1 for i,r in SiteCrash.iterrows() if r['Crash_injury_severity']=='A Injury Crash' and int(r['Crash_Year'])==year-2000])
    DF.loc[year]['B_Crashes']   += len([1 for i,r in SiteCrash.iterrows() if r['Crash_injury_severity']=='B Injury Crash' and int(r['Crash_Year'])==year-2000])
    DF.loc[year]['C_Crashes']   += len([1 for i,r in SiteCrash.iterrows() if r['Crash_injury_severity']=='C Injury Crash' and int(r['Crash_Year'])==year-2000])
    DF.loc[year]['PDO']         += sum([1 for i,r in SiteCrash.iterrows() if r['Crash_injury_severity']=='No Injuries'    and int(r['Crash_Year'])==year-2000])
    DF.loc[year]['Wet_Weather'] += sum([1 for i,r in SiteCrash.iterrows() if r['Weather']=='Rain' and int(r['Crash_Year'])==year-2000])
    DF.loc[year]['Not_Lighted'] += sum([1 for i,r in SiteCrash.iterrows() if r['Light_condition']=='Darkness' and int(r['Crash_Year'])==year-2000])
    DF.loc[year]['Fatalities']  += sum([r['Total_killed'] for i,r in SiteCrash.iterrows() if int(r['Crash_Year'])==year-2000])
    DF.loc[year]['A_Injuries']  += sum([r['A_injuries'] for i,r in SiteCrash.iterrows() if int(r['Crash_Year'])==year-2000])
    DF.loc[year]['B_Injuries']  += sum([r['B_injuries'] for i,r in SiteCrash.iterrows() if int(r['Crash_Year'])==year-2000])
    DF.loc[year]['C_Injuries']  += sum([r['C_injuries'] for i,r in SiteCrash.iterrows() if int(r['Crash_Year'])==year-2000])
    return(DF)
def CrashSevDF(Data,Years):
    DFSev = CreateEmptyCSDF(Years)
    for year in Years:
        DFSev = AddCrashSevValues(DFSev,year,Data)
    DFSev['Total'] = [sum([r[c] for c in ['K_Crashes','A_Crashes','B_Crashes','C_Crashes','PDO']]) for i,r in DFSev.iterrows()]
    DFSev.loc['Total'] = [sum(DFSev[c]) for c in DFSev.columns]
    return(DFSev)
def AssignPeriod(L,Assignmnts):
    out = []
    for l in L:
        a = ''
        for i in Assignmnts.keys():
            if l in Assignmnts[i]:
                a = i
                break
        out.append(a)
    return(out)
def TodayDollar(Value,Year,CurYear,interest):
    n = CurYear - Year
    r = (1+interest)**n
    return(Value*r)
def CrashTypeDF(Data):
    ctL = []
    for i,r in Data.iterrows():
        ct = r['Type_of_crash']
        ct_adj = ct.lower()
        ct_adj = ct_adj.replace('-', ' ')
        ctL.append(ct_adj)
    Data['Type_of_crash'] = ctL
    Rows = ['Fatal Crash','A Injury','B Injury','C Injury','PDO']
    Columns = ['animal', 'fixed object', 'head on', 'overturned', 'other object','other non collision',
           'rear end','angle','turning','sideswipe opposite direction', 'sideswipe same direction',
           'parked motor vehicle', 'pedestrian',]
    Summary = Data['Type_of_crash'].value_counts()
    CTDF = pd.DataFrame(columns = Columns)
    for ct in Columns:
        CTDF[ct] = [
           sum([1 for i,r in Data.iterrows() if r['Type_of_crash'] == ct and r['Crash_injury_severity']=='Fatal Crash']), 
           sum([1 for i,r in Data.iterrows() if r['Type_of_crash'] == ct and r['Crash_injury_severity']=='A Injury Crash']), 
           sum([1 for i,r in Data.iterrows() if r['Type_of_crash'] == ct and r['Crash_injury_severity']=='B Injury Crash']), 
           sum([1 for i,r in Data.iterrows() if r['Type_of_crash'] == ct and r['Crash_injury_severity']=='C Injury Crash']), 
           sum([1 for i,r in Data.iterrows() if r['Type_of_crash'] == ct and r['Crash_injury_severity']=='No Injuries']), 
        ]
    CTDF.index = Rows
    CTDF['Total'] = [sum([r[c].item() for c in CTDF.columns]) for i,r in CTDF.iterrows()]
    CTDF.loc['Total'] = [sum(CTDF[c]) for c in CTDF.columns]
    return(CTDF)
def AP(i,n):
        r = (1+i)**n
        return(i*r/(r-1))
def FA(i,n):
        r = (1+i)**n
        return((r-1)/i)
def BCRatio(TotalCost,ServiceYears,Interest,TrafficGrowth,AverageCrashValue,CMF):

    AverageCrashBenefit = AverageCrashValue * (1-CMF)  # Average crash cost per year for before period x CMF
    TotalCost = float(TotalCost)
    EUAC = TotalCost * AP(Interest,ServiceYears)
    EUAB = AverageCrashBenefit * FA(TrafficGrowth,ServiceYears) /ServiceYears
    BC = EUAB/EUAC
    print(EUAB,EUAC)
    return(BC)
def DF_RawCrash(MDB,p,Years,BeforePeriod,AfterPeriod,ConstPeriod):
    #p = int(os.path.basename(MDB).split('_')[1])
    SegFC = MDB + '\\Seg_' + p
    IntFC = MDB + '\\Int_' + p
    NumSeg = 0
    NumInt = 0
    try: NumSeg = int(str(arcpy.GetCount_management(SegFC)))
    except: pass
    try: NumInt = int(str(arcpy.GetCount_management(IntFC)))
    except: pass
    df3 = pd.DataFrame()
    if NumSeg > 0:
        df3 = pd.DataFrame()
        for year in Years:
            SegCrashes = SegFC + '_' + str(year) + '_Crash'
            try:
                cdf = common.AttributeTabletoDF(SegCrashes)
                cdf['Year'] = year
                df3 = pd.concat([df3,cdf])
            except:
                pass
    if NumInt > 0:
        df3 = pd.DataFrame()
        for year in Years:
            IntCrashes = IntFC + '_' + str(year) + '_points_Crash'
            try:
                cdf = common.AttributeTabletoDF(IntCrashes)
                cdf['Year'] = year
                df3 = pd.concat([df3,cdf])
            except:
                pass
    if 'Year' in df3.columns:
        df3['Period'] = AssignPeriod(list(df3['Year']),{'BeforePeriod':BeforePeriod,'AfterPeriod':AfterPeriod,'CosntPeriod':ConstPeriod})
    return(df3)
def CON_ExcelSheetSummary(WDir,HSMPY_PATH,MDB,Years,ExcelOut,HSIP_Path,Title,Fields):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_ExcelSum.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Title = "{}"
print("Create Summary Sheet: " + Title)
import os, sys
import pandas as pd
import atexit
#atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
MDB = r'{}'
Years = {}
ExcelOut = r'{}'
HSIP_Path = r'{}'
Fields = {}
sys.path.append(HSMPY_PATH) 
import hsmpy3
import numpy as np
import arcpy
HSIP_DF = hsmpy3.il.CreateHSIPDataFrame(HSIP_Path,Years)
hsmpy3.il.HSIP_SummarySheet(HSIP_DF,Title,MDB,ExcelOut,Years,Fields)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Title,HSMPY_PATH,MDB,Years,ExcelOut,HSIP_Path,Fields)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN])
                #shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def CON_ExcelSheetSummary_Contract(WDir,HSMPY_PATH,MDB,Years,ExcelOut,HSIP_Path,Title,Fields):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_ExcelSum.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Title = "{}"
print("Create Summary Sheet: " + Title)
import os, sys
import pandas as pd
import atexit
#atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
MDB = r'{}'
Years = {}
ExcelOut = r'{}'
HSIP_Path = r'{}'
Fields = {}
sys.path.append(HSMPY_PATH) 
import hsmpy3
import numpy as np
import arcpy
HSIP_DF = pd.read_excel(HSIP_Path)
hsmpy3.il.HSIP_SummarySheet_Contract(HSIP_DF,Title,MDB,ExcelOut,Years,Fields)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Title,HSMPY_PATH,MDB,Years,ExcelOut,HSIP_Path,Fields)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN])
                #shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)

def CostCat(a):
    if a<=100000:
        return('Low')
    if a<=1000000:
        return('Med')
    return('High')
def Extract_EAs(s,EA):
    try:
        if math.isnan(s):
            return([])
    except:
        s = str(s)
    L_List = s.split(' ')
    ea_List = {ea:False for ea in EA}
    for k in L_List:
        k = k.replace(',','')
        if len(k)<3:
            continue
        for ea in EA:
            if k in ea:
                ea_List[ea] = True
    return([ea for ea in ea_List if ea_List[ea]])
def HSIP_Aggr_Cost(HSIP_DF,OutDir,FN):
    Aggr_DF = pd.DataFrame(columns=['Tot','W Tot Award','Tot.Awrd.Amount','3Ys BA',
                                    'Proc_OC','Proc_OC_BC>1','EUAC_OC','EUAB_OC','BC_OC',
                                    'Proc_EC','Proc_EC_BC>1','EUAC_EC','EUAB_EC','BC_EC',
                                   'HSIP_ID_OC','HSIP_ID_EC'])
    Index = ['Low','Med','High']
    for c in Aggr_DF.columns:
        Aggr_DF[c] = [0.0 for ea in Index]
    Aggr_DF.index = Index
    Aggr_DF['HSIP_ID_OC'] = ''
    Aggr_DF['HSIP_ID_EC'] = ''
    
    for i,r in HSIP_DF.iterrows():
        ea_List = [CostCat(r['CompletionAmount'])]
        for ea in ea_List:
            Aggr_DF.set_value(ea,'Tot',Aggr_DF.loc[ea]['Tot']+1) 

            if r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate']):
                Aggr_DF.set_value(ea,'W Tot Award',Aggr_DF.loc[ea]['W Tot Award']+1)
                Aggr_DF.set_value(ea,'Tot.Awrd.Amount',Aggr_DF.loc[ea]['Tot.Awrd.Amount']+r['CompletionAmount'])
            
                if len(r['BeforePeriod'].split(';'))>=2 and len(r['AfterPeriod'].split(';'))>=2:
                    Aggr_DF.set_value(ea,'3Ys BA',Aggr_DF.loc[ea]['3Ys BA']+1)
                    
                    if r['EUAC']>0 and r['EUAB_OC']!=0:
                        Aggr_DF.set_value(ea,'Proc_OC',Aggr_DF.loc[ea]['Proc_OC']+1)
                        Aggr_DF.set_value(ea,'EUAC_OC',Aggr_DF.loc[ea]['EUAC_OC']+r['EUAC'])
                        Aggr_DF.set_value(ea,'EUAB_OC',Aggr_DF.loc[ea]['EUAB_OC']+r['EUAB_OC'])
                        Aggr_DF.set_value(ea,'BC_OC'  ,Aggr_DF.loc[ea]['EUAB_OC']/Aggr_DF.loc[ea]['EUAC_OC'])
                        Aggr_DF.set_value(ea,'HSIP_ID_OC',Aggr_DF.loc[ea]['HSIP_ID_OC']+';' + str(r['ContNum']))
                        if r['BC_OC']>1:
                            Aggr_DF.set_value(ea,'Proc_OC_BC>1',Aggr_DF.loc[ea]['Proc_OC_BC>1']+1)

                    if r['EUAC']>0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC']):
                        Aggr_DF.set_value(ea,'Proc_EC',Aggr_DF.loc[ea]['Proc_EC']+1)
                        Aggr_DF.set_value(ea,'EUAC_EC',Aggr_DF.loc[ea]['EUAC_EC']+r['EUAC'])
                        Aggr_DF.set_value(ea,'EUAB_EC',Aggr_DF.loc[ea]['EUAB_EC']+r['EUAB_EC'])
                        Aggr_DF.set_value(ea,'BC_EC'  ,Aggr_DF.loc[ea]['EUAB_EC']/Aggr_DF.loc[ea]['EUAC_EC'])
                        Aggr_DF.set_value(ea,'HSIP_ID_EC',Aggr_DF.loc[ea]['HSIP_ID_EC']+';' + str(r['ContNum']))
                        if r['BC_EC']>1:
                            Aggr_DF.set_value(ea,'Proc_EC_BC>1',Aggr_DF.loc[ea]['Proc_EC_BC>1']+1)
    for c in ['HSIP_ID_EC','HSIP_ID_OC']:
        Aggr_DF[c] = [s[1:] for s in Aggr_DF[c]]        
    Aggr_DF.index = Index
    TotL = []
    for c in Aggr_DF.columns:
        if c in ['HSIP_ID_EC','HSIP_ID_OC']:
            TotL.append(0)
        else:
            TotL.append(sum(Aggr_DF[c]))
    Aggr_DF.loc['Total'] = TotL
    Aggr_DF.set_value('Total','BC_OC',Aggr_DF.loc['Total']['EUAB_OC']/Aggr_DF.loc['Total']['EUAC_OC'])
    Aggr_DF.set_value('Total','BC_EC',Aggr_DF.loc['Total']['EUAB_EC']/Aggr_DF.loc['Total']['EUAC_EC'])
    Ex_FN = OutDir + '\\' + FN + '.xlsx'
    Pn_FN = OutDir + '\\' + FN + '.png'
    Aggr_DF.to_excel(Ex_FN)
    Agg_BoxPlot(HSIP_DF,Aggr_DF,Pn_FN)
    return(Aggr_DF)
def HSIP_Aggr_Systemic(HSIP_DF,OutDir,FN):
    Aggr_DF = pd.DataFrame(columns=['Tot','W Tot Award','Tot.Awrd.Amount','3Ys BA',
                                    'Proc_OC','Proc_OC_BC>1','EUAC_OC','EUAB_OC','BC_OC',
                                    'Proc_EC','Proc_EC_BC>1','EUAC_EC','EUAB_EC','BC_EC',
                                   'HSIP_ID_OC','HSIP_ID_EC'])
    Index = ['Systemic','Non-Systemic']
    for c in Aggr_DF.columns:
        Aggr_DF[c] = [0.0 for ea in Index]
    Aggr_DF.index = Index
    Aggr_DF['HSIP_ID_OC'] = ''
    Aggr_DF['HSIP_ID_EC'] = ''
    
    for i,r in HSIP_DF.iterrows():
        ea_List = [{True:'Systemic',False:'Non-Systemic'}[r['IsSystemic']]]
        for ea in ea_List:
            Aggr_DF.set_value(ea,'Tot',Aggr_DF.loc[ea]['Tot']+1) 

            if r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate']):
                Aggr_DF.set_value(ea,'W Tot Award',Aggr_DF.loc[ea]['W Tot Award']+1)
                Aggr_DF.set_value(ea,'Tot.Awrd.Amount',Aggr_DF.loc[ea]['Tot.Awrd.Amount']+r['CompletionAmount'])
            
                if len(r['BeforePeriod'].split(';'))>=2 and len(r['AfterPeriod'].split(';'))>=2:
                    Aggr_DF.set_value(ea,'3Ys BA',Aggr_DF.loc[ea]['3Ys BA']+1)
                    
                    if r['EUAC']>0 and r['EUAB_OC']!=0:
                        Aggr_DF.set_value(ea,'Proc_OC',Aggr_DF.loc[ea]['Proc_OC']+1)
                        Aggr_DF.set_value(ea,'EUAC_OC',Aggr_DF.loc[ea]['EUAC_OC']+r['EUAC'])
                        Aggr_DF.set_value(ea,'EUAB_OC',Aggr_DF.loc[ea]['EUAB_OC']+r['EUAB_OC'])
                        Aggr_DF.set_value(ea,'BC_OC'  ,Aggr_DF.loc[ea]['EUAB_OC']/Aggr_DF.loc[ea]['EUAC_OC'])
                        Aggr_DF.set_value(ea,'HSIP_ID_OC',Aggr_DF.loc[ea]['HSIP_ID_OC']+';' + str(r['ContNum']))
                        if r['BC_OC']>1:
                            Aggr_DF.set_value(ea,'Proc_OC_BC>1',Aggr_DF.loc[ea]['Proc_OC_BC>1']+1)

                    if r['EUAC']>0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC']):
                        Aggr_DF.set_value(ea,'Proc_EC',Aggr_DF.loc[ea]['Proc_EC']+1)
                        Aggr_DF.set_value(ea,'EUAC_EC',Aggr_DF.loc[ea]['EUAC_EC']+r['EUAC'])
                        Aggr_DF.set_value(ea,'EUAB_EC',Aggr_DF.loc[ea]['EUAB_EC']+r['EUAB_EC'])
                        Aggr_DF.set_value(ea,'BC_EC'  ,Aggr_DF.loc[ea]['EUAB_EC']/Aggr_DF.loc[ea]['EUAC_EC'])
                        Aggr_DF.set_value(ea,'HSIP_ID_EC',Aggr_DF.loc[ea]['HSIP_ID_EC']+';' + str(r['ContNum']))
                        if r['BC_EC']>1:
                            Aggr_DF.set_value(ea,'Proc_EC_BC>1',Aggr_DF.loc[ea]['Proc_EC_BC>1']+1)
    for c in ['HSIP_ID_EC','HSIP_ID_OC']:
        Aggr_DF[c] = [s[1:] for s in Aggr_DF[c]]        
    Aggr_DF.index = Index
    TotL = []
    for c in Aggr_DF.columns:
        if c in ['HSIP_ID_EC','HSIP_ID_OC']:
            TotL.append(0)
        else:
            TotL.append(sum(Aggr_DF[c]))
    Aggr_DF.loc['Total'] = TotL
    Aggr_DF.set_value('Total','BC_OC',Aggr_DF.loc['Total']['EUAB_OC']/Aggr_DF.loc['Total']['EUAC_OC'])
    Aggr_DF.set_value('Total','BC_EC',Aggr_DF.loc['Total']['EUAB_EC']/Aggr_DF.loc['Total']['EUAC_EC'])
    Ex_FN = OutDir + '\\' + FN + '.xlsx'
    Pn_FN = OutDir + '\\' + FN + '.png'
    Aggr_DF.to_excel(Ex_FN)
    Agg_BoxPlot(HSIP_DF,Aggr_DF,Pn_FN)
    return(Aggr_DF)
def HSIP_Aggr_EA(HSIP_DF,OutDir,FN):
    EA = ['RoadDepart',
            'Intersections',
            'DrBehavAwar',
            'LargeTrucks',
            'HwyRRGradeXX',
            'AlcoholRel',
            'InfoSys',
            'WorkZones',
            'BeltsProtection',
            'VulnerUsers']

    Aggr_DF = pd.DataFrame(columns=['Tot','W Tot Award','Tot.Awrd.Amount','3Ys BA',
                                    'Proc_OC','Proc_OC_BC>1','EUAC_OC','EUAB_OC','BC_OC',
                                    'Proc_EC','Proc_EC_BC>1','EUAC_EC','EUAB_EC','BC_EC',
                                   'HSIP_ID_OC','HSIP_ID_EC'])
    Index = EA
    for c in Aggr_DF.columns:
        Aggr_DF[c] = [0.0 for ea in EA]
    Aggr_DF.index = Index
    Aggr_DF['HSIP_ID_OC'] = ''
    Aggr_DF['HSIP_ID_EC'] = ''
    
    for i,r in HSIP_DF.iterrows():
        ea_List = Extract_EAs(r['EA'],EA)
        for ea in ea_List:
            Aggr_DF.set_value(ea,'Tot',Aggr_DF.loc[ea]['Tot']+1) 

            if r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate']):
                Aggr_DF.set_value(ea,'W Tot Award',Aggr_DF.loc[ea]['W Tot Award']+1)
                Aggr_DF.set_value(ea,'Tot.Awrd.Amount',Aggr_DF.loc[ea]['Tot.Awrd.Amount']+r['CompletionAmount'])
            
                if len(r['BeforePeriod'].split(';'))>=2 and len(r['AfterPeriod'].split(';'))>=2:
                    Aggr_DF.set_value(ea,'3Ys BA',Aggr_DF.loc[ea]['3Ys BA']+1)
                    
                    if r['EUAC']>0 and r['EUAB_OC']!=0:
                        Aggr_DF.set_value(ea,'Proc_OC',Aggr_DF.loc[ea]['Proc_OC']+1)
                        Aggr_DF.set_value(ea,'EUAC_OC',Aggr_DF.loc[ea]['EUAC_OC']+r['EUAC'])
                        Aggr_DF.set_value(ea,'EUAB_OC',Aggr_DF.loc[ea]['EUAB_OC']+r['EUAB_OC'])
                        Aggr_DF.set_value(ea,'BC_OC'  ,Aggr_DF.loc[ea]['EUAB_OC']/Aggr_DF.loc[ea]['EUAC_OC'])
                        Aggr_DF.set_value(ea,'HSIP_ID_OC',Aggr_DF.loc[ea]['HSIP_ID_OC']+';' + str(r['ContNum']))
                        if r['BC_OC']>1:
                            Aggr_DF.set_value(ea,'Proc_OC_BC>1',Aggr_DF.loc[ea]['Proc_OC_BC>1']+1)

                    if r['EUAC']>0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC']):
                        Aggr_DF.set_value(ea,'Proc_EC',Aggr_DF.loc[ea]['Proc_EC']+1)
                        Aggr_DF.set_value(ea,'EUAC_EC',Aggr_DF.loc[ea]['EUAC_EC']+r['EUAC'])
                        Aggr_DF.set_value(ea,'EUAB_EC',Aggr_DF.loc[ea]['EUAB_EC']+r['EUAB_EC'])
                        Aggr_DF.set_value(ea,'BC_EC'  ,Aggr_DF.loc[ea]['EUAB_EC']/Aggr_DF.loc[ea]['EUAC_EC'])
                        Aggr_DF.set_value(ea,'HSIP_ID_EC',Aggr_DF.loc[ea]['HSIP_ID_EC']+';' + str(r['ContNum']))
                        if r['BC_EC']>1:
                            Aggr_DF.set_value(ea,'Proc_EC_BC>1',Aggr_DF.loc[ea]['Proc_EC_BC>1']+1)
    for c in ['HSIP_ID_EC','HSIP_ID_OC']:
        Aggr_DF[c] = [s[1:] for s in Aggr_DF[c]]        
    Aggr_DF.index = Index
    TotL = []
    for c in Aggr_DF.columns:
        if c in ['HSIP_ID_EC','HSIP_ID_OC']:
            TotL.append(0)
        else:
            TotL.append(sum(Aggr_DF[c]))
    Aggr_DF.loc['Total'] = TotL
    Aggr_DF.set_value('Total','BC_OC',Aggr_DF.loc['Total']['EUAB_OC']/Aggr_DF.loc['Total']['EUAC_OC'])
    Aggr_DF.set_value('Total','BC_EC',Aggr_DF.loc['Total']['EUAB_EC']/Aggr_DF.loc['Total']['EUAC_EC'])
    Ex_FN = OutDir + '\\' + FN + '.xlsx'
    Pn_FN = OutDir + '\\' + FN + '.png'
    Aggr_DF.to_excel(Ex_FN)
    Agg_BoxPlot(HSIP_DF,Aggr_DF,Pn_FN)
    return(Aggr_DF)
def HSIP_Aggr_FundSource(HSIP_DF,OutDir,FN):
    Aggr_DF = pd.DataFrame()
    Index = ['D20','D21','D22','D15','D10','D28']

    Aggr_DF['Tot']    = [len(HSIP_DF[HSIP_DF['FundSource']==i]) for i in Index]

    Aggr_DF['W Tot Award']    = [len(HSIP_DF[[r['FundSource']==i and 
                                              r['CompletionAmount']>0 for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['Tot.Awrd.Amount']= [sum(HSIP_DF[[r['FundSource']==i and
                                              r['CompletionAmount']>0 for j,r in HSIP_DF.iterrows()]]['CompletionAmount']) for i in Index]

    Aggr_DF['3Ys BA'] = [len(HSIP_DF[[r['FundSource']==i and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0
                                      for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['Proc_OC'] = [len(HSIP_DF[[r['FundSource']==i and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and r['EUAC']!=0 and r['EUAB_OC']!=0
                                      for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['Proc_OC_BC>1'] = [len(HSIP_DF[[r['FundSource']==i and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and r['EUAC']!=0 and r['EUAB_OC']!=0 and r['BC_OC']>1
                                      for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['EUAC_OC'] = [sum(HSIP_DF[[i==r['FundSource'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and r['EUAC']!=0 and r['EUAB_OC']!=0
                                      for j,r in HSIP_DF.iterrows()]]['EUAC']) for i in Index]

    Aggr_DF['EUAB_OC'] = [sum(HSIP_DF[[i==r['FundSource'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and r['EUAC']!=0 and r['EUAB_OC']!=0
                                      for j,r in HSIP_DF.iterrows()]]['EUAB_OC']) for i in Index]

    Aggr_DF['BC_OC'] = [r['EUAB_OC']/(r['EUAC_OC'] or not r['EUAC_OC']) for i,r in Aggr_DF.iterrows()]

    Aggr_DF['Proc_EC'] = [len(HSIP_DF[[r['FundSource']==i and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and r['EUAC']!=0 and r['EUAB_OC']!=0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC'])
                                      for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['Proc_EC_BC>1'] = [len(HSIP_DF[[r['FundSource']==i and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and r['EUAC']!=0 and r['EUAB_OC']!=0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC']) and r['BC_EC']>1
                                      for j,r in HSIP_DF.iterrows()]]) for i in Index]
    
    Aggr_DF['EUAC_EC'] = [sum(HSIP_DF[[i==r['FundSource'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and r['EUAC']!=0 and r['EUAB_OC']!=0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC'])
                                      for j,r in HSIP_DF.iterrows()]]['EUAC']) for i in Index]
    Aggr_DF['EUAB_EC'] = [sum(HSIP_DF[[i==r['FundSource'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and r['EUAC']!=0 and r['EUAB_OC']!=0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC'])
                                      for j,r in HSIP_DF.iterrows()]]['EUAB_EC']) for i in Index]

    Aggr_DF['BC_EC'] = [r['EUAB_EC']/(r['EUAC_EC'] or not r['EUAC_EC']) for i,r in Aggr_DF.iterrows()]

    Aggr_DF['HSIP_ID_OC'] = [';'.join([str(ID) for ID in list(HSIP_DF[[i==r['FundSource'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and r['EUAC']!=0 and r['EUAB_OC']!=0
                                                                       for j,r in HSIP_DF.iterrows()]]['ContNum'])]) for i in Index]

    Aggr_DF['HSIP_ID_EC'] = [';'.join([str(ID) for ID in list(HSIP_DF[[i==r['FundSource'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and r['EUAC']!=0 and r['EUAB_OC']!=0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC'])
                                                                       for j,r in HSIP_DF.iterrows()]]['ContNum'])]) for i in Index]

    Aggr_DF.index = Index
    #Aggr_DF['Total'] = [sum([r[c] for c in ['Tot','W Tot Award','Tot.Awrd.Amount','3Ys BA','Proc','EUAC','EUAB_OC','EUAB_EC','BC_OC','BC_EC']]) for i,r in Aggr_DF.iterrows()]
    TotL = []
    for c in Aggr_DF.columns:
        if c in ['HSIP_ID_EC','HSIP_ID_OC']:
            TotL.append(0)
        else:
            TotL.append(sum(Aggr_DF[c]))
    Aggr_DF.loc['Total'] = TotL
    Aggr_DF.set_value('Total','BC_OC',Aggr_DF.loc['Total']['EUAB_OC']/Aggr_DF.loc['Total']['EUAC_OC'])
    Aggr_DF.set_value('Total','BC_EC',Aggr_DF.loc['Total']['EUAB_EC']/Aggr_DF.loc['Total']['EUAC_EC'])
    Ex_FN = OutDir + '\\' + FN + '.xlsx'
    Pn_FN = OutDir + '\\' + FN + '.png'
    Aggr_DF.to_excel(Ex_FN)
    Agg_BoxPlot(HSIP_DF,Aggr_DF,Pn_FN)
    return(Aggr_DF)
def HSIP_Aggr_District(HSIP_DF,OutDir,FN):
    Aggr_DF = pd.DataFrame()
    Index = ['District1','District2','District3','District4','District5','District6','District7','District8','District9']

    Aggr_DF['Tot']    = [len(HSIP_DF[[i[-1]==r['District'] for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['Completed']    = [len(HSIP_DF[[(i[-1])==r['District'] and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate']) for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['Tot.Awrd.Amount']= [sum(HSIP_DF[[(i[-1])==r['District'] and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate']) for j,r in HSIP_DF.iterrows()]]['CompletionAmount']) for i in Index]

    Aggr_DF['3Ys BA'] = [len(HSIP_DF[[(i[-1])==r['District'] and
                         len(r['BeforePeriod'].split(';'))>2 and
                         len(r['AfterPeriod' ].split(';'))>2 and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate']) 
                                      for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['Proc_OC'] = [len(HSIP_DF[[(i[-1])==r['District'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate']) and r['EUAC']!=0 and r['EUAB_OC']!=0
                                      for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['Proc_OC_BC>1'] = [len(HSIP_DF[[(i[-1])==r['District'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate']) and r['EUAC']!=0 and r['EUAB_OC']!=0 and r['BC_OC']>1
                                      for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['EUAC_OC'] = [sum(HSIP_DF[[(i[-1])==r['District'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate']) and r['EUAC']!=0 and r['EUAB_OC']!=0
                                      for j,r in HSIP_DF.iterrows()]]['EUAC']) for i in Index]

    Aggr_DF['EUAB_OC'] = [sum(HSIP_DF[[(i[-1])==r['District'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate']) and r['EUAC']!=0 and r['EUAB_OC']!=0
                                      for j,r in HSIP_DF.iterrows()]]['EUAB_OC']) for i in Index]

    Aggr_DF['BC_OC'] = [r['EUAB_OC']/(r['EUAC_OC'] or not r['EUAC_OC']) for i,r in Aggr_DF.iterrows()]

    Aggr_DF['Proc_EC'] = [len(HSIP_DF[[(i[-1])==r['District'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0  and not pd.isnull(r['CompletionDate']) and r['EUAC']!=0 and r['EUAB_OC']!=0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC'])
                                      for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['Proc_EC_BC>1'] = [len(HSIP_DF[[(i[-1])==r['District'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate'])  and r['EUAC']!=0 and r['EUAB_OC']!=0  and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC']) and r['BC_EC']>1
                                      for j,r in HSIP_DF.iterrows()]]) for i in Index]

    Aggr_DF['EUAC_EC'] = [sum(HSIP_DF[[(i[-1])==r['District'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate'])  and r['EUAC']!=0 and r['EUAB_OC']!=0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC'])
                                      for j,r in HSIP_DF.iterrows()]]['EUAC']) for i in Index]
    
    Aggr_DF['EUAB_EC'] = [sum(HSIP_DF[[(i[-1])==r['District'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate'])  and r['EUAC']!=0 and r['EUAB_OC']!=0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC'])
                                      for j,r in HSIP_DF.iterrows()]]['EUAB_EC']) for i in Index]

    Aggr_DF['BC_EC'] = [r['EUAB_EC']/(r['EUAC_EC'] or not r['EUAC_EC']) for i,r in Aggr_DF.iterrows()]


    Aggr_DF['HSIP_ID_OC'] = [';'.join([str(ID) for ID in list(HSIP_DF[[(i[-1])==r['District'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate'])  and r['EUAC']!=0 and r['EUAB_OC']!=0
                                                                       for j,r in HSIP_DF.iterrows()]]['ContNum'])]) for i in Index]

    Aggr_DF['HSIP_ID_EC'] = [';'.join([str(ID) for ID in list(HSIP_DF[[(i[-1])==r['District'] and
                         len(r['BeforePeriod'].split(';'))>=2 and
                         len(r['AfterPeriod' ].split(';'))>=2 and
                         r['CompletionAmount']>0 and not pd.isnull(r['CompletionDate'])  and r['EUAC']!=0 and r['EUAB_OC']!=0 and r['EUAB_EC']!=0 and not math.isnan(r['EUAB_EC'])
                                                                       for j,r in HSIP_DF.iterrows()]]['ContNum'])]) for i in Index]
    
    
    Aggr_DF.index = Index
    #Aggr_DF['Total'] = [sum([r[c] for c in ['Tot','W Tot Award','Tot.Awrd.Amount','3Ys BA','Proc','EUAC','EUAB_OC','EUAB_EC','BC_OC','BC_EC']]) for i,r in Aggr_DF.iterrows()]
    TotL = []
    for c in Aggr_DF.columns:
        if c in ['HSIP_ID_EC','HSIP_ID_OC']:
            TotL.append(0)
        else:
            TotL.append(sum(Aggr_DF[c]))
    Aggr_DF.loc['Total'] = TotL
    Aggr_DF.set_value('Total','BC_OC',Aggr_DF.loc['Total']['EUAB_OC']/Aggr_DF.loc['Total']['EUAC_OC'])
    Aggr_DF.set_value('Total','BC_EC',Aggr_DF.loc['Total']['EUAB_EC']/Aggr_DF.loc['Total']['EUAC_EC'])
    Ex_FN = OutDir + '\\' + FN + '.xlsx'
    Pn_FN = OutDir + '\\' + FN + '.png'
    Aggr_DF.to_excel(Ex_FN)
    Agg_BoxPlot(HSIP_DF,Aggr_DF,Pn_FN)
    return(Aggr_DF)

#Plots and Figures
def PlotHSIP(df,df_sum,ID,Out):
    import matplotlib
    import scipy.stats as st
    from scipy.stats import ttest_ind
    
    Years = list(df[df.Period != 'Service'].index)
    BP = list(df.index[df.Period == 'BeforePeriod'])
    AP = list(df.index[(df.Period == 'AfterPeriod')])
    CP = list(df.index[(df.Period == 'CosntPeriod')])
    def YRange(Y):
        ymax = 0.1
        ymin = -0.1
        for s in Y.keys():
            l = list([i for i in Y[s] if not math.isnan(i)])
            lmin = list([i for i in Y[s] if not math.isnan(i)])
            if np.var(Y[s][BP])>0:
                intv1 = IntervalEst(Y[s][BP])
                if not math.isnan(intv1[1]):
                    l.append(intv1[1])
                if not math.isnan(intv1[0]):
                    lmin.append(intv1[0])
            if np.var(Y[s][AP])>0:
                intv2 = IntervalEst(Y[s][AP])
                if not math.isnan(intv2[1]):
                    l.append(intv2[1])
                if not math.isnan(intv2[0]):
                    lmin.append(intv2[0])
            l.append(ymax)
            lmin.append(ymin)
            ymin = min(lmin)
            ymax = max(l)
        
        if ymax<0.1 or math.isnan(ymax):
            ymax = 0.1
        if ymin>-0.1 or math.isnan(ymin):
            ymin = -0.1
        yinc = (ymax-ymin) * 0.1
        return([ymin-yinc,ymax+yinc])
    def IntervalEst(L):
        L = [i for i in L if not math.isnan(i)]
        intv = st.t.interval(0.95, len(L)-1, loc=np.mean(L), scale=st.sem(L))
        return(intv)
    plt.figure(figsize=(6.67,7.5))
    Marker = {'K':'o','A':'x','B':'v','EC':'v','OC':'o'}
    Col = {'K':'red','A':'pink','B':'brown','OC':'red','EC':'blue'}
    Leg_Hand1 = []
    for s in ['K','A','B']:
        Leg_Hand1.append(plt.Line2D((0,1),(0,0), color=Col[s]))
    Leg_Hand2 = []
    for s in ['OC','EC']:
        Leg_Hand2.append(plt.Line2D((0,1),(0,0), color=Col[s], marker=Marker[s]))

    plt.subplot(311)
    plt.title("Contract Number: " + str(ID) +'\nK Crashes')
    X = Years;Y = {'EC':df.K_EC[X],'OC':df.K_OC[X]}
    plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    plt.gca().set_xlim([min(X)-1,max(X)+1])
    plt.gca().set_ylim(YRange(Y))
    plt.gca().xaxis.set_ticks([])
    for s in ['EC','OC']:
        plt.plot(X,Y[s],Marker[s],color=Col[s])
        plt.gca().axhline(xmin=(min(BP)-min(X)+0.5)/(max(X)-min(X)+2) ,
                          xmax =(max(BP)-min(X)+1.5)/(max(X)-min(X)+2) ,
                          y=np.mean(Y[s][BP]),color=Col[s])
        plt.gca().axhline(xmin=(min(AP)-min(X)+0.5)/(max(X)-min(X)+2) ,
                          xmax =(max(AP)-min(X)+1.5)/(max(X)-min(X)+2) ,
                          y=np.mean(Y[s][AP]),color=Col[s])
        plt.plot([min(CP)-0.5,max(CP)+0.5],[np.mean(Y[s][BP]),np.mean(Y[s][AP])],color=Col[s])
        if np.var(Y[s][BP])>0:
            intv = IntervalEst(Y[s][BP])
            if not math.isnan(intv[0]) and not math.isnan(intv[1]):
                plt.gca().fill_between([min(BP)-0.5,max(BP)+0.5], intv[0], intv[1], facecolor= Col[s], alpha=0.5)
        if np.var(Y[s][AP])>0:
            intv = IntervalEst(Y[s][AP])
            if np.var(Y[s][BP])>0 and ttest_ind(Y[s][BP], Y[s][AP], equal_var=False)[1]<0.05:
                if not math.isnan(intv[0]) and not math.isnan(intv[1]):
                    plt.gca().fill_between([min(AP)-0.5,max(AP)+0.5], intv[0], intv[1], facecolor= 'g', alpha=0.5)
            else:
                if not math.isnan(intv[0]) and not math.isnan(intv[1]):
                    plt.gca().fill_between([min(AP)-0.5,max(AP)+0.5], intv[0], intv[1], facecolor= Col[s], alpha=0.5)
    #plt.gca().add_patch(matplotlib.patches.Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], closed=True, facecolor='red'))        
    plt.grid(True)
    plt.gca().fill_between([min(CP)-0.5,max(CP)+0.5], min([-0.1,YRange(Y)[0]]), max([ 0.1,YRange(Y)[1]]), facecolor= 'yellow', alpha=0.5)
    #for i,s in enumerate(['{}: {:0.3f}'.format(s,np.mean(Y[s])) for s in ['K','A','B']]):
    #    plt.gca().text(min(X)-0.9, ymax-yinc*(i+1), s)
    plt.legend(Leg_Hand2,['Obs.','Exp.'],frameon = False,fancybox=True)
    plt.gca().text(np.mean(CP),YRange(Y)[1]*0.8,'Construction',ha='center', va='center') 

    plt.subplot(312)
    plt.title('A Crashes')
    X = Years;Y = {'EC':df.A_EC[X],'OC':df.A_OC[X]}
    plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    plt.gca().set_xlim([min(X)-1,max(X)+1])
    plt.gca().set_ylim(YRange(Y))
    plt.gca().xaxis.set_ticks([])
    for s in ['EC','OC']:
        plt.plot(X,Y[s],Marker[s],color=Col[s])
        plt.gca().axhline(xmin=(min(BP)-min(X)+0.5)/(max(X)-min(X)+2) ,
                          xmax =(max(BP)-min(X)+1.5)/(max(X)-min(X)+2) ,
                          y=np.mean(Y[s][BP]),color=Col[s])
        plt.gca().axhline(xmin=(min(AP)-min(X)+0.5)/(max(X)-min(X)+2) ,
                          xmax =(max(AP)-min(X)+1.5)/(max(X)-min(X)+2) ,
                          y=np.mean(Y[s][AP]),color=Col[s])
        plt.plot([min(CP)-0.5,max(CP)+0.5],[np.mean(Y[s][BP]),np.mean(Y[s][AP])],color=Col[s])
        if np.var(Y[s][BP])>0:
            intv = IntervalEst(Y[s][BP])
            if not math.isnan(intv[0]) and not math.isnan(intv[1]):
                plt.gca().fill_between([min(BP)-0.5,max(BP)+0.5], intv[0], intv[1], facecolor= Col[s], alpha=0.5)
        if np.var(Y[s][AP])>0:
            intv = IntervalEst(Y[s][AP])
            if np.var(Y[s][BP])>0 and ttest_ind(Y[s][BP], Y[s][AP], equal_var=False)[1]<0.05:
                if not math.isnan(intv[0]) and not math.isnan(intv[1]):
                    plt.gca().fill_between([min(AP)-0.5,max(AP)+0.5], intv[0], intv[1], facecolor= 'g', alpha=0.5)
            else:
                if not math.isnan(intv[0]) and not math.isnan(intv[1]):
                    plt.gca().fill_between([min(AP)-0.5,max(AP)+0.5], intv[0], intv[1], facecolor= Col[s], alpha=0.5)

    plt.grid(True)
    plt.gca().fill_between([min(CP)-0.5,max(CP)+0.5], min([-0.1,YRange(Y)[0]]), max([ 0.1,YRange(Y)[1]]), facecolor= 'yellow', alpha=0.5)
    #plt.gca().text(min(X)-0.9, ymax-yinc*1, 'K: {:0.3f};   EUAC: ${:,.2f}'.format(np.mean(Y['K']),df_sum.loc[2]['EUAC']))
    #plt.gca().text(min(X)-0.9, ymax-yinc*2, 'A: {:0.3f};   EUAB_EC: ${:,.2f}'.format(np.mean(Y['A']),df_sum.loc[2]['EUAB_EC']))
    #if df_sum.loc[2]['EUAB_EC'] > 0:
    #    plt.gca().text(min(X)-0.9, ymax-yinc*3, 'B: {:0.3f};   B/C: {:,.2f}'.format(np.mean(Y['B']),df_sum.loc[2]['EUAB_EC']/df_sum.loc[2]['EUAC']))
    #else:
    #    plt.gca().text(min(X)-0.9, ymax-yinc*3, 'B: {:0.3f};   B/C: N.A.'.format(np.mean(Y['B'])))

        
    plt.subplot(313)
    plt.title('B Crashes')
    X = Years;Y = {'OC':df.B_OC[X],'EC':df.B_EC[X]}
    plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
    plt.gca().set_xlim([min(X)-1,max(X)+1])
    plt.gca().set_ylim(YRange(Y))
    plt.gca().xaxis.set_ticks(np.arange(min(X), max(X)+1, 1))
    plt.xticks(rotation=45)
    for s in ['EC','OC']:
        plt.plot(X,Y[s],Marker[s],color=Col[s])
        plt.gca().axhline(xmin=(min(BP)-min(X)+0.5)/(max(X)-min(X)+2) ,
                          xmax =(max(BP)-min(X)+1.5)/(max(X)-min(X)+2) ,
                          y=np.mean(Y[s][BP]),color=Col[s])
        plt.gca().axhline(xmin=(min(AP)-min(X)+0.5)/(max(X)-min(X)+2) ,
                          xmax =(max(AP)-min(X)+1.5)/(max(X)-min(X)+2) ,
                          y=np.mean(Y[s][AP]),color=Col[s])
        plt.plot([min(CP)-0.5,max(CP)+0.5],[np.mean(Y[s][BP]),np.mean(Y[s][AP])],color=Col[s])
        if np.var(Y[s][BP])>0:
            intv = IntervalEst(Y[s][BP])
            if not math.isnan(intv[0]) and not math.isnan(intv[1]):
                plt.gca().fill_between([min(BP)-0.5,max(BP)+0.5], intv[0], intv[1], facecolor= Col[s], alpha=0.5)
        if np.var(Y[s][AP])>0:
            intv = IntervalEst(Y[s][AP])
            if np.var(Y[s][BP])>0 and ttest_ind(Y[s][BP], Y[s][AP], equal_var=False)[1]<0.05:
                if not math.isnan(intv[0]) and not math.isnan(intv[1]):
                    plt.gca().fill_between([min(AP)-0.5,max(AP)+0.5], intv[0], intv[1], facecolor= 'g', alpha=0.5)
            else:
                if not math.isnan(intv[0]) and not math.isnan(intv[1]):
                    plt.gca().fill_between([min(AP)-0.5,max(AP)+0.5], intv[0], intv[1], facecolor= Col[s], alpha=0.5)
        #test_ind(Y[s][BP], Y[s][AP], equal_var=False)[1]
    plt.grid(True)
    #plt.gca().axhline(xmin=min(BP) ,xmax =max(BP) ,y=np.mean(Y['OC'][BP]))
    #plt.gca().axhline(y=np.mean(Y[s]),color = Col[s])
    plt.gca().fill_between([min(CP)-0.5,max(CP)+0.5], min([-0.1,YRange(Y)[0]]), max([ 0.1,YRange(Y)[1]]), facecolor= 'yellow', alpha=0.5)
    #for i,s in enumerate(['{}: {:0.3f}'.format(s,np.mean(Y[s])) for s in ['K','A','B']]):
    #    plt.gca().text(min(X)-0.9, ymax-yinc*(i+1), s)
    #plt.legend(Leg_Hand1,[r'$\bar \mathrm{K}\ $',r'$\bar \mathrm{A}\ $',r'$\bar \mathrm{B}\ $'],frameon = False,fancybox=True)

    ymax = YRange(Y)[1]
    ymin = YRange(Y)[0]
    yinc = (ymax-ymin) * 0.1
    #plt.gca().text(min(X)-0.9, ymax-yinc*1, 'EUAC: ${:,.2f}'.format(df_sum.loc[2]['EUAC']))
    #plt.gca().text(min(X)-0.9, ymax-yinc*2, 'EUAB_OC: ${:,.2f}'.format(df_sum.loc[2]['EUAB_OC']))
    if not math.isnan(df_sum.loc[2]['BC_OC']):
        plt.gca().text(min(X)-0.9, ymax-yinc*1, 'Naive B/C: {:,.2f}'.format(df_sum.loc[2]['BC_OC']))
    else:
        plt.gca().text(min(X)-0.9, ymax-yinc*1, 'Naive B/C: N.A.')
    if not math.isnan(df_sum.loc[2]['BC_EC']):
        plt.gca().text(min(X)-0.9, ymax-yinc*2, 'EB B/C: {:,.2f}'.format(df_sum.loc[2]['BC_EC']))
    else:
        plt.gca().text(min(X)-0.9, ymax-yinc*2, 'EB B/C: N.A.')
    
    
    #handles, labels = plt.gca().get_legend_handles_labels()
    #plt.gcf().legend(handles, labels, bbox_to_anchor=(0.8, 0.8),fancybox=True, framealpha=0.5)
    plt.tight_layout()
    plt.savefig(Out,transparent=True,dpi=1200)
    #plt.savefig(Out,transparent=False)
    plt.close()
def PlotCrashType(df3,FN,ID,TargetCrashTypes):
    left, width = .1, .85
    bottom, height = .1, .85
    right = left + width
    top = bottom + height    

    BYs = list(set(df3[df3.Period=='BeforePeriod']['Year']))
    BYs.sort()
    AYs = list(set(df3[df3.Period=='AfterPeriod']['Year']))
    AYs.sort()
    if len(BYs)==0 or len(AYs)==0:
        return
    df4 = df3[df3.Period == 'BeforePeriod']
    df5 = df3[df3.Period == 'AfterPeriod']
    df4 = CrashTypeDF(df4)
    for c in df4.columns:
        df4[c] = [float(v)/len(BYs) for v in df4[c]]
    df5 = CrashTypeDF(df5)
    for c in df5.columns:
        df5[c] = [float(v)/len(AYs) for v in df5[c]]
    DFBefore = df4
    DFAfter = df5
    ymin = 0
    ymax = max([max([max(DFBefore[c]) for c in DFBefore.columns]),
                max([max(DFAfter[c])  for c in DFAfter.columns ])])
    if ymax == 0:
        return
    #ymax = ymax * 1.1
    Conv_Dict = {
        'animal':'ANM',
        'fixed object':'FO',
        'head on':'HO',
        'overturned':'OT',
        'other object':'OO',
        'other non collision':'ONC',
        'rear end':'RE',
        'angle':'ANG',
        'turning':'TUR',
        'sideswipe opposite direction':'SSWO',
        'sideswipe same direction':'SSWS',
        'parked motor vehicle':'PMV',
        'pedestrian':'PED'
    }
    TargetCrashTypes = [s.lower() for s in TargetCrashTypes]
    TargetCrashTypes = [Conv_Dict[s] for s in TargetCrashTypes if s in Conv_Dict.keys()]
    plt.figure(figsize=(6*6.67/3.75,6))
    #plt.gcf().suptitle("HSIP ID: " + str(ID), fontsize=14)

    plt.subplot(211)
    
    #fig, ax = plt.subplots(figsize=(6,3))  
    #axes = plt.gca()
    plt.gca().set_ylim([ymin,ymax])    
    DFBefore = RemoveTotals(DFBefore)
    DFAfter = RemoveTotals(DFAfter)
    df = DFBefore
    df.columns = [Conv_Dict[c] for c in df.columns]
    sev = df.index
    margin_bottom = np.zeros(len(df.columns))
    
    #cmap = mcolors.LinearSegmentedColormap('redgreen',  [(0,'#FF0000'),(1,'#74C476')], 100)
    #colors = [cmap(i) for i in np.linspace(0, 1, 5)]
    colors = ["red", "brown","coral","yellow","green"]

    for num, s in enumerate(sev):
        values = list(df.loc[s])
        df.loc[s].plot.bar(ax=plt.gca(), stacked=True, 
                                    bottom = margin_bottom, label=s,color = colors[num])
        margin_bottom += values
    plt.legend(loc='upper left',frameon = False,fancybox=True,ncol=3)
    plt.grid()
    #plt.gca().text(.5,.9,'Before Period',horizontalalignment='center',transform=plt.gca().transAxes)
    plt.title("HSIP ID: " + str(ID) + '\n Before Period')
    plt.gca().text(right, top, str(len(BYs)) + ' Years: ' + str(BYs[0]) + '-' + str(BYs[-1]),
        horizontalalignment='right',
        verticalalignment='top',
        transform=plt.gca().transAxes)

    for xtick in plt.gca().get_xticklabels():
        if xtick.properties()['text'] in TargetCrashTypes:
            xtick.set_backgroundcolor('y')
    
    #plt.show()
    plt.subplot(212)
    #fig, ax = plt.subplots(figsize=(6,3))  
    plt.gca().set_ylim([ymin,ymax])    
    df = DFAfter
    df.columns = [Conv_Dict[c] for c in df.columns]
    sev = df.index
    margin_bottom = np.zeros(len(df.columns))

    for num, s in enumerate(sev):
        values = list(df.loc[s])
        df.loc[s].plot.bar(ax=plt.gca(), stacked=True, 
                                    bottom = margin_bottom, label=s,color = colors[num])
        margin_bottom += values
    #plt.legend(loc='center left')
    plt.grid()
    plt.title('After Period')
    plt.gca().text(right, top, str(len(AYs)) + ' Years: ' + str(AYs[0]) + '-' + str(AYs[-1]),
        horizontalalignment='right',
        verticalalignment='top',
        transform=plt.gca().transAxes)
    
    for xtick in plt.gca().get_xticklabels():
        if xtick.properties()['text'] in TargetCrashTypes:
            xtick.set_backgroundcolor('y')
                
    plt.tight_layout()
    plt.savefig(FN,transparent=True,dpi=1200)
    plt.close()
def AdjustExtend(ext,distance):
    ext.XMax += distance
    ext.XMin -= distance
    ext.YMax += distance
    ext.YMin -= distance   
    return(ext)
def AppendExtent(ext,app_ext):
    if ext == '':
        return(app_ext)
    else:
        ext.XMax = max([ext.XMax,app_ext.XMax])
        ext.XMin = min([ext.XMin,app_ext.XMin])
        ext.YMax = max([ext.YMax,app_ext.YMax])
        ext.YMin = min([ext.YMin,app_ext.YMin])
        return(ext)
def AddFCtoDataFrame(DF,FC,Position = 'AUTO_ARRANGE',Visible= True):
    layer = ''
    try:
        layer = DF.addDataFromPath(FC)
        layer.visible = Visible
    except:
        print(FC)
        pass
    return(layer)
def AddFCtoDataFrameGroup(DF,Group,FC,Position = 'AUTO_ARRANGE',Visible= True):
    layer = ''
    try:
        layer = DF.addDataFromPath(FC)
        DF.addLayerToGroup(add_layer_or_layerfile=layer,target_group_layer=Group,add_position=Position)
        DF.removeLayer(layer)
        layer = DF.listLayers(os.path.basename(FC))[0]
        layer.visible = Visible
    except:
        pass
    return(layer)
def CreateMapandProject(GDB,Years,APRX,Cont_DF,SegSymbology,IntSymbology,IntSymbology2,BeforeSymbology,AfterSymbology,OutDir):
    p = os.path.basename(GDB).split('_')[1]
    SegFC = GDB + '\\Seg_' + p
    IntFC = GDB + '\\Int_' + p
    HSIP_SegFC = GDB + '\\HSIP_Seg'
    HSIP_IntFC = GDB + '\\HSIP_Int'


    RteFN = {year:os.path.join(GDB,'HWY' + str(year) + '_route') for year in Years}
    IntFN = {year:os.path.join(GDB,'HWY' + str(year) + '_inter') for year in Years}
    TabFN = {year:os.path.join(GDB,'HWY' + str(year) + '_table') for year in Years}

    NumSeg = 0
    NumInt = 0
    try: NumSeg = int(str(arcpy.GetCount_management(SegFC)))
    except: pass
    try: NumInt = int(str(arcpy.GetCount_management(IntFC)))
    except: pass

    NumHSIP_Seg = 0
    NumHSIP_Int = 0
    try: NumHSIP_Seg = int(str(arcpy.GetCount_management(HSIP_SegFC)))
    except: pass
    try: NumHSIP_Int = int(str(arcpy.GetCount_management(HSIP_IntFC)))
    except: pass
    
    p = str(p)
    mxd = arcpy.mp.ArcGISProject(APRX)
    df = mxd.listMaps('Site')[0]
    df2 = mxd.listMaps('State')[0]
    
    LG_BaseInt = df.listLayers("Base Intersection Data")[0]
    LG_BaseSeg = df.listLayers("Base Roadway Data")[0]
    LG_Sites   = df.listLayers("Geocoded Sites")[0]
    LG_SegAtt  = df.listLayers("Segment Attribute Data")[0]
    LG_IntAtt  = df.listLayers("Intersection Attribute Data")[0]
    LG_Crash   = df.listLayers("Crash Data")[0]

    LG_BaseInt.visible = False
    LG_BaseSeg.visible = False
    LG_Sites.visible = True
    LG_SegAtt.visible = False
    LG_IntAtt.visible = False
    LG_Crash.visible = False
    BY = []
    AY = []
    CY = []
    try:
        BY = [int(y) for y in Cont_DF.loc[(p)]['BeforePeriod'].split(';')]
        AY = [int(y) for y in Cont_DF.loc[(p)]['AfterPeriod'].split(';')]
        CY = [int(y) for y in Cont_DF.loc[(p)]['ConstPeriod'].split(';')]
    except:
        pass
    
    SegLayer = AddFCtoDataFrameGroup(df,LG_Sites,SegFC,'AUTO_ARRANGE',True)
    IntLayer = AddFCtoDataFrameGroup(df,LG_Sites,IntFC,'AUTO_ARRANGE',True)

    HSIP_SegLayer = AddFCtoDataFrameGroup(df,LG_Sites,HSIP_SegFC,'AUTO_ARRANGE',True)
    HSIP_IntLayer = AddFCtoDataFrameGroup(df,LG_Sites,HSIP_IntFC,'AUTO_ARRANGE',True)

    F2P = SegFC
    if NumSeg>0:
        F2P = common.CreateOutPath(SegFC,'F2P',Extension = '')
        arcpy.FeatureToPoint_management (SegFC, F2P, 'CENTROID')
    
    SegLayer2 = AddFCtoDataFrame(df2,F2P,'AUTO_ARRANGE',True)
    IntLayer2 = AddFCtoDataFrame(df2,IntFC,'AUTO_ARRANGE',True)

    for year in Years:
        AddFCtoDataFrameGroup(df,LG_BaseSeg,RteFN[year],'AUTO_ARRANGE',True)
        AddFCtoDataFrameGroup(df,LG_BaseInt,IntFN[year],'AUTO_ARRANGE',True)

        AddFCtoDataFrameGroup(df,LG_SegAtt,SegFC + '_' + str(year),'AUTO_ARRANGE',True)
        AddFCtoDataFrameGroup(df,LG_IntAtt,IntFC + '_' + str(year) + '_points','AUTO_ARRANGE',True)
        l1 = AddFCtoDataFrameGroup(df,LG_Crash,SegFC + '_' + str(year) + '_Crash','AUTO_ARRANGE',True)
        l2 = AddFCtoDataFrameGroup(df,LG_Crash,IntFC + '_' + str(year) + '_points_Crash' ,'AUTO_ARRANGE',True)
        if year in BY:
            if l1!='':
                arcpy.ApplySymbologyFromLayer_management (l1,BeforeSymbology)
            if l2!='':
                arcpy.ApplySymbologyFromLayer_management (l2,BeforeSymbology)
        if year in AY:
            if l1!='':
                arcpy.ApplySymbologyFromLayer_management (l1,AfterSymbology)
            if l2!='':
                arcpy.ApplySymbologyFromLayer_management (l2,AfterSymbology)
    layout = mxd.listLayouts()[0]
    mapframe = layout.listElements()[1]
    mapframe2 = layout.listElements()[0]

    ext = ''
    if NumSeg>0:
        ext = AppendExtent(ext,arcpy.Describe(SegFC).extent.projectAs(arcpy.SpatialReference(102672)))
    if NumInt>0:
        ext = AppendExtent(ext,arcpy.Describe(IntFC).extent.projectAs(arcpy.SpatialReference(102672)))
    if NumHSIP_Int>0:
        ext = AppendExtent(ext,arcpy.Describe(HSIP_IntFC).extent.projectAs(arcpy.SpatialReference(102672)))
    if NumHSIP_Seg>0:
        ext = AppendExtent(ext,arcpy.Describe(HSIP_SegFC).extent.projectAs(arcpy.SpatialReference(102672)))

    if ext!='':
        ext = ext.projectAs(arcpy.SpatialReference(102672))
        ext = AdjustExtend(ext,600)
        mapframe.camera.setExtent(ext)
    
    try:
        arcpy.ApplySymbologyFromLayer_management (SegLayer, SegSymbology)
    except:pass
    try:
        arcpy.ApplySymbologyFromLayer_management (IntLayer, IntSymbology)
    except:pass
    try:
        arcpy.ApplySymbologyFromLayer_management (SegLayer2, IntSymbology2)
    except:pass
    try:
        arcpy.ApplySymbologyFromLayer_management (IntLayer2, IntSymbology2)
    except:pass
    
    ImageName = OutDir + '\\HSIP_' + p + '_Site.jpg'
    mapframe.exportToJPEG(ImageName)
    ImageName = OutDir + '\\HSIP_' + p + '_State.jpg'
    mapframe2.exportToJPEG(ImageName)
    mxd.saveACopy (OutDir + '\\HSIP_' + p + '.aprx')


def Agg_BoxPlot(Cont_DF,Agg_DF,OutFN):
    plt.figure(figsize=(10,8))
    x_OC = []
    x_EC = []
    for d in list(Agg_DF.index)[:-1]:
        df_OC = Cont_DF[Cont_DF.ContNum.isin(Agg_DF.loc[d].HSIP_ID_OC.split(';'))]
        x_OC.append(df_OC.BC_OC)
        df_EC = Cont_DF[Cont_DF.ContNum.isin(Agg_DF.loc[d].HSIP_ID_EC.split(';'))]
        x_EC.append(df_EC.BC_EC)

    plt.subplot(211)
    #plt.gca().set_ylim([-60,60])
    plt.boxplot(x=x_OC,positions=range(1,len(list(Agg_DF.index))),showfliers =False,labels=["" for i in range(1,len(list(Agg_DF.index)))])
    plt.gca().set_xlim([0,len(list(Agg_DF.index))])
    #plt.xticks(rotation=45)
    #plt.gca().xaxis.set_ticks([])
    plt.hlines(1,0,len(list(Agg_DF.index)))
    plt.ylabel('Naive BC Ratio')
    plt.grid()

    plt.subplot(212)
    #plt.gca().set_ylim([-60,60])
    plt.boxplot(x=x_EC,positions=range(1,len(list(Agg_DF.index))),showfliers =False,labels=list(Agg_DF.index)[:-1])
    plt.gca().set_xlim([0,len(list(Agg_DF.index))])
    plt.xticks(rotation=45)
    plt.hlines(1,0,len(list(Agg_DF.index)))
    plt.ylabel('EB BC Ratio')
    plt.grid()
    
    plt.savefig(OutFN,transparent=True,dpi=1200)
    plt.show()


#IL SHSP
def FindRatio(Y,YT):
    def objfun(x):
        return(sum([abs(y-float(yt)/x) for y,yt in zip(Y,YT)]))
    res = scipy.optimize.minimize(objfun, np.mean(YT)/np.mean(Y), method='nelder-mead',options={'xtol': 1e-8, 'disp': False})
    x = res.x[0]
    #ratio = np.arange(x*0.5,x*1.5,x*0.05)
    #plt.plot(ratio,[objfun(r) for r in ratio])
    #plt.vlines(x,plt.ylim()[0],plt.ylim()[1])
    #plt.show()
    return(x)
def AdjustColumnWidth(FN):
    import openpyxl
    wb = openpyxl.load_workbook(filename = FN)        
    for worksheet in wb.worksheets: 
        i= 1
        for col in worksheet.columns:
            max_length = 5
            cname = col[0].column
            for cell in col:
                try: # Necessary to avoid error on empty cells
                    if len(str(cell.value)) > max_length:
                        max_length = len(cell.value)
                except:
                    pass
                cell.alignment = openpyxl.styles.Alignment(horizontal='center')
            adjusted_width = (max_length + 2) * 1.2
            if i>1:
                adjusted_width = 7
            worksheet.column_dimensions[cname].width = adjusted_width
            i += 1
    wb.save(FN)
def SHSP_NationalTrend_All(Years,png_out):
    y = [2016 ,2015 ,2014 ,2013 ,2012 ,2011 ,2010 ,2009 ,2008 ,2007 ,2006 ,2005 ,2004 ,2003 ,2002 ,2001 ,2000 ,1999 ,1998 ,1997 ,1996 ,1995 ,1994 ]
    k = [34439,32539,30056,30202,31006,29867,30296,30862,34172,37435,38648,39252,38444,38477,38491,37862,37526,37140,37107,37324,37494,37241,36254]
    k = [37461,35485,32744,32893,33782,32479,32999,33883,37423,41259,42708,43510,42836,42884,43005,42196,41945,41717,41501,42013,42065,41817,40716]
    FARS_DF = pd.DataFrame()
    FARS_DF['KCrashes'] = k
    FARS_DF.index = y
    FARS_DF = FARS_DF.sort_index()
    FARS_DF = FARS_DF.loc[Years]
    X = list(FARS_DF.index)
    Y = list(FARS_DF.KCrashes)
    plt.figure(figsize=(8, 4), dpi=300, facecolor='w', edgecolor='k')
    plt.plot(X,Y,'-o')
    #plt.xlim(2006,2017)
    plt.xticks(X,[str(x) for x in X],rotation=90)
    plt.gca().set_yticklabels(['{:,.0f}'.format(y) for y in plt.gca().get_yticks()])
    plt.ylabel('Fatalities')
    plt.title('National - All Time')
    plt.grid()
    plt.savefig(png_out,transparent=True,dpi=1200)
    plt.close()
def SHSP_StateTrend_All(Crash_DF,png_out):
    y = [2016 ,2015 ,2014 ,2013 ,2012 ,2011 ,2010 ,2009 ,2008 ,2007 ,2006 ,2005 ,2004 ,2003 ,2002 ,2001 ,2000 ,1999 ,1998 ,1997 ,1996 ,1995 ,1994 ]
    k = [34439,32539,30056,30202,31006,29867,30296,30862,34172,37435,38648,39252,38444,38477,38491,37862,37526,37140,37107,37324,37494,37241,36254]
    k = [37461,35485,32744,32893,33782,32479,32999,33883,37423,41259,42708,43510,42836,42884,43005,42196,41945,41717,41501,42013,42065,41817,40716]

    FARS_DF = pd.DataFrame()
    FARS_DF['KCrashes'] = k
    FARS_DF.index = y
    FARS_DF = FARS_DF.sort_index()
    FARS_DF = FARS_DF.loc[Years]
    X = list(set(Crash_DF.Crash_Year))
    X = [x+2000 for x in X]
    X.sort()
    FARS_DF = FARS_DF.loc[X]
    Y = [Crash_DF[Crash_DF.Crash_Year==x-2000]['Total_killed'].sum() for x in X]
    YT = list(FARS_DF.KCrashes)
    r = FindRatio(Y,YT)
    YT = [float(yt)/r for yt in YT]
    plt.figure(figsize=(6, 4), dpi=300, facecolor='w', edgecolor='k')
    p1 = plt.plot(X,Y,'-o',label='State')
    p2 = plt.plot(X,YT,'--x',label ='Normalized National ({:0.2f}%)'.format(100.0/r))
    plt.xlim(X[0]-1,X[1]+1)
    plt.xticks(X,[str(x) for x in X],rotation=0)
    plt.gca().set_yticklabels(['{:,.0f}'.format(y) for y in plt.gca().get_yticks()])
    plt.ylabel('Fatalities')
    plt.title('Statewide')
    plt.grid()
    plt.plot([], [], ' ', label='Correlation: {:0.2f}'.format(np.corrcoef(x=Y,y=YT)[0][1]))
    plt.legend(loc='upper right',fancybox=True,framealpha=0.5, prop={'size': 9})
    plt.tight_layout()
    plt.savefig(png_out,transparent=True,dpi=1200)
    plt.close()
def SHSP_EATrend(Crash_DF,EADF,png_out):
    X = list(set(Crash_DF.Crash_Year))
    X = [x+2000 for x in X]
    X.sort()
    for i,r in EADF.iterrows():
        Y  = [Crash_DF[(Crash_DF.Crash_Year==x-2000) & (Crash_DF[r.CrashDataField]=='X')]['KA'].sum() for x in X]
        YT = [Crash_DF[(Crash_DF.Crash_Year==x-2000)]['KA'].sum() for x in X]
        ratio = FindRatio(Y,YT)
        YT = [float(yt)/ratio for yt in YT]
        plt.figure(figsize=(6, 4), dpi=300, facecolor='w', edgecolor='k')
        plt.plot(X,Y,'-o',label='Emphasis Area')
        plt.plot(X,YT,'--x',label='Normalized State ({:0.2f}%)'.format(100.0/ratio))
        plt.xlim(X[0]-1,X[1]+1)
        plt.xticks(X,[str(x) for x in X],rotation=0)
        plt.gca().set_yticklabels(['{:,.0f}'.format(y) for y in plt.gca().get_yticks()])
        plt.ylabel('Fatalities and A Injuries')
        plt.title(r.Name)
        plt.grid()
        plt.plot([], [], ' ', label='Correlation: {:0.2f}'.format(np.corrcoef(x=Y,y=YT)[0][1]))
        plt.legend(loc='upper right',fancybox=True,framealpha=0.5, prop={'size': 7})
        plt.tight_layout()
        plt.savefig(png_out(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()
def SHSP_EAJAccard(Crash_DF,EADF,png_out):
    n = len(EADF.Name)
    Jaccard_M = numpy.zeros(shape=(n,n))
    for i1,r1 in EADF.iterrows():
        df = pd.DataFrame(columns=['Jaccard_Index'])
        for i2,r2 in EADF.iterrows():
            if i2!=i1:
                I = Crash_DF[(Crash_DF[r1.CrashDataField]=='X') & (Crash_DF[r2.CrashDataField]=='X')]['KA'].sum()
                U = Crash_DF[(Crash_DF[r1.CrashDataField]=='X') | (Crash_DF[r2.CrashDataField]=='X')]['KA'].sum()
                try:
                    df.loc[r2.Name] = float(I)/float(U)
                except:
                    df.loc[r2.Name] = 0
        df =df.sort_values('Jaccard_Index',ascending=False)
        df.columns.name = r1.Name
        plt.figure(figsize=(4, 6), dpi=300, facecolor='w', edgecolor='k')
        plt.imshow(df, cmap=plt.cm.Reds, interpolation='nearest',aspect='equal')
        plt.xticks([0],[df.columns.name],rotation=90)
        plt.yticks(range(0,n-1),df.index,rotation=0)
        plt.grid()
        plt.colorbar()
        plt.title('Jaccard Index')
        #plt.annotate('Jaccard Index is defined as the intersection over the union.', (0,0), (-150, -180), xycoords='axes fraction', textcoords='offset points', va='top')
        plt.tight_layout()
        plt.savefig(png_out(r1.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()
def SHSP_EABarStateLine(Crash_DF,Field,EADF,png_out):
    df = pd.DataFrame(Crash_DF[Field].value_counts(True))
    df = df.sort_index(ascending=False)
    for i,r in EADF.iterrows():
        plt.figure(figsize=(6, 4), dpi=300, facecolor='w', edgecolor='k')
        eadf = pd.DataFrame(Crash_DF[Crash_DF[r.CrashDataField]=='X'][Field].value_counts(True))
        eadf = eadf.loc[df.index]
        p1 = plt.bar(range(len(eadf)),eadf[Field],align='center')
        plt.xticks(range(len(df)),df.index,rotation=90)
        p2, = plt.plot(range(len(df)),df[Field],'-o',color='green')
        #plt.xticks(rotation=90)
        plt.title(r.Name)
        plt.grid()
        plt.gca().set_yticklabels(['{:,.2%}'.format(x) for x in plt.gca().get_yticks()])
        plt.legend([p2,p1],['Statewide',r.Name],loc=2,fancybox=True,framealpha=0.5,prop={'size': 9})
        plt.tight_layout()
        plt.savefig(png_out(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()
def Year_Percentage_OnePlot(Crash_DF,EADF,Field,Order,PNGName):
    import matplotlib
    for i,r in EADF.iterrows():
        df = pd.DataFrame(Crash_DF[Crash_DF[r.CrashDataField]=='X'].groupby(['Crash_Year',Field])['KA'].aggregate(sum))
        df = df.unstack(Field)
        df.index = [2000+i for i in df.index]
        df.columns = [c[1] for c in df.columns]
        df = df.fillna(0)
        if len(Order) == 0:
            O = df.columns
        else:
            O == Order
        for i in df.index:
            df.loc[i] = df.loc[i]/float(sum(df.loc[i]))
        for c in O:
            if not c in df.columns:
                df[c] = 0
        plt.figure(figsize=(7.5, 6.5), dpi=300, facecolor='w', edgecolor='k')
        n = len(df.columns)
        ic = 0
        M = list(matplotlib.markers.MarkerStyle.markers.keys())
        for j,l in enumerate(O):
            ic+=0.9/len(O)
            plt.plot(range(len(df.index)),df[l],marker=M[j],label=l, color=plt.cm.Set1(ic))
            plt.xticks(range(len(df.index)),[])
            plt.xlim(-1,len(df.index))
        yt = ['{:,.2%}'.format(x) for x in plt.gca().get_yticks()]
        plt.gca().set_yticklabels(yt)
        plt.legend(loc='upper left',fancybox=True,framealpha=0.5, prop={'size': 7})
        plt.grid()
        plt.title(r.Name)
        plt.xticks(range(len(df.index)),df.index,rotation=0)
        plt.tight_layout()
        plt.savefig(PNGName(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()
def Year_Percentage_Stacked(Crash_DF,EADF,Field,Order,PNGName):
    import matplotlib
    for i,r in EADF.iterrows():
        df = pd.DataFrame(Crash_DF[Crash_DF[r.CrashDataField]=='X'].groupby(['Crash_Year',Field])['KA'].aggregate(sum))
        df = df.unstack(Field)
        df.index = [2000+i for i in df.index]
        df.columns = [c[1] for c in df.columns]
        df = df.fillna(0)
        if len(Order) == 0:
            O = df.columns
        else:
            O == Order
        for i in df.index:
            df.loc[i] = df.loc[i]/float(sum(df.loc[i]))
        for c in O:
            if not c in df.columns:
                df[c] = 0
        plt.figure(figsize=(7.5, 6.5), dpi=300, facecolor='w', edgecolor='k')
        barWidth=.8
        bottom = 0
        ic = 0
        for l in O:
            ic+=0.9/len(O)
            plt.bar(range(len(df.index)),df[l],label=l, edgecolor='white', width=barWidth,align='center',color=plt.cm.Set1(ic),bottom=bottom)
            bottom+=df[l]
        plt.ylim(0,1)
        plt.xticks(range(len(df.index)),df.index,rotation=0)
        plt.gca().set_yticklabels(['{:,.2%}'.format(x) for x in plt.gca().get_yticks()])
        plt.legend(loc=2,fancybox=True,framealpha=0.5,ncol=1, prop={'size': 7})
        plt.grid()
        plt.title(r.Name)
        plt.tight_layout()
        plt.savefig(PNGName(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()
def Year_Percentage_SubPlot(Crash_DF,EADF,Field,Order,PNGName):
    import matplotlib
    for i,r in EADF.iterrows():
        df = pd.DataFrame(Crash_DF[Crash_DF[r.CrashDataField]=='X'].groupby(['Crash_Year',Field])['KA'].aggregate(sum))
        df = df.unstack(Field)
        df.index = [2000+i for i in df.index]
        df.columns = [c[1] for c in df.columns]
        df = df.fillna(0)
        if len(Order) == 0:
            O = df.columns
        else:
            O == Order
        for i in df.index:
            df.loc[i] = df.loc[i]/float(sum(df.loc[i]))
        for c in O:
            if not c in df.columns:
                df[c] = 0
        plt.figure(figsize=(7.5, 6.5), dpi=300, facecolor='w', edgecolor='k')
        n = len(df.columns)
        ic = 0
        M = list(matplotlib.markers.MarkerStyle.markers.keys())
        for j,l in enumerate(O):
            plt.subplot(n,1,j+1)
            ic+=0.9/len(O)
            plt.plot(range(len(df.index)),df[l],'-o',label=l, color=plt.cm.Set1(ic))
            plt.xticks(range(len(df.index)),[])
            plt.xlim(-1,len(df.index))
            yt = ['{:,.2%}'.format(x) for x in plt.gca().get_yticks()]
            yt[0] = ''
            yt[-1] = ''
            plt.gca().set_yticklabels(yt)
            plt.legend(loc='upper left',fancybox=True,framealpha=0.5, prop={'size': 7})
            plt.grid()
            plt.tick_params(axis='both', which='major', labelsize=6)
            plt.tick_params(axis='both', which='minor', labelsize=6)
            if j==0:
                plt.title(r.Name)
        plt.xticks(range(len(df.index)),df.index,rotation=0)
        plt.tight_layout()
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.savefig(PNGName(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()
def SHSP_EABarStateLine(Crash_DF,Field,EADF,png_out,Order=[],Length=0):
    df = pd.DataFrame(Crash_DF.groupby([Field])['KA'].aggregate(sum))
    df.KA = df.KA/float(sum(df.KA))
    df.columns = [Field]
    if len(Order) == 0:
        df = df.sort_index(ascending=True)
    else:
        df = df.loc[Order]
    for i,r in EADF.iterrows():
        plt.figure(figsize=(7.5, 6.5), dpi=300, facecolor='w', edgecolor='k')
        eadf = pd.DataFrame(Crash_DF[Crash_DF[r.CrashDataField]=='X'].groupby([Field])['KA'].aggregate(sum))
        eadf = eadf.fillna(0)
        eadf.KA = eadf.KA/float(sum(eadf.KA))
        eadf.columns = [Field]
        if Length>0:
            eadf = eadf.sort_values(Field,ascending=False)
            eadf = eadf.iloc[range(min(Length,len(eadf)))]
            df = pd.DataFrame(Crash_DF.groupby([Field])['KA'].aggregate(sum))
            df.KA = df.KA/float(sum(df.KA))
            df.columns = [Field]
            if len(Order) == 0:
                df = df.sort_index(ascending=True)
            else:
                df = df.loc[Order]
            df  = df.loc[list(eadf.index)]
        else:
            eadf = eadf.loc[df.index]
        V = [v1-v2 for v1,v2 in zip(eadf[Field],df[Field])]
        my_cmap = matplotlib.cm.get_cmap('RdYlGn_r')
        my_norm = matplotlib.colors.Normalize(vmin=min(V), vmax=max(V))
        p1 = plt.bar(range(len(eadf)),eadf[Field],align='center',color=my_cmap(my_norm(V)))
        plt.xticks(range(len(df)),df.index,rotation=90)
        p2, = plt.plot(range(len(df)),df[Field],'-o',color='green')
        plt.xlabel(Field)
        #plt.xticks(rotation=90)
        plt.title(r.Name)
        plt.grid()
        plt.gca().set_yticklabels(['{:,.2%}'.format(x) for x in plt.gca().get_yticks()])
        plt.legend([p2,p1],['Statewide',r.Name],loc=2,fancybox=True,framealpha=0.5,prop={'size': 9})
        plt.tight_layout()
        plt.savefig(png_out(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()
def SHSP_EAStackStateLine(Crash_DF,Field,EADF,png_out,Order=[]):
    df = pd.DataFrame(Crash_DF.groupby([Field])['KA'].aggregate(sum))
    df.KA = df.KA/float(sum(df.KA))
    df.columns = [Field]
    if len(Order) == 0:
        df = df.sort_index(ascending=True)
    else:
        df = df.loc[Order]
    for i,r in EADF.iterrows():
        plt.figure(figsize=(7.5, 6.5), dpi=300, facecolor='w', edgecolor='k')
        eadf = pd.DataFrame(Crash_DF[Crash_DF[r.CrashDataField]=='X'].groupby([Field])['KA'].aggregate(sum))
        eadf = eadf.fillna(0)
        eadf.KA = eadf.KA/float(sum(eadf.KA))
        eadf.columns = [Field]
        eadf = eadf.loc[df.index]
        p1, = plt.stackplot(eadf.index,eadf[Field])
        plt.xlabel(Field)
        p2, = plt.plot(df.index,df[Field],color='green')
        plt.title(r.Name)
        plt.grid()
        plt.gca().set_yticklabels(['{:,.2%}'.format(x) for x in plt.gca().get_yticks()])
        plt.legend([p2,p1],['Statewide',r.Name],loc=2,fancybox=True,framealpha=0.5,prop={'size': 9})
        plt.tight_layout()
        plt.savefig(png_out(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()
def SHSP_EAOverlap(Crash_DF,EADF,png_out):
    for i,r in EADF.iterrows():
        plt.figure(figsize=(7.5, 6.5), dpi=300, facecolor='w', edgecolor='k')
        df = pd.DataFrame(columns=['KA'])
        for i2,r2 in EADF.iterrows():
            if i2!=i:
                df.loc[r2.Name] = Crash_DF[(Crash_DF[r2.CrashDataField]=='X') & (Crash_DF[r.CrashDataField]=='X')].KA.sum()
        p1 = plt.bar(range(len(df)),df.KA,align='center')
        plt.xticks(range(len(df)),df.index,rotation=90)
        plt.plot([], [], ' ', label='Total {} Fataliteis and A Injuries: {:,.0f}'.format(r.Name,len(Crash_DF[Crash_DF[r.CrashDataField]=='X'])))
        plt.legend(loc='upper right',fancybox=True,framealpha=0.5,prop={'size': 8})
        plt.title(r.Name)
        plt.ylabel('Number of KA Crashes')
        plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in plt.gca().get_yticks()])
        plt.grid()
        plt.tight_layout()
        plt.savefig(png_out(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close() 
def SHSP_County(Crash_DF,EADF,png_out):
    df = pd.DataFrame(Crash_DF.groupby(['County_name'])['KA'].aggregate(sum))
    df = df.sort_index()
    df.KA = df.KA/float(sum(df.KA))
    X = list(df.index)
    for i,r in EADF.iterrows():
        eadf = pd.DataFrame(Crash_DF[Crash_DF[r.CrashDataField]=='X'].groupby(['County_name'])['KA'].aggregate(sum))
        eadf = eadf.loc[list(df.index)]
        eadf = eadf.fillna(0)
        eadf.KA = eadf.KA/float(sum(eadf.KA))
        X = list(df.index)
        V = [eadf.KA.loc[x]-df.KA.loc[x] for x in X]
        xr = (min(V)*1.2,max(V)*1.2)

        plt.figure(figsize=(7.5, 6.5), dpi=300, facecolor='w', edgecolor='k')
        plt.subplot(131)
        X = list(df.index)[0:34]
        V = [eadf.KA.loc[x]-df.KA.loc[x] for x in X]
        for i,v in enumerate(V):
            plt.barh(i+1,v,color={-1:'green',1:'red'}[np.sign(v)],align='center')
        plt.xlim(xr)
        plt.ylim((0,len(X)+1))
        plt.grid()
        plt.yticks(range(1,len(X)+1),X)
        plt.gca().set_xticklabels(['{:,.2%}'.format(x) for x in plt.gca().get_xticks()])
        plt.xticks(rotation=90)

        plt.subplot(132)
        X = list(df.index)[34:68]
        V = [eadf.KA.loc[x]-df.KA.loc[x] for x in X]
        for i,v in enumerate(V):
            plt.barh(i+1,v,color={-1:'green',1:'red'}[np.sign(v)],align='center')
        plt.xlim(xr)
        plt.ylim((0,len(X)+1))
        plt.grid()
        plt.yticks(range(1,len(X)+1),X)
        plt.xticks(rotation=90)
        plt.gca().set_xticklabels(['{:,.2%}'.format(x) for x in plt.gca().get_xticks()])

        plt.subplot(133)
        X = list(df.index)[68:102]
        V = [eadf.KA.loc[x]-df.KA.loc[x] for x in X]
        for i,v in enumerate(V):
            plt.barh(i+1,v,color={-1:'green',1:'red'}[np.sign(v)],align='center')
        plt.xlim(xr)
        plt.ylim((0,len(X)+1))
        plt.grid()
        plt.yticks(range(1,len(X)+1),X)
        plt.xticks(rotation=90)
        plt.gca().set_xticklabels(['{:,.2%}'.format(x) for x in plt.gca().get_xticks()])

        plt.suptitle(r.Name)
        #plt.annotate('Over/Under Reperesentation compared to state-wide distribution of KA Crashes.', (0,0), (-300, -50), xycoords='axes fraction', textcoords='offset points', va='top',fontsize= 9)
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(png_out(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()
        plt.close()
def SHSP_EABarStateLineSubplot(Crash_DF,Field,EADF,png_out,Order=[]):
    df = pd.DataFrame(Crash_DF.groupby([Field])['KA'].aggregate(sum))
    df.KA = df.KA/float(sum(df.KA))
    df.columns = [Field]
    if len(Order) == 0:
        df = df.sort_index(ascending=True)
    else:
        df = df.loc[Order]
    for i,r in EADF.iterrows():
        plt.figure(figsize=(7.5, 6.5), dpi=300, facecolor='w', edgecolor='k')
        eadf = pd.DataFrame(Crash_DF[Crash_DF[r.CrashDataField]=='X'].groupby([Field])['KA'].aggregate(sum))
        eadf = eadf.fillna(0)
        eadf.KA = eadf.KA/float(sum(eadf.KA))
        eadf.columns = [Field]
        eadf = eadf.loc[df.index]

        X = df.index
        ax = plt.subplot(211)
        plt.bar(range(len(eadf)),eadf[Field],align='center',label=r.Name)
        plt.plot(range(len(eadf)),eadf[Field],'-o',color='green',label='Statewide')
        plt.xticks(range(len(X)),[])
        plt.title(r.Name)
        plt.grid()
        plt.gca().set_yticklabels(['{:,.2%}'.format(x) for x in plt.gca().get_yticks()])
        plt.legend(loc='upper right',fancybox=True,framealpha=0.5,prop={'size': 9})

        plt.subplot(212)
        V = [v1-v2 for v1,v2 in zip(eadf[Field],df[Field])]
        plt.bar([j for j,v in enumerate(V) if v>=0],[v for v in V if v>=0],align='center',color='red',label='Over Representation')
        plt.bar([j for j,v in enumerate(V) if v< 0],[v for v in V if v< 0],align='center',color='green',label='Under Representation')
        plt.xticks(range(len(X)),X,rotation=90)
        plt.xlim(ax.get_xlim())
        plt.gca().set_yticklabels(['{:,.2%}'.format(x) for x in plt.gca().get_yticks()])
        plt.grid()
        plt.legend(loc='upper right',fancybox=True,framealpha=0.5,prop={'size': 9})

        plt.tight_layout()
        plt.subplots_adjust(wspace=0, hspace=.1)
        plt.savefig(png_out(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()
def Year_SLRU_Trend(Crash_DF,EADF,PNGName):
    def LineFun(x, A, B):
        return A*x + B
    from scipy.optimize import curve_fit

    import matplotlib
    for i,r in EADF.iterrows():
        df = pd.DataFrame(Crash_DF[Crash_DF[r.CrashDataField]=='X'].groupby(['Crash_Year','State_Local_Urban_Rural'])['KA'].aggregate(sum))
        df = df.unstack('State_Local_Urban_Rural')
        df.index = [2000+i for i in df.index]
        df.columns = [c[1] for c in df.columns]
        df = df.fillna(0)

        plt.figure(figsize=(7.5, 6.5), dpi=300, facecolor='w', edgecolor='k')
        n = len(df.columns)
        ic = 0
        M = list(matplotlib.markers.MarkerStyle.markers.keys())
        O = ['State Urban','Local Urban','State Rural','Local Rural']
        for j,l in enumerate(['Urban','Rural']):
            plt.subplot(2,1,j+1)
            for l2 in ['State','Local']:
                ic+=0.9/4
                plt.plot(df.index,df[' '.join([l2,l])],'-o',label=' '.join([l2,l]), color=plt.cm.Set1(ic))
                for y in [[2010,2011,2012,2013,2014],[2012,2013,2014,2015,2016]]:
                    cr = Crash_DF[(Crash_DF[r.CrashDataField]=='X') & (Crash_DF.State_Local_Urban_Rural==' '.join([l2,l])) & (Crash_DF.Crash_Year.isin([y1-2000 for y1 in y]))].groupby(['Crash_Year'])['KA'].aggregate(sum)
                    cr.index = [2000+k for k in cr.index]
                    A,B = curve_fit(LineFun, cr.index, cr)[0]
                    plt.plot(pd.Series(data=LineFun(cr.index,A,B),index=cr.index),
                             {2010:'-.',2012:'-'}[y[0]],
                             color=plt.cm.Set1(ic),
                             label=' - {}-{}: {:.1%} {}'.format(y[0],y[-1],
                                                            abs(LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B),
                                                            {1:'Increase',-1:'Decrease'}[np.sign(LineFun(y[-1],A,B)-LineFun(y[0],A,B))]))
            plt.xlim(2006,2017)
            plt.xticks(range(2006,2017),[])
            yt = ['{}'.format(x) for x in plt.gca().get_yticks()]
            yt[0] = ''
            yt[-1] = ''
            plt.gca().set_yticklabels(yt)
            plt.tick_params(axis='both', which='major', labelsize=6)
            plt.tick_params(axis='both', which='minor', labelsize=6)
            plt.legend(loc='upper left',fancybox=True,framealpha=0.5, prop={'size': 7})
            plt.grid()
            if j==0:
                plt.title(r.Name)
        plt.xticks(df.index,df.index,rotation=0)
        plt.tight_layout()
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.savefig(PNGName(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()
def Year_SLRU_EMA(Crash_DF,EADF,PNGName):
    import warnings
    warnings.filterwarnings('ignore')
    from scipy.optimize import curve_fit
    import matplotlib
    def LineFun(x, A, B):
            return A*x + B
    def EMA(Data,window):
        from scipy.interpolate import spline
        Data =Data.fillna(0)
        ema = pd.ewma(Data,span = window)[window-1:]
        #z = np.polyfit(ema.index, ema, 4)
        #f = np.poly1d(z)
        x = np.linspace(list(ema.index)[0], list(ema.index)[-1],100)
        try:
            y = spline(list(ema.index),ema,x)
            return(pd.Series(index=x,data=y))
        except:
            print(ema)
            return(pd.Series(index=x,data=0))
        #y = f(x)
    def Get_NM_EMA_Diff(Crash_EA_DF,SLUR):
                    cr = Crash_EA_DF[(Crash_EA_DF.State_Local_Urban_Rural==SLUR)].groupby(['Crash_Year'])['KA'].aggregate(sum)
                    cr.index = [2000+k for k in cr.index]
                    cr = cr.loc[range(2007,2017)]
                    cr = cr.fillna(0)
                    ema1 = pd.ewma(cr,span = 6)
                    ema2 = pd.ewma(cr,span = 3)
                    diff = ema2-ema1
                    diff = pd.Series([a/b for a,b in zip(diff.loc[diff.index[1:]],cr.loc[diff.index[:-1]])],index=range(2008,2017))
                    diff = diff.loc[range(2012,2017)]
                    return(diff)   
    my_cmap = matplotlib.cm.get_cmap('RdYlGn_r')
    my_norm = matplotlib.colors.Normalize(vmin=-1, vmax=1)
    barwidth = 0.5
    CL = pd.DataFrame(data=[[plt.cm.Set1(0.9/4*(i+1))] for i in range(4)],index=['State Urban','Local Urban','State Rural','Local Rural'])
    for i,r in EADF.iterrows():
            df = pd.DataFrame(Crash_DF[Crash_DF[r.CrashDataField]=='X'].groupby(['Crash_Year','State_Local_Urban_Rural'])['KA'].aggregate(sum))
            df = df.unstack('State_Local_Urban_Rural')
            df.index = [2000+i for i in df.index]
            df.columns = [c[1] for c in df.columns]
            df = df.fillna(0)
            gs = matplotlib.gridspec.GridSpec(10, 1)
            n = len(df.columns)
            ic = 0
            M = list(matplotlib.markers.MarkerStyle.markers.keys())
            O = ['State Urban','Local Urban','State Rural','Local Rural']
            tPlot, axes = plt.subplots(nrows=4, ncols=1, sharex=True, sharey=False, gridspec_kw={'height_ratios':[3,1,3,1]})
            plt.figure(figsize=(7.5, 6.5), dpi=300, facecolor='w', edgecolor='k')
            for j,l in enumerate(['Urban','Rural']):
                plt.subplot(gs[5*j:5*j+3, :])
                for l2 in ['State','Local']:
                    ic+=0.9/4
                    plt.plot(df.index,df[' '.join([l2,l])],'-.o',label=' '.join([l2,l]), color=CL.loc[' '.join([l2,l]),0])
                    for k,win in enumerate([6,3]):
                        cr = Crash_DF[(Crash_DF[r.CrashDataField]=='X') & (Crash_DF.State_Local_Urban_Rural==' '.join([l2,l]))].groupby(['Crash_Year'])['KA'].aggregate(sum)
                        cr.index = [2000+k for k in cr.index]
                        cr = cr.fillna(0)
                        cr = cr.loc[range(2007,2017)]
                        #A,B = curve_fit(LineFun, cr.index, cr)[0]
                        plt.plot(EMA(cr,win),
                                 {0:'-',1:'--'}[k],
                                 color=CL.loc[' '.join([l2,l]),0],
                                 label=' - EMA {} Years'.format(win))
                plt.xlim(2006,2017)
                plt.xticks(range(2006,2017),[])
                yt = ['{:,.0f}'.format(x) for x in plt.gca().get_yticks()]
                yt[0] = ''
                yt[-1] = ''
                plt.gca().set_yticklabels(yt)
                plt.tick_params(axis='both', which='major', labelsize=6)
                plt.tick_params(axis='both', which='minor', labelsize=6)
                plt.legend(loc='upper left',fancybox=True,framealpha=0.5, prop={'size': 7},ncol=2)
                plt.grid()
                if j==0:
                    plt.title(r.Name)
                plt.subplot(gs[5*j+3, :])
                l2  = 'State'
                plt.gca().set_axis_bgcolor(CL.loc[' '.join([l2,l]),0])
                diff_S = Get_NM_EMA_Diff(Crash_DF[Crash_DF[r.CrashDataField]=='X'],' '.join(['State',l]))
                diff_L = Get_NM_EMA_Diff(Crash_DF[Crash_DF[r.CrashDataField]=='X'],' '.join(['Local',l]))
                L = [abs(v) for v in list(pd.concat([diff_S,diff_L]))]
                yl = [-max(L),max(L)]
                diff = diff_S
                plt.bar(diff.index,diff,align='center',color = my_cmap(np.sign(diff)),label='{} {}, EMA3-EMA6 Indicator'.format(l2,l),width=barwidth)
                plt.hlines(0,2006,2017,'black')
                plt.xlim(2006,2017)
                plt.ylim(yl[0],yl[1])
                plt.xticks(range(2006,2017),[])
                yt = ['{:,.1%}'.format(x) for x in plt.gca().get_yticks()]
                yt = [{True:y,False:''}[z in [1,len(yt)-2]] for z,y in enumerate(yt)]
                plt.gca().set_yticklabels(yt)
                plt.tick_params(axis='both', which='major', labelsize=6)
                plt.tick_params(axis='both', which='minor', labelsize=6)
                plt.grid()
                plt.legend(loc='upper left',fancybox=True,framealpha=0.5, prop={'size': 7},ncol=1)
                plt.subplot(gs[5*j+4, :])
                l2 = 'Local'
                plt.gca().set_axis_bgcolor(CL.loc[' '.join([l2,l]),0])
                diff = diff_L
                plt.bar(diff.index,diff,align='center',color=my_cmap(np.sign(diff)),label='{} {}, EMA3-EMA6 Indicator'.format(l2,l),width=barwidth)
                plt.hlines(0,2006,2017,'black')
                plt.xlim(2006,2017)
                plt.ylim(yl[0],yl[1])
                plt.xticks(range(2006,2017),[])
                yt = ['{:,.1%}'.format(x) for x in plt.gca().get_yticks()]
                yt = [{True:y,False:''}[z in [1,len(yt)-2]] for z,y in enumerate(yt)]
                plt.gca().set_yticklabels(yt)
                plt.tick_params(axis='both', which='major', labelsize=6)
                plt.tick_params(axis='both', which='minor', labelsize=6)
                plt.grid()
                plt.legend(loc='upper left',fancybox=True,framealpha=0.5, prop={'size': 7},ncol=1)
            plt.xticks(df.index,df.index,rotation=0)
            plt.tight_layout()
            plt.subplots_adjust(wspace=0, hspace=0)
            plt.savefig(PNGName(r.Name.replace('/','_').replace(' ','_')),transparent=False,DeprecationWarning=1200)
            plt.close()
            plt.close()
def SHSP_TimeTrend_Contour(DF,EADF,PNGName):
    import warnings
    warnings.filterwarnings('ignore')
    DF['Time'] = [datetime.time(datetime(2000,1,1,d.hour,0)).strftime('%I:%M %p') for d in DF.Date]
    TimeOrder = [datetime.time(datetime(2000,1,1,d,0)).strftime('%I:%M %p') for d in range(0,24)]
    TimeOrder.reverse()
    DF['DayName'] = [d.weekday_name for d in DF.Date]
    DayOrder = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    DF['Month']  = [d.strftime('%b') for d in DF.Date]
    MonthOrder = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for i,r in EADF.iterrows():
        df0 = pd.DataFrame(DF[DF[r.CrashDataField]=='X'].groupby(['Month','DayName','Time'])['KA'].aggregate(sum))
        df0 = df0.unstack('Time').T
        df0.index = df0.index.droplevel(0)
        arr = []
        for m in MonthOrder:
            for d in DayOrder:
                arr.append((m,d))
        cs = pd.MultiIndex.from_tuples(arr)
        df = pd.DataFrame(columns=cs,index=TimeOrder)
        for i1 in df.index:
            for j1 in df.columns:
                try:
                    df.set_value(i1,j1,int(df0.loc[i1,j1]))
                except:
                    pass
        df = df.fillna(0)
        df = df.loc[TimeOrder]
        L = []
        for l in list(df.values):
            L.extend(l)
        v_max = max(L)
        v_min = min(L)
        df = df/v_max
        v_max = 1
        v_min = 0
    
        plt.figure(figsize=(7, 7), dpi=300, facecolor='w', edgecolor='k')
        ax1 = plt.subplot(211)
    
        df1 = df[MonthOrder[0:6]]
        pl1 = plt.contourf(df1, cmap=plt.cm.Reds,corner_mask=True ,alpha=1)
        xposition = [7*(i1)-0.5 for i1 in range(1,6)]
        for xc in xposition:
            plt.axvline(x=xc, color='k', linestyle='--')
        xl = [{True:f[1][0:2] + '  ' + f[0],False:f[1][0:2]}[f[1][0:2]=='Th'] for f in df1.columns]
        plt.xticks(range(len(list(df1))),xl,rotation=90,fontsize=6)
        plt.gca().xaxis.tick_top()
        plt.yticks(range(1,len(df1.index)),list(df1.index)[1:],rotation=0,fontsize=6)
        
        plt.grid()
        df1 = df[MonthOrder[6:13]]
        ax2 = plt.subplot(212)
        pl2 = plt.contourf(df1, cmap=plt.cm.Reds,corner_mask=True ,alpha=1)
        for xc in xposition:
            plt.axvline(x=xc, color='k', linestyle='--')
        xl = [{True:f[0] + '  ' + f[1][0:2],False:f[1][0:2]}[f[1][0:2]=='Th'] for f in df1.columns]
        plt.xticks(range(len(list(df1))),xl,rotation=90,fontsize=6)
        plt.yticks(range(len(df1.index)),df1.index,rotation=0,fontsize=6)
        plt.grid()
        #plt.gcf().subplots_adjust(right=0.8)
        #cbar_ax = plt.gcf().add_axes([0.85, 0.15, 0.05, 0.7])
        #plt.colorbar(pl1, cax=cbar_ax)
        plt.subplots_adjust(wspace=0, hspace=0)
        plt.suptitle(r.Name,y=0.99)
        #plt.tight_layout()
        plt.savefig(PNGName(r.Name.replace('/','_').replace(' ','_')),transparent=True,dpi=1200)
        plt.close()


def CalRed(y1,y2):
    try:
        return(y1-y2)
    except:
        return({True:0,False:100}[y1==y2])
def FormatPercentages(r):
    if type(r.Y12_16)==numpy.float64:
        return('{:,.0%}'.format(abs(r.Y12_16)))
    if type(r.Y12_16)==str:
        if r.Reduction==0:
            return('{}'.format(r.Y12_16))
        else:
            return('')
def FormatReduction(r):
    if type(r.Y12_16)==numpy.float64:
        return('({:,.1%} {} compared to 2010-2014)'.format(abs(r.Reduction),{1:'decrease',-1:'increase'}[np.sign(r.Reduction)]))    
    if type(r.Y12_16)==str:
        if r.Reduction==100:
            return('{}'.format(r.Y12_16))
def LineFun(x, A, B):
    ObjFun = A*x + B 
    return (ObjFun)
def QueryBulletPoints(Crash_DF,Occ_DF,AC,Veh_DF):
    r = EADF.loc[EADF[EADF.Acronym==AC].index.item()]
    Res = []
    for y in [[10,11,12,13,14],[15,16,12,13,14]]:
        res = []
        df = Crash_DF[(Crash_DF[r.CrashDataField]=='X') & (Crash_DF.Crash_Year.isin(y))]
        if AC=='RD':
            mf1 = df[df.Nbr_of_Vehicles==1]['KA'].sum()/float(df.KA.sum())
            res.append(mf1)

            df2 = df[(df.Weather.isin(['Rain','Snow']))]
            mf2 = df2.KA.sum()/float(df.KA.sum())
            mf2_1 = df2[df2.SpeedingAggressiveDriver=='X'].KA.sum()/df2.KA.sum()
            mf2_2 = df2[df2.ImpairedDriver=='X'].KA.sum()/df2.KA.sum()
            res.extend([mf2,mf2_1,mf2_2])

            df31 = df[df.State_Local_Urban_Rural.isin(['Local Rural','State Rural'])]
            mf3_1_1 = df31.KA.sum()/df.KA.sum()
            mf3_1_2 = df31[df31.State_Local_Urban_Rural=='Local Rural'].KA.sum()/df31.KA.sum()
            mf3_1_3 = df31[(df31.State_Local_Urban_Rural=='Local Rural') & (df31.Type_of_crash=='Fixed Object')].KA.sum()/df31[(df31.State_Local_Urban_Rural=='Local Rural')].KA.sum()

            df32 = df[df.State_Local_Urban_Rural.isin(['Local Urban','State Urban'])]
            mf3_2_1 = df32.KA.sum()/df.KA.sum()
            mf3_2_2 = df32[df32.State_Local_Urban_Rural=='Local Urban'].KA.sum()/df32.KA.sum()
            mf3_2_3 = df32[(df32.State_Local_Urban_Rural=='Local Urban') & (df32.County_name.isin(['Cook','Will','DuPage']))].KA.sum()/df32[(df32.State_Local_Urban_Rural=='Local Urban')].KA.sum()
            res.extend([mf3_1_1,mf3_1_2,mf3_1_3,mf3_2_1,mf3_2_2,mf3_2_3])

            odf = Occ_DF.loc[df.index]
            mf4 = df.loc[list(set(odf[(odf.UnitNo==1) & (odf.Age<25) & (odf.Age>16)].index))].KA.sum()/df.KA.sum()
            #mf4 = df[(df.YoungerDriver16to20=='X') | (df.YoungerDriver21to25=='X')].KA.sum()/df.KA.sum()
            res.append(mf4)

            df5 = df[df.LightCondition.isin(['Darkness','Darkness, Lighted Road','Dusk','Dawn'])]
            mf5 = df5.KA.sum()/df.KA.sum()
            mf5_1 = df5[df5.LightCondition=='Darkness'].KA.sum()/df5.KA.sum()
            mf5_2 = df5[df5.Day_of_week_name.isin(['Sunday','Saturday'])].KA.sum()/df5.KA.sum()
            mf5_2_1 = df5[(df5.Day_of_week_name.isin(['Sunday','Saturday'])) & (df5.ImpairedDriver=='X')].KA.sum()/df5[df5.Day_of_week_name.isin(['Sunday','Saturday'])].KA.sum()
            res.extend([mf5,mf5_1,mf5_2,mf5_2_1])

            df6 = df[df.Trafficway_description.isin(['Not Divided','Divided, No Median Barrier'])]
            mf6 = df6.KA.sum()/df.KA.sum()
            mf6_1 = df6[(df6.Type_of_crash=='Fixed Object')].KA.sum()/df6.KA.sum()
            df611 = df6[(df6.Type_of_crash=='Fixed Object') & (df6.Alignment.isin(['Curve, Level','Curve On Grade','Curve On Hillcrest']))]
            mf6_1_1 = df611.KA.sum()/df6[(df6.Type_of_crash=='Fixed Object')].KA.sum()
            mf6_1_1_1 = df611[df611.ImpairedDriver=='X'].KA.sum()/df611.KA.sum()
            mf6_1_1_2 = df611[df611.SpeedingAggressiveDriver=='X'].KA.sum()/df611.KA.sum()
            res.extend([mf6,mf6_1,mf6_1_1,mf6_1_1_1,mf6_1_1_2])
        
        if AC=='IN':
            df1 = df[df.State_Local_Urban_Rural.isin(['Local Urban','State Urban'])]
            df2 = df[df.State_Local_Urban_Rural.isin(['Local Rural','State Rural'])]
            mf1 = df1.KA.sum()/float(df.KA.sum())
            res.append(mf1)
            df11 = df1[(df1.Traffic_Device=='Traffic Signal')] 
            mf2 = df11.KA.sum()/float(df1.KA.sum())
            res.append(mf2)
            mf3 = df11[df11.Cause1.isin(['Failing to Yield Right of Way','Failing to yield right-of-way'])].KA.sum()/float(df11.KA.sum())
            res.append(mf3)
            mf4 = df11[df11.Cause1.isin(['Disregarding Traffic Signals'])].KA.sum()/float(df11.KA.sum())
            res.append(mf4)

            mf1 = df2.KA.sum()/float(df.KA.sum())
            res.append(mf1)
            df21 = df2[(df2.Traffic_Device=='Stop Sign/Flasher')] 
            mf2 = df21.KA.sum()/float(df2.KA.sum())
            res.append(mf2)
            mf4 = df21[df21.Cause1.isin(['Disregarding Stop Sign'])].KA.sum()/float(df21.KA.sum())
            res.append(mf4)

            df3 = df[df.Nbr_of_Vehicles==1]
            res.append(df3.KA.sum()/float(df.KA.sum()))
            df31 = df3[df3.Pedestrian=='X']
            res.append(df31.KA.sum()/float(df3.KA.sum()))
            odf = Occ_DF.loc[df31.index]
            mf9 = df31.loc[list(set(odf[(odf.PED_Location=='In Crosswalk')].index))].KA.sum()/df31.KA.sum()
            res.append(mf9)


            df4 = df[df.Nbr_of_Vehicles==2]
            res.append(df4.KA.sum()/float(df.KA.sum()))
            res.append(df4[df4.Type_of_crash=='Angle'].KA.sum()/df4.KA.sum())

            df5 = df[df.LightCondition.isin(['Darkness','Darkness, Lighted Road','Dusk','Dawn'])]
            res.append(df5.KA.sum()/df.KA.sum())
            df51 = df5[df5.LightCondition=='Darkness, Lighted Road']
            res.append(df51.KA.sum()/df5.KA.sum())
            res.append(df51[df51.County_name.isin(['Cook','Will','DuPage'])].KA.sum()/df51.KA.sum())
            res.append(df51[df51.ImpairedDriver=='X'].KA.sum()/df51.KA.sum())
            res.append(df51[df51.YoungerDriver16to20=='X'].KA.sum()/df51.KA.sum())
            res.append(df51[df51.SpeedingAggressiveDriver=='X'].KA.sum()/df51.KA.sum())
            
        if AC=='PD':
            df1 = df[df.State_Local_Urban_Rural.isin(['Local Urban','State Urban'])]
            df11 = df[df.State_Local_Urban_Rural.isin(['State Urban'])]
            df12 = df[df.State_Local_Urban_Rural.isin(['Local Urban'])]
            mf1 = df1.KA.sum()/float(df.KA.sum())
            res.append(mf1)
            mf2 = df11.KA.sum()/float(df1.KA.sum())
            res.append(mf2)
            mf3 = df12.KA.sum()/float(df1.KA.sum())
            res.append(mf3)
            cr = df11.groupby('Crash_Year')['KA'].aggregate(sum)
            A,B = curve_fit(LineFun, cr.index, cr)[0]
            #mf4 = (LineFun(y[0],A,B)-LineFun(y[-1],A,B))/LineFun(y[0],A,B)
            mf40 = {1:'decreased',-1:'increased'}[np.sign(cr[y[0]]-cr[y[-1]])]
            mf4 = (cr[y[0]]-cr[y[-1]])/cr[y[0]]
            mf5 = mf4/(len(y)-1)
            mf51 = {1:'reduction',-1:'increase'}[np.sign(cr[y[0]]-cr[y[-1]])]
            res.extend([mf40,mf4,mf5,mf51])

            df111 = df11[df11.Roadway_functional_class_description.isin(['Minor Arterial (Urban)','Other Principal Arterial (PAS)','Minor Arterial (Non-Urban)','Collector (Urban)'])]
            mf6 = df111.KA.sum()/df11.KA.sum()
            res.append(mf6)
            mf7 = df111[df111.Intersection_related=='Y'].KA.sum()/df111.KA.sum()
            res.append(mf7)
            mf8 = df111[(df111.Intersection_related=='Y') & (df111.Traffic_Device=='Traffic Signal')].KA.sum()/df111[df111.Intersection_related=='Y'].KA.sum()
            res.append(mf8)

            odf = Occ_DF.loc[df111.index]
            mf9 = df111.loc[list(set(odf[(odf.PED_Location!='In Crosswalk')].index))].KA.sum()/df111.KA.sum()
            res.append(mf9)
            mf10 = df111.loc[list(set(odf[(odf.PED_Location=='In Roadway')].index))].KA.sum()/df111.KA.sum()
            res.append(mf10)
            mf11 = df111.loc[list(set(odf[(odf.PED_Location=='In Crosswalk')].index))].KA.sum()/df111.KA.sum()
            res.append(mf11)

            cr = df12.groupby('Crash_Year')['KA'].aggregate(sum)
            A,B = curve_fit(LineFun, cr.index, cr)[0]
            mf120 = {1:'increased',-1:'decreased'}[np.sign(cr[y[-1]]-cr[y[0]])]
            #mf12 = (LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B)
            mf12 = (cr[y[-1]]-cr[y[0]])/cr[y[0]]
            mf13 = mf12/(len(y)-1)
            mf131 = {-1:'reduction',1:'increase'}[np.sign(cr[y[-1]]-cr[y[0]])]
            res.extend([mf120,mf12,mf13,mf131])

            df121 = df12[df12.Roadway_functional_class_description.isin(['Minor Arterial (Urban)','Other Principal Arterial (PAS)','Minor Arterial (Non-Urban)','Collector (Urban)'])]
            mf14 = df121.KA.sum()/df12.KA.sum()
            res.append(mf14)

            mf15 = df121[df121.Intersection_related=='Y'].KA.sum()/df121.KA.sum()
            res.append(mf15)
            mf16 = df121[(df121.Intersection_related=='Y') & (df121.Traffic_Device=='Traffic Signal')].KA.sum()/df121[df121.Intersection_related=='Y'].KA.sum()
            res.append(mf16)

            odf = Occ_DF.loc[df121.index]
            mf17 = df121.loc[list(set(odf[(odf.PED_Location!='In Crosswalk')].index))].KA.sum()/df121.KA.sum()
            res.append(mf17)
            mf18 = df121.loc[list(set(odf[(odf.PED_Location=='In Roadway')].index))].KA.sum()/df121.KA.sum()
            res.append(mf18)
            mf19 = df121.loc[list(set(odf[(odf.PED_Location=='In Crosswalk')].index))].KA.sum()/df121.KA.sum()
            res.append(mf19)

            mf20 = df121[df121.Cause1.isin(['Failing to Yield Right of Way','Failing to yield right-of-way'])].KA.sum()/df121.KA.sum()
            res.append(mf20)

            odf = Occ_DF.loc[df1.index]
            mf21 = df1.loc[list(set(odf[(odf.PED_Location.isin(['In Crosswalk','In Roadway']))].index))].KA.sum()/df1.KA.sum()
            res.append(mf21)

            df2 = df[df.State_Local_Urban_Rural.isin(['State Rural'])]
            cr = df2.groupby('Crash_Year')['KA'].aggregate(sum)
            A,B = curve_fit(LineFun, cr.index, cr)[0]
            #mf22 = LineFun(y[-1],A,B)/LineFun(y[0],A,B)
            mf22 = cr[y[-1]]/cr[y[0]]
            res.append(mf22)

            mf23 = df[df.County_name.isin(['Cook','Will','DuPage'])].KA.sum()/df.KA.sum()
            res.append(mf23)
            
        if AC=='PC':
            odf = Occ_DF.loc[df.index]
            odf = odf[odf.Age<26]
            res.append(df.loc[list(set(odf.index))].KA.sum()/df.KA.sum())
            res.append(odf[odf.Sex=='M'].KA.sum()/odf.KA.sum())
            res.append(odf[odf.Sex=='F'].KA.sum()/odf.KA.sum())

            df1 = df[df.State_Local_Urban_Rural.isin(['Local Urban','State Urban'])]
            df11 = df[df.State_Local_Urban_Rural.isin(['State Urban'])]
            df12 = df[df.State_Local_Urban_Rural.isin(['Local Urban'])]
            res.append(df1.KA.sum()/df.KA.sum())
            res.append(df11.KA.sum()/df1.KA.sum())
            res.append(df12.KA.sum()/df1.KA.sum())

            cr = df11.groupby('Crash_Year')['KA'].aggregate(sum)
            A,B = curve_fit(LineFun, cr.index, cr)[0]
            mf120 = {1:'increased',-1:'decreased'}[np.sign(cr[y[-1]]-cr[y[0]])]
            #mf12 = (LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B)
            mf12 = abs(cr[y[-1]]-cr[y[0]])/cr[y[0]]
            mf13 = mf12/(len(y)-1)
            mf131 = {-1:'reduction',1:'increase'}[np.sign(cr[y[-1]]-cr[y[0]])]
            res.extend([mf120,mf12,mf13,mf131])

            df121 = df11[df11.Roadway_functional_class_description.isin(['Minor Arterial (Urban)','Other Principal Arterial (PAS)','Minor Arterial (Non-Urban)','Collector (Urban)'])]
            mf14 = df121.KA.sum()/df11.KA.sum()
            res.append(mf14)

            mf15 = df121[df121.Intersection_related=='Y'].KA.sum()/df121.KA.sum()
            res.append(mf15)
            mf16 = df121[(df121.Intersection_related=='Y') & (df121.Traffic_Device=='Traffic Signal')].KA.sum()/df121[df121.Intersection_related=='Y'].KA.sum()
            res.append(mf16)

            cr = df12.groupby('Crash_Year')['KA'].aggregate(sum)
            A,B = curve_fit(LineFun, cr.index, cr)[0]
            mf120 = {1:'increased',-1:'decreased'}[np.sign(cr[y[-1]]-cr[y[0]])]
            #mf12 = (LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B)
            mf12 = abs(cr[y[-1]]-cr[y[0]])/cr[y[0]]
            mf13 = mf12/(len(y)-1)
            mf131 = {-1:'reduction',1:'increase'}[np.sign(cr[y[-1]]-cr[y[0]])]
            res.extend([mf120,mf12,mf13,mf131])

            df121 = df12[df12.Roadway_functional_class_description.isin(['Minor Arterial (Urban)','Other Principal Arterial (PAS)','Minor Arterial (Non-Urban)','Collector (Urban)'])]
            mf14 = df121.KA.sum()/df12.KA.sum()
            res.append(mf14)

            mf15 = df121[df121.Intersection_related=='Y'].KA.sum()/df121.KA.sum()
            res.append(mf15)
            mf16 = df121[(df121.Intersection_related=='Y') & (df121.Traffic_Device=='Traffic Signal')].KA.sum()/df121[df121.Intersection_related=='Y'].KA.sum()
            res.append(mf16)
            mf3 = df121[df121.Cause1.isin(['Failing to Yield Right of Way','Failing to yield right-of-way'])].KA.sum()/float(df121.KA.sum())
            res.append(mf3)

            res.append(df[df.Day_of_week_name.isin(['Tuesday'])].KA.sum()/df.KA.sum())
            res.append(df[df.Day_of_week_name.isin(['Wednesday'])].KA.sum()/df.KA.sum())
            res.append(df[df.Day_of_week_name.isin(['Friday'])].KA.sum()/df.KA.sum())
            res.append(df[df.Day_of_week_name.isin(['Tuesday','Wednesday','Friday'])].KA.sum()/df.KA.sum())
            res.append(df[(df.Day_of_week_name.isin(['Friday'])) & (df.Time.isin(TimeOrder[12:17]))].KA.sum()/df[df.Day_of_week_name.isin(['Friday'])].KA.sum())
            res.append(df[(df.Day_of_week_name.isin(['Wednesday'])) & (df.Time.isin(TimeOrder[18:]))].KA.sum()/df[df.Day_of_week_name.isin(['Wednesday'])].KA.sum())

            res.append(df[df.Month.isin(['Jun','Jul','Aug'])].KA.sum()/df.KA.sum())
            
        if AC=='SA':
            df1 = df[df.State_Local_Urban_Rural.isin(['Local Urban','State Urban'])]
            res.append(df1.KA.sum()/df.KA.sum())
            df11 = df[df.State_Local_Urban_Rural.isin(['State Urban'])]
            res.append(df11.KA.sum()/df1.KA.sum())
            df111 = df11[df11.Roadway_functional_class_description.isin(['Minor Arterial (Urban)','Other Principal Arterial (PAS)','Minor Arterial (Non-Urban)','Collector (Urban)'])]
            res.append(df111.KA.sum()/df11.KA.sum())
            df112 = df11[df11.Roadway_functional_class_description.isin(['Interstate (PAS)','Freeway and Expressway (Urban Only) (PAS)'])]
            res.append(df112.KA.sum()/df11.KA.sum())
            res.append(df112[(df112.Type_of_crash=='Fixed Object')].KA.sum()/df112.KA.sum())
            
            res.append(df111[df111.Intersection_related=='Y'].KA.sum()/df111.KA.sum())
            res.append(df111[df111.YoungerDriver16to20=='X'].KA.sum()/df111.KA.sum())
            res.append(df111[df111.Type_of_crash=='Rear End'].KA.sum()/df111.KA.sum())
            
            res.append(df[df.RoadwayDeparture=='X'].KA.sum()/df.KA.sum())
            res.append(df[df.YoungerDriver16to20=='X'].KA.sum()/df.KA.sum())
            res.append(df[df.ImpairedDriver=='X'].KA.sum()/df.KA.sum())
            
            odf = Occ_DF.loc[df[df.ImpairedDriver=='X'].index]
            res.append(df.loc[list(set(odf[odf.Sex=='M'].index))].KA.sum()/df[df.ImpairedDriver=='X'].KA.sum())
            odf = Occ_DF.loc[df[df.RoadwayDeparture=='X'].index]
            res.append(df.loc[list(set(odf[odf.Sex=='M'].index))].KA.sum()/df[df.RoadwayDeparture=='X'].KA.sum())
            
            df2 = df[df.Roadway_surface.isin(['Ice','Sand / Mud / Dirt','Sand, Mud, Dirt','Snow or Slush','Wet'])]
            res.append(df2.KA.sum()/df.KA.sum())
            res.append(df2[df2.Type_of_crash=='Rear End'].KA.sum()/df2.KA.sum())
            res.append(df2[df2.Type_of_crash=='Fixed Object'].KA.sum()/df2.KA.sum())
            res.append(df2[df2.Alignment.isin(['Curve, Level','Curve On Grade','Curve On Hillcrest'])].KA.sum()/df2.KA.sum())
            res.append(df[df.Time.isin(TimeOrder[12:18])].KA.sum()/df.KA.sum())            
            
        if AC=='UO':
            UOC = ['Child Restraint Not Used',
             'Child Restraint Used Improperly',
             'Helmet Not Used',
             'None Present',
             'Seat Belts Not Used',
             'Unknown/NA']            
            odf = Occ_DF[(Occ_DF.Unrestrained_Occupants_ISHSP=='X') & (Occ_DF.Crash_Year.isin(y))]
            odf1 = odf[odf.Safety_Equipment.isin(['Seat Belts Not Used'])]
            mf1 = odf1.KA.sum()/odf.KA.sum()
            res.append(mf1)
            res.append(1-mf1)

            res.append(odf[(odf['Person Type']==1) & (odf.Age>=16) & (odf.Age<=20)].KA.sum()/odf.KA.sum())
            res.append(odf[(odf['Person Type']==1) & (odf.Age>=21) & (odf.Age<=25)].KA.sum()/odf.KA.sum())
            res.append(odf[(odf['Person Type']==1) & (odf.Age>=16) & (odf.Age<=25)].KA.sum()/odf.KA.sum())
            
            odf1 = odf[odf['Person Type']==1]
            odf2 = odf[odf['Person Type']==7]
            res.append(odf1.KA.sum()/odf.KA.sum())
            res.append(odf2.KA.sum()/odf.KA.sum())
            res.append(odf1[odf1.Sex=='M'].KA.sum()/odf1.KA.sum())
            res.append(odf1[odf1.Sex=='F'].KA.sum()/odf1.KA.sum())
            res.append(odf2[odf2.Sex=='M'].KA.sum()/odf2.KA.sum())
            res.append(odf2[odf2.Sex=='F'].KA.sum()/odf2.KA.sum())
            
            odf1 = odf[odf.State_Local_Urban_Rural.isin(['Local Urban','State Urban'])]
            odf11 = odf[odf.State_Local_Urban_Rural.isin(['State Urban'])]
            odf12 = odf[odf.State_Local_Urban_Rural.isin(['Local Urban'])]
            res.append(odf1.KA.sum()/odf.KA.sum())
            res.append(odf11.KA.sum()/odf1.KA.sum())
            res.append(odf12.KA.sum()/odf1.KA.sum())

            cr = odf11.groupby('Crash_Year')['KA'].aggregate(sum)
            mf120 = {1:'increased',-1:'decreased'}[np.sign(cr[y[-1]]-cr[y[0]])]
            #mf12 = (LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B)
            mf12 = abs(cr[y[-1]]-cr[y[0]])/cr[y[0]]
            mf13 = mf12/(len(y)-1)
            mf131 = {-1:'reduction',1:'increase'}[np.sign(cr[y[-1]]-cr[y[0]])]
            res.extend([mf120,mf12,mf13,mf131])
            
            cr = odf12.groupby('Crash_Year')['KA'].aggregate(sum)
            mf120 = {1:'increased',-1:'decreased'}[np.sign(cr[y[-1]]-cr[y[0]])]
            #mf12 = (LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B)
            mf12 = abs(cr[y[-1]]-cr[y[0]])/cr[y[0]]
            mf13 = mf12/(len(y)-1)
            mf131 = {-1:'reduction',1:'increase'}[np.sign(cr[y[-1]]-cr[y[0]])]
            res.extend([mf120,mf12,mf13,mf131])
            
            df12 = odf[odf.State_Local_Urban_Rural.isin(['Local Urban'])]
            df121 = df12[df12.Roadway_functional_class_description.isin(['Minor Arterial (Urban)','Other Principal Arterial (PAS)','Minor Arterial (Non-Urban)','Collector (Urban)'])]
            df122 = df121[df121.Intersection_related!='Y']
            df123 = df122[df122.Type_of_crash.isin(['Fixed Object','Head On','Overturned','Sideswipe Opposite Direction'])]
            res.append(df121.KA.sum()/df12.KA.sum())
            res.append(df122.KA.sum()/df121.KA.sum())
            res.append(df123.KA.sum()/df122.KA.sum())
            res.append(df123[df123.Type_of_crash.isin(['Fixed Object'])].KA.sum()/df123.KA.sum())
            
            df12 = df[df.State_Local_Urban_Rural.isin(['State Urban'])]
            df121 = df12[df12.Roadway_functional_class_description.isin(['Minor Arterial (Urban)','Other Principal Arterial (PAS)','Minor Arterial (Non-Urban)','Collector (Urban)'])]
            df122 = df121[df121.Intersection_related!='Y']
            df123 = df122[df122.Type_of_crash.isin(['Fixed Object','Head On','Overturned','Sideswipe Opposite Direction'])]
            res.append(odf.loc[df121.index].KA.sum()/odf.loc[df12.index].KA.sum())
            res.append(odf.loc[df122.index].KA.sum()/odf.loc[df121.index].KA.sum())
            res.append(odf.loc[df123.index].KA.sum()/odf.loc[df122.index].KA.sum())
            res.append(odf.loc[df123[df123.Type_of_crash.isin(['Fixed Object'])].index].KA.sum()/odf.loc[df123.index].KA.sum())

            df3 = df[df.Day_of_week_name.isin(['Saturday','Sunday','Friday'])]
            res.append(odf.loc[df3.index].KA.sum()/odf.KA.sum())
            df3 = df[(df.Day_of_week_name.isin(['Saturday','Sunday']))]
            res.append(odf.loc[df3[(df3.Time.isin(TimeOrder[0:6]))].index].KA.sum()/odf.loc[df3.index].KA.sum())
            
            res.append(odf[odf.Month.isin(['Apr','May'])].KA.sum()/odf.KA.sum())
            res.append(odf[odf.Vehicle_Type.isin(['Passenger'])].KA.sum()/odf.KA.sum())
            
        if AC=='IM':
            odf = Occ_DF.loc[df.index]
            odf1 = odf[odf.County_name.isin(['Cook','Will','DuPage'])]
            res.append(odf1.KA.sum()/odf.KA.sum())
            res.append(odf1[odf1.RoadwayDeparture=='X'].KA.sum()/odf1.KA.sum())
            res.append(odf1[odf1.SpeedingAggressiveDriver=='X'].KA.sum()/odf1.KA.sum())
            res.append(odf1[odf1.Unrestrained_Occupants_ISHSP=='X'].KA.sum()/odf1.KA.sum())
            
            res.append(df[df.Day_of_week_name.isin(['Saturday','Sunday'])].KA.sum()/df.KA.sum())

            L1 = TimeOrder[0:6]
            L2 = TimeOrder[20:25]
            L3 = L1+L2
            df2 = df[df.Time.isin(L3)]
            res.append(df2.KA.sum()/df.KA.sum())
            res.append(df2[((df2.Day_of_week_name=='Friday') & (df2.Time.isin(L2))) | ((df2.Day_of_week_name=='Saturday') & (df2.Time.isin(L1)))].KA.sum()/df2.KA.sum())
            res.append(df2[((df2.Day_of_week_name=='Saturday') & (df2.Time.isin(L2))) | ((df2.Day_of_week_name=='Sunday') & (df2.Time.isin(L1)))].KA.sum()/df2.KA.sum())
            res.append(df2[((df2.Day_of_week_name=='Sunday') & (df2.Time.isin(L2))) | ((df2.Day_of_week_name=='Monday') & (df2.Time.isin(L1)))].KA.sum()/df2.KA.sum())

            df1 = df[df.State_Local_Urban_Rural.isin(['Local Urban','State Urban'])]
            res.append(df1.KA.sum()/df.KA.sum())
            df11 = df1[df1.Roadway_functional_class_description.isin(['Minor Arterial (Urban)','Other Principal Arterial (PAS)','Minor Arterial (Non-Urban)','Collector (Urban)'])]
            res.append(df11.KA.sum()/df1.KA.sum())
            df111 = df11[df11.State_Local_Urban_Rural.isin(['Local Urban'])]
            res.append(df111.KA.sum()/df1.KA.sum())
            df1111 = df111[df111.RoadwayDeparture=='X']
            res.append(df1111.KA.sum()/df111.KA.sum())
            res.append(df111[df111.Intersection_related=='Y'].KA.sum()/df111.KA.sum())
            res.append(df1111[df1111.Type_of_crash=='Fixed Object'].KA.sum()/df1111.KA.sum())
            res.append(df1[df1.Roadway_functional_class_description.isin(['Interstate (PAS)','Freeway and Expressway (Urban Only) (PAS)'])].KA.sum()/df1.KA.sum())
                            
            df1 = df[df.State_Local_Urban_Rural.isin(['Local Rural','State Rural'])]
            df11 = df1[df1.Roadway_functional_class_description.isin(['Minor Arterial (Urban)',
                                                                      'Major Collector (Non-Urban)',
                                                                      'Other Principal Arterial (PAS)',
                                                                      'Minor Arterial (Non-Urban)',
                                                                      'Minor Collector (Non-Urban)',
                                                                      'Collector (Urban)'])]
            res.append(df11.KA.sum()/df1.KA.sum())
            df12 = df11[df11.State_Local_Urban_Rural.isin(['Local Rural'])]
            res.append(df12.KA.sum()/df11.KA.sum())
            
            df111 = df11[df11.RoadwayDeparture=='X']
            res.append(df111.KA.sum()/df11.KA.sum())
            res.append(df111[df111.Type_of_crash=='Fixed Object'].KA.sum()/df111.KA.sum())
            res.append(df111[df111.UnrestrainedOccupants_ISHSP=='X'].KA.sum()/df111.KA.sum())
            res.append(df11[df11.UnrestrainedOccupants_ISHSP=='X'].KA.sum()/df11.KA.sum())
            res.append(df11[df11.SpeedingAggressiveDriver=='X'].KA.sum()/df11.KA.sum())
            
            df111 = df12[df12.RoadwayDeparture=='X']
            res.append(df111.KA.sum()/df12.KA.sum())
            res.append(df111[df111.Type_of_crash=='Fixed Object'].KA.sum()/df111.KA.sum())
            res.append(df111[df111.UnrestrainedOccupants_ISHSP=='X'].KA.sum()/df111.KA.sum())
            
            
        if AC=='DF':
            df1 = df[df.State_Local_Urban_Rural.isin(['Local Urban','State Urban'])]
            res.append(df1.KA.sum()/df.KA.sum())
            df11 = df[df.State_Local_Urban_Rural.isin(['State Urban'])]
            res.append(df11.KA.sum()/df1.KA.sum())
            df12 = df[df.State_Local_Urban_Rural.isin(['Local Urban'])]
            res.append(df12.KA.sum()/df1.KA.sum())

            cr = df11.groupby('Crash_Year')['KA'].aggregate(sum)
            mf120 = {1:'increased',-1:'decreased'}[np.sign(cr[y[-1]]-cr[y[0]])]
            #mf12 = (LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B)
            mf12 = abs(cr[y[-1]]-cr[y[0]])/cr[y[0]]
            mf13 = mf12/(len(y)-1)
            mf131 = {-1:'reduction',1:'increase'}[np.sign(cr[y[-1]]-cr[y[0]])]
            res.extend([mf120,mf12,mf13,mf131])
            
            cr = df12.groupby('Crash_Year')['KA'].aggregate(sum)
            mf120 = {1:'increased',-1:'decreased'}[np.sign(cr[y[-1]]-cr[y[0]])]
            #mf12 = (LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B)
            mf12 = abs(cr[y[-1]]-cr[y[0]])/cr[y[0]]
            mf13 = mf12/(len(y)-1)
            mf131 = {-1:'reduction',1:'increase'}[np.sign(cr[y[-1]]-cr[y[0]])]
            res.extend([mf120,mf12,mf13,mf131])
            
            df121 = df12[df12.Roadway_functional_class_description.isin(['Minor Arterial (Urban)','Other Principal Arterial (PAS)','Minor Arterial (Non-Urban)','Collector (Urban)'])]
            res.append(df121.KA.sum()/df12.KA.sum())
            
            df1211 = df121[df121.Intersection_related!='Y']
            res.append(df1211.KA.sum()/df121.KA.sum())
            df1212 = df1211[df1211.RoadwayDeparture=='X']
            res.append(df1212.KA.sum()/df1211.KA.sum())
            res.append(df1212[df1212.Type_of_crash=='Fixed Object'].KA.sum()/df1212.KA.sum())
            
            res.append(df[df.Day_of_week_name.isin(['Friday','Saturday','Thursday'])].KA.sum()/df.KA.sum())

            res.append(df[df.Time.isin([TimeOrder[16]])].KA.sum()/df.KA.sum())
            res.append(df[df.Time.isin(TimeOrder[12:18])].KA.sum()/df.KA.sum())
            res.append(df[df.Month.isin(['Jun','Jul','Aug'])].KA.sum()/df.KA.sum())
            res.append(df[df.Cause1=='Distraction - From Inside Vehicle'].KA.sum()/df.KA.sum())
            res.append(df[df.Cause1=='Physical Condition of Driver'].KA.sum()/df.KA.sum())
            
        if AC=='OD':
            df1 = df[df.State_Local_Urban_Rural.isin(['Local Urban','State Urban'])]
            res.append(df1.KA.sum()/df.KA.sum())
            df11 = df[df.State_Local_Urban_Rural.isin(['State Urban'])]
            df12 = df[df.State_Local_Urban_Rural.isin(['Local Urban'])]

            cr = df11.groupby('Crash_Year')['KA'].aggregate(sum)
            mf120 = {1:'increased',-1:'decreased'}[np.sign(cr[y[-1]]-cr[y[0]])]
            #mf12 = (LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B)
            mf12 = abs(cr[y[-1]]-cr[y[0]])/cr[y[0]]
            mf13 = mf12/(len(y)-1)
            mf131 = {-1:'reduction',1:'increase'}[np.sign(cr[y[-1]]-cr[y[0]])]
            res.extend([mf120,mf12])
            
            cr = df12.groupby('Crash_Year')['KA'].aggregate(sum)
            mf120 = {1:'increased',-1:'decreased'}[np.sign(cr[y[-1]]-cr[y[0]])]
            #mf12 = (LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B)
            mf12 = abs(cr[y[-1]]-cr[y[0]])/cr[y[0]]
            mf13 = mf12/(len(y)-1)
            mf131 = {-1:'reduction',1:'increase'}[np.sign(cr[y[-1]]-cr[y[0]])]
            res.extend([mf120,mf12])

            res.append(df11.KA.sum()/df1.KA.sum())
            df111 = df11[df11.Roadway_functional_class_description.isin(['Minor Arterial (Urban)',
                                                                      'Major Collector (Non-Urban)',
                                                                      'Other Principal Arterial (PAS)',
                                                                      'Minor Arterial (Non-Urban)',
                                                                      'Minor Collector (Non-Urban)',
                                                                      'Collector (Urban)'])]
            res.append(df111.KA.sum()/df11.KA.sum())
            df1111 = df111[df111.Intersection_related=='Y']
            res.append(df1111.KA.sum()/df111.KA.sum())
            df1112 = df1111[(df1111.Traffic_Device=='Traffic Signal')] 
            res.append(df1112.KA.sum()/df1111.KA.sum())
            df1113 = df1112[(df1112.Collision_type_code.isin([10,15]))] 
            res.append(df1113.KA.sum()/df1112.KA.sum())
            
            res.append(df12.KA.sum()/df1.KA.sum())
            df111 = df12[df12.Roadway_functional_class_description.isin(['Minor Arterial (Urban)',
                                                                      'Major Collector (Non-Urban)',
                                                                      'Other Principal Arterial (PAS)',
                                                                      'Minor Arterial (Non-Urban)',
                                                                      'Minor Collector (Non-Urban)',
                                                                      'Collector (Urban)'])]
            res.append(df111.KA.sum()/df12.KA.sum())
            df1111 = df111[df111.Intersection_related=='Y']
            res.append(df1111.KA.sum()/df111.KA.sum())
            df1112 = df1111[(df1111.Traffic_Device=='Traffic Signal')] 
            res.append(df1112.KA.sum()/df1111.KA.sum())
            df1113 = df1112[(df1112.Collision_type_code.isin([10,15]))] 
            res.append(df1113.KA.sum()/df1112.KA.sum())
            
            df1 = df[df.State_Local_Urban_Rural.isin(['Local Rural','State Rural'])]
            res.append(df1.KA.sum()/df.KA.sum())
            df11 = df[df.State_Local_Urban_Rural.isin(['State Rural'])]
            df12 = df[df.State_Local_Urban_Rural.isin(['Local Rural'])]

            cr = df11.groupby('Crash_Year')['KA'].aggregate(sum)
            mf120 = {1:'increased',-1:'decreased'}[np.sign(cr[y[-1]]-cr[y[0]])]
            #mf12 = (LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B)
            mf12 = abs(cr[y[-1]]-cr[y[0]])/cr[y[0]]
            mf13 = mf12/(len(y)-1)
            mf131 = {-1:'reduction',1:'increase'}[np.sign(cr[y[-1]]-cr[y[0]])]
            res.extend([mf120,mf12])
            
            cr = df12.groupby('Crash_Year')['KA'].aggregate(sum)
            mf120 = {1:'increased',-1:'decreased'}[np.sign(cr[y[-1]]-cr[y[0]])]
            #mf12 = (LineFun(y[-1],A,B)-LineFun(y[0],A,B))/LineFun(y[0],A,B)
            mf12 = abs(cr[y[-1]]-cr[y[0]])/cr[y[0]]
            mf13 = mf12/(len(y)-1)
            mf131 = {-1:'reduction',1:'increase'}[np.sign(cr[y[-1]]-cr[y[0]])]
            res.extend([mf120,mf12])
            
            res.append(df[df.Day_of_week_name.isin(['Friday','Wednesday','Thursday'])].KA.sum()/df.KA.sum())
            res.append(df[df.Cause_1_code.isin([5])].KA.sum()/Crash_DF[Crash_DF.Cause_1_code.isin([5])].KA.sum())
            
        if AC=='YD':
            odf = Occ_DF.loc[df.index]
            res.append(odf[(odf.Age<18)].KA.sum()/odf.KA.sum())
            df1 = df[df.Intersection_related=='Y']
            res.append(df1.KA.sum()/df.KA.sum())
            df11 = df1[(df1.Traffic_Device=='Traffic Signal')] 
            res.append(df11.KA.sum()/df1.KA.sum())
            res.append(df[df.RoadwayDeparture=='X'].KA.sum()/df.KA.sum())
            res.append(df[(~df.Day_of_week_name.isin(['Sturday','Sunday'])) & (df.Time.isin(TimeOrder[12:17]))].KA.sum()/df.KA.sum())

            odf1 = odf[(odf['Person Type']==1) & (odf.Age<21)]
            res.append(odf1.KA.sum()/odf.KA.sum())
            res.append(odf1[odf1.Sex=='M'].KA.sum()/odf1.KA.sum())
            res.append(odf1[odf1.Unrestrained_Occupants_ISHSP=='X'].KA.sum()/odf1.KA.sum())
            res.append(Occ_DF[Occ_DF.CaseNum_UnitNo.isin(odf1.CaseNum_UnitNo)].groupby('CaseNum_UnitNo').size().value_counts(True).loc[1])

            res.append(df[df.SpeedingAggressiveDriver=='X'].KA.sum()/df.KA.sum())
            
            
            df1 = df[df.State_Local_Urban_Rural.isin(['Local Urban','State Urban'])]
            res.append(df1.KA.sum()/df.KA.sum())
            df11 = df[df.State_Local_Urban_Rural.isin(['State Urban'])]
            df12 = df[df.State_Local_Urban_Rural.isin(['Local Urban'])]

            df111 = df11[df11.Roadway_functional_class_description.isin(['Minor Arterial (Urban)',
                                                                      'Major Collector (Non-Urban)',
                                                                      'Other Principal Arterial (PAS)',
                                                                      'Minor Arterial (Non-Urban)',
                                                                      'Minor Collector (Non-Urban)',
                                                                      'Collector (Urban)'])]
            res.append(df111.KA.sum()/df11.KA.sum())
            df1111 = df111[df111.Intersection_related=='Y']
            res.append(df1111.KA.sum()/df111.KA.sum())
            df1112 = df1111[(df1111.Traffic_Device=='Traffic Signal')] 
            res.append(df1112.KA.sum()/df1111.KA.sum())
            
            df111 = df12[df12.Roadway_functional_class_description.isin(['Minor Arterial (Urban)',
                                                                      'Major Collector (Non-Urban)',
                                                                      'Other Principal Arterial (PAS)',
                                                                      'Minor Arterial (Non-Urban)',
                                                                      'Minor Collector (Non-Urban)',
                                                                      'Collector (Urban)'])]
            res.append(df111.KA.sum()/df12.KA.sum())
            df1111 = df111[df111.Intersection_related=='Y']
            res.append(df1111.KA.sum()/df111.KA.sum())
            df1112 = df1111[(df1111.Traffic_Device=='Traffic Signal')] 
            res.append(df1112.KA.sum()/df1111.KA.sum())
            
            df1 = df[df.State_Local_Urban_Rural.isin(['Local Rural'])]
            df11 = df1[df1.Roadway_functional_class_description.isin(['Minor Arterial (Urban)',
                                                                      'Major Collector (Non-Urban)',
                                                                      'Other Principal Arterial (PAS)',
                                                                      'Minor Arterial (Non-Urban)',
                                                                      'Minor Collector (Non-Urban)',
                                                                      'Collector (Urban)'])]
            res.append(df11.KA.sum()/df1.KA.sum())
            df12 = df11[df11.RoadwayDeparture=='X']
            res.append(df12.KA.sum()/df11.KA.sum())
            odf1 = Occ_DF.loc[df12.index]
            res.append(odf1[odf1.Unrestrained_Occupants_ISHSP=='X'].KA.sum()/odf1.KA.sum())

            df12 = df1[df1.Roadway_functional_class_description.isin(['Local Road or Street (Non-Urban)',
                                                                      'Local Road or Street (Urban)'])]
            res.append(df12.KA.sum()/df1.KA.sum())
            df13 = df12[df12.RoadwayDeparture=='X']
            res.append(df13.KA.sum()/df12.KA.sum())
            res.append(df13[df13.Type_of_crash=='Fixed Object'].KA.sum()/df13.KA.sum())
            res.append(df13[df13.SpeedingAggressiveDriver=='X'].KA.sum()/df13.KA.sum())
            odf1 = Occ_DF.loc[df13.index]
            res.append(odf1[odf1.Unrestrained_Occupants_ISHSP=='X'].KA.sum()/odf1.KA.sum())
            
        if AC=='HV':
            odf = Occ_DF.loc[df.index]
            idx1 = list(set(Veh_DF[(Veh_DF.VEHT.isin([7,8])) & (Veh_DF.Crash_Year.isin(y))].index))
            res.append(df.loc[idx1].KA.sum()/df.KA.sum())
            idx1 = list(set(Veh_DF[(Veh_DF.VEHT.isin([4,5])) & (Veh_DF.Crash_Year.isin(y))].index))
            res.append(df.loc[idx1].KA.sum()/df.KA.sum())
            #idx1 = list(set(Veh_DF[(Veh_DF.VEHT.isin([6])) & (Veh_DF.Crash_Year.isin(y))].index))
            #res.append(df.loc[idx1].KA.sum()/df.KA.sum())
            df1 = df[df.Roadway_functional_class_description.isin(['Interstate (PAS)','Freeway and Expressway (Urban Only) (PAS)'])]
            res.append(df1.KA.sum()/df.KA.sum())
            idx1 = list(set(Veh_DF[(Veh_DF.VEHT.isin([7,8])) & (Veh_DF.Crash_Year.isin(y))].index))
            res.append(df1.loc[idx1].KA.sum()/df1.KA.sum())
            idx2 = list(set(Veh_DF[(Veh_DF.VEHT.isin([6])) & (Veh_DF.Crash_Year.isin(y))].index))
            res.append(df1.loc[idx2].KA.sum()/df1.KA.sum())
            
            df1 = df.loc[idx1]
            df2 = df1[df1.RoadwayDeparture=='X']
            res.append(df2.KA.sum()/df1.KA.sum())
            res.append(df2[df2.Alignment.isin(['Curve, Level','Curve On Grade','Curve On Hillcrest'])].KA.sum()/df2.KA.sum())
            
            df2 = df[df.Intersection_related=='Y']
            res.append(df2.KA.sum()/df.KA.sum())
            
            df11 = df2[df2.Roadway_functional_class_description.isin(['Minor Arterial (Urban)',
                                                                      'Major Collector (Non-Urban)',
                                                                      'Other Principal Arterial (PAS)',
                                                                      'Minor Arterial (Non-Urban)',
                                                                      'Minor Collector (Non-Urban)',
                                                                      'Collector (Urban)'])]
            res.append(df11.KA.sum()/df2.KA.sum())
            df21 = df2[df2.State_Local_Urban_Rural.isin(['Local Urban','Local Rural'])]
            res.append(df21.KA.sum()/df2.KA.sum())
            idx1 = list(set(Veh_DF[(Veh_DF.VEHT.isin([4,5])) & (Veh_DF.Crash_Year.isin(y))].index))
            res.append(df2.loc[idx1].KA.sum()/df2.KA.sum())
            df3 = df2.loc[idx1]
            res.append(df3[df3.Type_of_crash=='Rear End'].KA.sum()/df3.KA.sum())
            
            res.append(df[df.Alignment.isin(['Curve, Level','Curve On Grade','Curve On Hillcrest'])].KA.sum()/df.KA.sum())
            
        if AC=='MC':
            odf = Occ_DF.loc[df.index]
            res.append(odf[odf.Safety_Equipment=='Helmet Used'].KA.sum()/odf.KA.sum())
            res.append(odf[~odf.Safety_Equipment.isin(['Unknown/NA','Helmet Used'])].KA.sum()/odf.KA.sum())
            res.append(odf[odf.Safety_Equipment=='Unknown/NA'].KA.sum()/odf.KA.sum())
            idx1 = list(set(Veh_DF[(Veh_DF.VEHT.isin([10,11])) & (Veh_DF.UnitNo==1)].index))
            df1 = df.loc[idx1]
            res.append(df1.KA.sum()/df.KA.sum())
            
            odf1 = odf.loc[idx1]
            odf1 = odf1[odf1.UnitNo==1]
            res.append(odf1[~odf1.Safety_Equipment.isin(['Unknown/NA','Helmet Used'])].shape[0]/odf1.shape[0])
            res.append(odf1[odf1.ImpairedDriver=='X'].shape[0]/odf1.shape[0])
            
            df2 = df[df.RoadwayDeparture=='X']
            res.append(df2.KA.sum()/df.KA.sum())
            res.append(df2[df2.SpeedingAggressiveDriver=='X'].KA.sum()/df2.KA.sum())
            res.append(df2[df2.ImpairedDriver=='X'].KA.sum()/df2.KA.sum())
            
            odf1 = odf[odf.Sex=='M']
            res.append(odf1.KA.sum()/odf.KA.sum())
            res.append(odf1.loc[idx1].KA.sum()/odf1.KA.sum())
            
            odf3 = odf[odf.Younger_Driver21to25=='X']
            res.append(odf3.KA.sum()/odf.KA.sum())

            df3 = df[df.State_Local_Urban_Rural.isin(['State Urban','Local Urban'])]
            res.append(df3.KA.sum()/df.KA.sum())
            
            res.append(df[df.Month.isin(['May','Jun','Jul','Aug','Sep'])].KA.sum()/df.KA.sum())            
            res.append(df[df.Month.isin(['Jul'])].KA.sum()/df.KA.sum())            
            
            res.append(df[df.Day_of_week_name.isin(['Sunday','Saturday'])].KA.sum()/df.KA.sum())

            res.append(df[df.Time.isin(TimeOrder[18:24])].KA.sum()/df.KA.sum())

        if AC=='TN':
            df1 = df[(df.Traffic_control_device_code.isin([6,7]))] 
            res.append(df1.KA.sum()/df.KA.sum())
            res.append(df1[df.Traffic_control_device_code.isin([6])].KA.sum()/df.KA.sum())
            res.append(df1[df.Traffic_control_device_code.isin([7])].KA.sum()/df.KA.sum())
            
            df2 = df[df.State_Local_Urban_Rural.isin(['State Urban','Local Urban'])]
            df3 = df[df.State_Local_Urban_Rural.isin(['State Rural','Local Rural'])]
            res.append(df2.KA.sum()/df.KA.sum())
            res.append(df3.KA.sum()/df.KA.sum())

            res.append(df[df.OlderDriver65plus=='X'].KA.sum()/df.KA.sum())
            res.append(df[df.ImpairedDriver=='X'].KA.sum()/df.KA.sum())
            
            df4 = df3[df3.Roadway_functional_class_description.isin(['Minor Arterial (Urban)',
                                                                      'Major Collector (Non-Urban)',
                                                                      'Other Principal Arterial (PAS)',
                                                                      'Minor Arterial (Non-Urban)',
                                                                      'Minor Collector (Non-Urban)',
                                                                      'Collector (Urban)'])]
            res.append(df4.KA.sum()/df3.KA.sum())

            df5 = df3[df3.Roadway_functional_class_description.isin(['Local Road or Street (Non-Urban)',
                                                                      'Local Road or Street (Urban)'])]
            res.append(df5.KA.sum()/df3.KA.sum())
            
            res.append(df4[df4.OlderDriver65plus=='X'].KA.sum()/df4.KA.sum())
            res.append(df4[df4.ImpairedDriver=='X'].KA.sum()/df4.KA.sum())
            odf = Occ_DF.loc[df4.index]
            res.append(odf[odf.Unrestrained_Occupants_ISHSP=='X'].KA.sum()/odf.KA.sum())
            
            res.append(df5[df5.OlderDriver65plus=='X'].KA.sum()/df5.KA.sum())
            res.append(df5[df5.ImpairedDriver=='X'].KA.sum()/df5.KA.sum())
            odf = Occ_DF.loc[df5.index]
            res.append(odf[odf.Unrestrained_Occupants_ISHSP=='X'].KA.sum()/odf.KA.sum())
            
            res.append(df5[df5.Cause_1_code.isin([2])].KA.sum()/df5.KA.sum())
            res.append(df5[df5.Cause_1_code.isin([24])].KA.sum()/df5.KA.sum())
            
            df4 = df2[df2.Roadway_functional_class_description.isin(['Minor Arterial (Urban)',
                                                                      'Major Collector (Non-Urban)',
                                                                      'Other Principal Arterial (PAS)',
                                                                      'Minor Arterial (Non-Urban)',
                                                                      'Minor Collector (Non-Urban)',
                                                                      'Collector (Urban)'])]
            res.append(df4.KA.sum()/df2.KA.sum())

            df5 = df2[df2.Roadway_functional_class_description.isin(['Local Road or Street (Non-Urban)',
                                                                      'Local Road or Street (Urban)'])]
            res.append(df5.KA.sum()/df2.KA.sum())
            
            res.append(df4[df4.OlderDriver65plus=='X'].KA.sum()/df4.KA.sum())
            res.append(df4[df4.ImpairedDriver=='X'].KA.sum()/df4.KA.sum())
            odf = Occ_DF.loc[df4.index]
            res.append(odf[odf.Unrestrained_Occupants_ISHSP=='X'].KA.sum()/odf.KA.sum())
            res.append(df4[df4.Cause_1_code.isin([25])].KA.sum()/df4.KA.sum())
            res.append(df4[df4.Cause_1_code.isin([24])].KA.sum()/df4.KA.sum())
            res.append(df5[df5.ImpairedDriver=='X'].KA.sum()/df5.KA.sum())
            
        if AC=='WZ':    
            df1 = df[df.State_Local_Urban_Rural.isin(['State Urban','State Rural'])]
            df2 = df[df.State_Local_Urban_Rural.isin(['State Urban','Local Urban'])]
            res.append(df1.KA.sum()/df.KA.sum())
            res.append(df2.KA.sum()/df.KA.sum())
            df3 = df[df.State_Local_Urban_Rural.isin(['State Urban'])]
            res.append(df3.KA.sum()/df.KA.sum())
            res.append(df[df.SpeedingAggressiveDriver=='X'].KA.sum()/df.KA.sum())

            df4 = df3[df3.Roadway_functional_class_description.isin(['Interstate (PAS)','Freeway and Expressway (Urban Only) (PAS)'])]
            res.append(df4.KA.sum()/df3.KA.sum())
            df5 = df4[df4.HeavyVehicle=='X']
            res.append(df5.KA.sum()/df4.KA.sum())
            res.append(df5[df5.SpeedingAggressiveDriver=='X'].KA.sum()/df5.KA.sum())
            res.append(df5[df5.Collision_type_code.isin([11])].KA.sum()/df5.KA.sum())

            df6 = df4[df4.UnrestrainedOccupants_ISHSP=='X']
            res.append(df6.KA.sum()/df4.KA.sum())
            res.append(df6[df6.ImpairedDriver=='X'].KA.sum()/df6.KA.sum())

            df7 = df4[df4.OlderDriver65plus=='X']
            res.append(df7.KA.sum()/df4.KA.sum())
            res.append(df7[df.Light_condition_code.isin([2,3,4,5])].KA.sum()/df7.KA.sum())

            df8 = df2[df2.Roadway_functional_class_description.isin(['Minor Arterial (Urban)',
                                                                      'Major Collector (Non-Urban)',
                                                                      'Other Principal Arterial (PAS)',
                                                                      'Minor Arterial (Non-Urban)',
                                                                      'Minor Collector (Non-Urban)',
                                                                      'Collector (Urban)'
                                                                  ])]
            res.append(df8.KA.sum()/df.KA.sum())
            df9 = df8[df8.State_Local_Urban_Rural.isin(['State Urban','State Rural'])]
            res.append(df9.KA.sum()/df8.KA.sum())
            df10 = df9[df9.Intersection_related=='Y']
            res.append(df10.KA.sum()/df9.KA.sum())
            res.append(df10[df10.Collision_type_code.isin([10])].KA.sum()/df10.KA.sum())
            res.append(df10[df10.Collision_type_code.isin([11])].KA.sum()/df10.KA.sum())
            
            df11 = df9[df9.UnrestrainedOccupants_ISHSP=='X']
            res.append(df11.KA.sum()/df9.KA.sum())
            res.append(df11[df11.ImpairedDriver=='X'].KA.sum()/df11.KA.sum())
            
            df11 = df9[df9.RoadwayDeparture=='X']
            res.append(df11.KA.sum()/df9.KA.sum())
            res.append(df11[df11.SpeedingAggressiveDriver=='X'].KA.sum()/df11.KA.sum())
            
        Res.append(res)
    df = pd.DataFrame()
    df['Y10_14'] = Res[0]
    df['Y12_16'] = Res[1]
    df['Reduction'] = [CalRed(y1,y2) for y1,y2 in zip(df.Y10_14,df.Y12_16)]
    df.index = ['mf{}'.format(i+1) for i in range(len(df))]
    return(df)
def UpdateBPDoc(AC,df):
    template = Project_Dir + '\\Template\\{}_MergeDocument.docx'.format(AC)
    document = MailMerge(template)
    document.merge(**{i:FormatPercentages(r) for i,r in df.iterrows()})
    document.merge(**{i+'c':FormatReduction(r) for i,r in df.iterrows() if abs(r.Reduction)>0.02})
    document.write(OutputDir + '\\{}_Bullets.docx'.format(AC))    
    document.close()   

#IL Crash Data
def SunAngle(lat,lon,dt):
    import astropy.coordinates as coord
    tz = "America/Chicago"
    try:
        loc = coord.EarthLocation(lon=lon,lat=lat)
        now = astropy.time.Time(pytz.timezone(tz).localize(dt, is_dst=None).astimezone(pytz.utc))
        altaz = coord.AltAz(location=loc, obstime=now)
        sun = astropy.coordinates.get_sun(now)
        return(sun.transform_to(altaz).alt.deg)
    except:
        #print('Sun Angle Failed: {},{} @ {}'.format(lat,lon,dt))
        pass
def DayNight(d,s):
    if s<-6:
        return(4) #Night
    if s>0:
        return(2) #Day
    if s>=-6 and s <=0:
        if d.hour<12:
            return(1) #Dwan
        else:
            return(3) #Dusk
def GetCrashTime(y,m,d,s,h):
    y += 2000
    h1 = int(s.split(':')[0])
    mm = int(s.split(':')[1].split(' ')[0])
    ampm = s.split(':')[1].split(' ')[1]
    if ampm == 'PM':
            if h1<12:
                h1+=12
    #if h1!=h:
        #print(' - Crash Hour: {}, Crash Time: {}'.format(h,s))
    return(datetime(int(y),int(m),int(d),int(h),int(mm)))
def ConvToInt(s):
    try:
        return(int(s))
    except:
        pass
def DOBtoDatetime(dob):
    try:
        dob = int(dob)
        if len(str(dob))==7:
            m = int(str(dob)[0])
            d = int(str(dob)[1:3])
            y = int(str(dob)[3:7])
            if y>1800 and y<2020:
                return(datetime(y,m,d,0,0))
        if len(str(dob))==8:
            m = int(str(dob)[0:2])
            d = int(str(dob)[2:4])
            y = int(str(dob)[4:8])
            if y>1800 and y<2020:
                return(datetime(y,m,d,0,0))
    except:
        pass    
def FindKABCO(pdf,i):
    v_c = pd.Series(index=[0,1,2,3,4],name='INJ_SEV')
    v_c = v_c.fillna(0)
    if i in pdf.index:
        i_s = pdf.loc[i,'INJ_SEV']
    else:
        print('[{}]  - {} not in person file'.format(strftime("%Y-%m-%d %H:%M:%S"),i))
        v_c.index = ['O','C','B','A','K']
        v_c.loc['KABCO'] = 'O'
        return(v_c)
    v_c.loc[i_s.value_counts().index] = i_s.value_counts()
    v_c.index = ['O','C','B','A','K']
    v_c.loc['KABCO'] = {4:'K',3:'A',2:'B',1:'C',0:'O'}[max(i_s)]
    return(v_c)
def IndexList(DF,idx):
    try:
        n = len(DF.index.levels)
    except:
        n = 1
    try:
        m = len(idx[0])
    except:
        m = 1
    if n==1:
        if m==1:
            return(idx)
        else:
            return([i[0] for i in idx])
    if n==2:
        if m==3:
            L = [(i[0],i[1]) for i in idx]
            L0 = list(DF.index)
            L = [v for v in L if v in L0]
            return(L)
        if m==1:
            L0 = [i[0] for i in DF.index]
            L = [v for v in idx if v in L0]
            return(L)
        if m==2:
            L0 = list(DF.index)
            L = [v for v in idx if v in L0]
            return(L)
    if n==3:
        if m==1:
            L0 = [i[0] for i in DF.index]
            L = [v for v in idx if v in L0]
            return(L)
        if m==3:
            L0 = list(DF.index)
            L = [v for v in idx if v in L0]
            return(L)
        if m==2:
            df = DF.copy(True)
            df['PersonID'] = [i[2] for i in df.index]
            df.index = df.index.droplevel(level=2)
            df = df.loc[idx]
            df = df[~pd.isnull(df.PersonID)]
            t = [(i[0],i[1],p) for i,p in zip(df.index, df.PersonID)]
            df.index = pd.MultiIndex.from_tuples(t,names=['CID','UnitID','OccID'])
            return(list(df.index))
def FixIndex(i):
    if len(str(i))==8:
        s = str(i)
        s1 = '200' + s[0] + '0' + s[1:]
        return(int(s1))
    else:
        return(i)
def Crash_MDBExtToCSV(In_CSV,Out_CSV):
    print('[{}] Read Data: {}'.format(strftime("%Y-%m-%d %H:%M:%S"),In_CSV))

    WZTypeDict = {'(N/A)':1, 
                  'Construction Work Zone':2,
                  'Construction':2, 
                  'Maintenance':3, 
                  'Maintenance Work Zone':3, 
                  'Utility':4,
                  'Utility Work Zone':4, 
                  'Unk. Work Zone Type':5, 
                  'Unknown':5
                 }
    df = pd.read_csv(In_CSV,low_memory=False, encoding='latin-1')
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape))

    print('[{}] Data Clean ups'.format(strftime("%Y-%m-%d %H:%M:%S")))
    # Index Data
    if 'CaseNum' in df.columns:
        df['Casenum'] = df.CaseNum
    df['Casenum'] = df.Casenum.apply(ConvToInt).apply(FixIndex)
    df = df[(~pd.isnull(df.Casenum))]
    df.index = df.Casenum.apply(FixIndex)
    df.index.name = 'CID'
    #Sort
    df = df.sort_index()
    
    df.X_COORD = df.X_COORD.fillna(0)
    df.Y_COORD = df.Y_COORD.fillna(0)
    df.Crash_latitude = df.Crash_latitude.fillna(0)
    df.Crash_longitude = df.Crash_longitude.fillna(0)
    df.loc[df.X_COORD<1,'X_COORD'] = 0
    df.loc[df.Y_COORD<1,'Y_COORD'] = 0
    idx = (df.X_COORD==0) & (df.Y_COORD==0) & (df.Crash_latitude!=0) & (df.Crash_longitude!=0)
    n1 = df[(df.X_COORD!=0) & (df.Y_COORD!=0)].shape[0]
    pl = [arcpy.PointGeometry(arcpy.Point(-r.Crash_longitude,r.Crash_latitude),common.WGS1984).projectAs(common.NAD1983IL) for i,r in df.loc[idx].iterrows()]
    df.loc[idx,'X_COORD'] = [p.firstPoint.X for p in pl]
    df.loc[idx,'Y_COORD'] = [p.firstPoint.Y for p in pl]

    WeatherDict = {1:'Clear', 8:'Cloudy/Overcast', 4:'Fog/Smoke/Haze', 7:'Other', 2:'Rain', 6:'Severe Cross Wind', 5:'Sleet/Hail', 3:'Snow', 9:'Unknown'}
    if not 'Weather_code' in list(df.columns):
        df['Weather_code'] = [{v:k for k,v in WeatherDict.items()}[val] for val in df.Weather]
    if not 'County_code' in list(df.columns):
        df['County_code'] = df['County_Code']
    if not 'Class_of_Trafficway_code' in list(df.columns):
        df['Class_of_Trafficway_code'] = df['Class_of_Trafficway_Code']
    for f in ['OccurInWorkZone','Intersection_related','Hit_and_run','Work_zone_related']:
        df[f] = df[f].fillna('N')
    
    # Convert Data
    df['Date'] = [GetCrashTime(y,m,d,t,h) for y,m,d,t,h in zip(df.Crash_Year,df.Crash_Month,df.Crash_Day,df.Time_of_crash,df.Hour_)]
    for f in ['Intersection_related','Hit_and_run','Work_zone_related','OccurInWorkZone']:
        df[f] = [{'Y':1,'N':0}[v] for v in df[f]]
    for f in ['WorkersPresent']:
        df.loc[~pd.isnull(df[f]),f] = [{'Y':1,'N':0}[v] for v in df.loc[~pd.isnull(df[f]),f]]

    df['WorkZoneType'] = df['WorkZoneType'].fillna('(N/A)')
    df['WorkZoneType'] = [WZTypeDict[v] for v in df['WorkZoneType']]
    # Fillna
    for f in ['Cause_1_code','Cause_2_code','Traffic_control_device_code']:
        df[f] = df[f].fillna(99)
    for f in ['Road_surface_condition_code','Light_condition_code','Weather_code','Traffic_control_condition_code']:
        df[f] = df[f].fillna(9)
    for f in ['City_Class_Code']:
        df[f] = df[f].fillna(0)
    for f in ['Alignment_code']:
        df[f] = df[f].fillna(9)
        df.loc[df[f]==0,f] = 9
    for f in ['Road_surface_condition_code']:
        df.loc[df[f]==0,f] = 9
    for f in ['Road_defects_code']:
        df.loc[df[f]==0,f] = 99
    
    
    # Format Columns
    for f in ['County_code','City_Code','City_Class_Code','Nbr_of_Vehicles',
           'Class_of_Trafficway_code','Traffic_control_device_code','Traffic_control_condition_code',
           'Trafficway_description_code','Roadway_functional_class',
           'Collision_type_code','Cause_1_code','Cause_2_code',
           'Agency_code',
              'Intersection_related','Hit_and_run','Work_zone_related',
          'Road_surface_condition_code','Road_defects_code','Light_condition_code','Weather_code','Alignment_code']:
        #df[f] = [ConvToInt(v) for v in df[f]]
        df[f] = df[f].replace(np.NaN,None).astype(int,errors="ignore")
    
    # Select Columns
    F2K = ['Nbr_of_Vehicles','Date','Route_number',
           'County_code','City_Code','City_Class_Code','Township',
           'Class_of_Trafficway_code','Traffic_control_device_code','Traffic_control_condition_code',
           'Trafficway_description_code','Roadway_functional_class',
           'Collision_type_code','Cause_1_code','Cause_2_code',
           'Intersection_related','Hit_and_run',
           'Agency_code',
          'Road_surface_condition_code','Road_defects_code','Light_condition_code','Weather_code','Alignment_code',
           'Work_zone_related','X_COORD','Y_COORD','OccurInWorkZone','WorkZoneType','WorkersPresent'
          ]
    df = df[F2K]
    F2K_N = ['NO_VEH','DATE','RT_NBR',
           'COUNTY','CITY','CITY_CLASS','TOWNSHIP',
           'TWAY_CLASS','TCONT_DEV','TCONT_CON',
           'TWAY_DESC','FUNC_CLASS',
           'COL_TYPE','CAUSE_1','CAUSE_2',
           'INT_REL','HIT_RUN',
           'AGENCY',
          'SURF_CON','DEFECT','LIGHT','WEATHER','ALIGN',
           'WZ_REL','X','Y','WZ_OCCUR','WZ_TYPE','WZ_WORKER'
          ]
    df.columns = F2K_N

    df['YEAR'] = [d.year for d in df.DATE]
    df.loc[df.YEAR<2013,'WZ_OCCUR'] = df.loc[df.YEAR<2013,'WZ_REL']
    df.loc[df.YEAR<2013,'WZ_TYPE'] = df.loc[df.YEAR<2013,'DEFECT']
    df.loc[df.WZ_OCCUR==0,'WZ_TYPE'] = np.NaN
    df.loc[(df.WZ_OCCUR==1) & (df.WZ_TYPE==1),'WZ_TYPE'] = np.NaN
    df.loc[df.WZ_OCCUR==0,'WZ_WORKER'] = np.NaN
    df.loc[df.X==0,'X'] = np.NaN
    df.loc[df.Y==0,'Y'] = np.NaN
    df.loc[df.COUNTY==0,'COUNTY'] = np.NaN
    df.loc[~df.FUNC_CLASS.isin([10,20,30,40,50,60,70,80,90]),'FUNC_CLASS'] = np.NaN
    df.loc[df.TWAY_DESC==0,'TWAY_DESC'] = np.NaN
    df.loc[(df.YEAR>=2013) & (df.TWAY_DESC.isin([5,6])),'TWAY_DESC'] = np.NaN
    df.loc[df.WEATHER==99,'WEATHER'] = 9
    df.loc[df.COL_TYPE.isin([0,99]),'COL_TYPE'] = np.NaN
    df.loc[df.CAUSE_1.isin([0]),'CAUSE_1'] = 99
    df.loc[df.CAUSE_2.isin([0]),'CAUSE_2'] = 99
    df.loc[df.AGENCY==0,'AGENCY'] = 9

    print('[{}] Calculate LAT/LONs'.format(strftime("%Y-%m-%d %H:%M:%S")))
    idx = df[(~pd.isnull(df.X)) & (~pd.isnull(df.Y))].index
    df.loc[idx,'Point'] = [arcpy.PointGeometry(arcpy.Point(x,y),common.NAD1983IL).projectAs(common.WGS1984) for x,y in zip(list(df.loc[idx,'X']),list(df.loc[idx,'Y']))]
    def GetLON(p):
        try:
            return(p.X)
        except:
            pass
    def GetLAT(p):
        try:
            return(p.Y)
        except:
            pass
    df.loc[idx,'LAT'] = [GetLAT(p) for p in df.Point.loc[idx]]
    df.loc[idx,'LON'] = [GetLON(p) for p in df.Point.loc[idx]]
    
    print('[{}] Calculate Sun Angle'.format(strftime("%Y-%m-%d %H:%M:%S")))
    df['SUN_ANG'] = [SunAngle(lt,ln,dt) for lt,ln,dt in zip(list(df.LAT),list(df.LON),list(df.DATE))]

    print('[{}] Export {} to {}'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape,Out_CSV))
    df = df[[
        'DATE','NO_VEH','RT_NBR',
        'COUNTY','CITY','CITY_CLASS','TOWNSHIP','AGENCY',
        'INT_REL','FUNC_CLASS','TWAY_CLASS','TWAY_DESC','TCONT_DEV','TCONT_CON',
        'SURF_CON','ALIGN','DEFECT','LIGHT','SUN_ANG','WEATHER',
        'COL_TYPE','CAUSE_1','CAUSE_2','HIT_RUN',
        'WZ_OCCUR','WZ_TYPE','WZ_WORKER',
        'X','Y','LON','LAT'
        ]]
    df.to_csv(Out_CSV)
def Veh_MDBExtToCSV(In_CSV,Out_CSV):
    # Read Data
    print('[{}] Read Data: {}'.format(strftime("%Y-%m-%d %H:%M:%S"),In_CSV))
    df = pd.read_csv(In_CSV,low_memory=False, encoding='latin-1')
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape))
    
    # Index Data
    print('[{}] Data Clean ups'.format(strftime("%Y-%m-%d %H:%M:%S")))
    df.Case_number = [ConvToInt(v) for v in df.Case_number]
    df.Case_number = [FixIndex(v) for v in df.Case_number]
    l1 = df.shape[0]
    df = df[~pd.isnull(df.Case_number)]
    l2 = df.shape[0]
    if l2!= l1:
        print(' - Non Int Case number: {}'.format(l1-l2))
    t = [(int(c),int(u)) for c,u in zip(df.Case_number, df.UnitNo)]
    mi = pd.MultiIndex.from_tuples(t,names=['CID','UnitID'])
    df.index = mi
    #Sort
    df = df.sort_index()
    

    # Fillna
    df.loc[[str(v) in ['(UNK)','0'] for v in df.NoOccupants],'NoOccupants'] = None
    for f in ['VEHT','VEHU','VEHD','MANV']:
        df.loc[(pd.isnull(df[f])) | (df[f]==0),f] = 99
    for f in ['DIRP']:
        df.loc[(pd.isnull(df[f])) | (df[f]==0),f] = 9
    for f in ['TOW','FIRE_IND','HAZMAT','CV_IND','ExceedingSpeedLimit']:
        df[f] = df[f].fillna('N')
    df.loc[[str(v)=='(UNK)' for v in df.Vehicle_Model_Year],'Vehicle_Model_Year'] = None
    df.Vehicle_Model_Year = df.Vehicle_Model_Year.fillna(0)
    df.Vehicle_Model_Year = df.Vehicle_Model_Year.astype(int)
    df.loc[(df.Vehicle_Model_Year<1900) | (df.Vehicle_Model_Year>2020),'Vehicle_Model_Year'] = None
    
    df.loc[df.VIN11.isin(['(UNK)','(N/A)','UNKNOWN']),'VIN11'] = None
    df.loc[df.Vehicle_Make.isin(['UNKNOWN']),'Vehicle_Make'] = None
    df.loc[df.Vehicle_Model.isin(['OTHER/UNKNOWN','(UNK)']),'Vehicle_Model'] = None
    
    # Convert Data
    for f in ['TOW','FIRE_IND','HAZMAT','CV_IND','ExceedingSpeedLimit']:
        df[f] = [{'Y':1,'N':0}[v] for v in df[f]]
    
    # Format Columns
    for f in ['VEHT','VEHU','VEHD','MANV','MostHarmfulEvent', 'EVNT1', 'EVNT2', 'EVNT3',
              'DIRP','LOC1', 'LOC2', 'LOC3','NoOccupants','LocationOfMostHarmful',
              'MostHarmfulEventNo','TOW','FIRE_IND','HAZMAT','CV_IND','ExceedingSpeedLimit']:
        df[f] = [ConvToInt(v) for v in df[f]]
    
    # Select Columns
    VL = ['NoOccupants','VEHT', 'VEHU', 'MANV', 'DIRP', 'ExceedingSpeedLimit', 
          'EVNT1', 'EVNT2', 'EVNT3', 'LOC1', 'LOC2', 'LOC3', 'MostHarmfulEvent', 'LocationOfMostHarmful', 'MostHarmfulEventNo',
         'FirstContact', 'VEHD',  
         'TOW', 'FIRE_IND', 'HAZMAT', 'CV_IND','Vehicle_Model_Year', 'Vehicle_Make', 'Vehicle_Model','VIN11'
         ]
    df = df[VL]
    VL_N = ['NO_OCC','VEHT', 'VEHU', 'MANV', 'DIRP', 'EXC_SPL', 
          'EVNT1', 'EVNT2', 'EVNT3', 'LOC1', 'LOC2', 'LOC3', 'MHE', 'MHE_LOC', 'MHE_NO',
         'FRST_CONT', 'VEHD',  
         'TOW', 'FIRE_IND', 'HAZMAT', 'CV_IND','V_YEAR', 'V_MAKE', 'V_MODEL','VIN11'
         ]
    df.columns = VL_N
    
    df = df[[
        'NO_OCC','VEHT', 'VEHU', 'MANV', 'DIRP', 'EXC_SPL', 
        'EVNT1', 'EVNT2', 'EVNT3', 'LOC1', 'LOC2', 'LOC3', 'MHE', 'MHE_LOC', 'MHE_NO',
        'FRST_CONT', 'VEHD', 'TOW', 
        'FIRE_IND', 'HAZMAT', 'CV_IND','V_YEAR', 'V_MAKE', 'V_MODEL','VIN11'        
        ]]
    print('[{}] Export {} to {}'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape,Out_CSV))
    df.to_csv(Out_CSV)
def Occ_MDBExtToCSV(In_CSV,Out_CSV):
    # Read Data
    print('[{}] Read Data: {}'.format(strftime("%Y-%m-%d %H:%M:%S"),In_CSV))
    df = pd.read_csv(In_CSV,low_memory=False, encoding='latin-1')
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape))
    
    # Index Data
    print('[{}] Data Clean ups'.format(strftime("%Y-%m-%d %H:%M:%S")))
    df.CaseNum = [ConvToInt(v) for v in df.CaseNum]
    df.CaseNum = [FixIndex(v) for v in df.CaseNum]
    l1 = df.shape[0]
    df = df[(~pd.isnull(df.CaseNum)) | (~pd.isnull(df.UnitNo))]
    l2 = df.shape[0]
    if l2!= l1:
        print(' - Non Int Case number: {}'.format(l1-l2))
    t = [(int(c),int(u)) for c,u in zip(df.CaseNum, df.UnitNo)]
    mi = pd.MultiIndex.from_tuples(t,names=['CID','UnitID'])
    df.index = mi
    #Sort
    df = df.sort_values(['CaseNum','UnitNo','Person_Type','Age'])
    idf = pd.DataFrame(df.index.value_counts().sort_index())
    idf['List'] = [list(range(1,v+1)) for v in idf[0]]
    L = []
    for l in idf.List:
        L.extend(l)
    df['PersonID'] = L
    t = [(int(c),int(u),int(i)) for c,u,i in zip(df.CaseNum, df.UnitNo,df.PersonID)]
    mi = pd.MultiIndex.from_tuples(t,names=['CID','UnitID','OccID'])
    df.index = mi
    #Sort
    df = df.sort_index()

    for f in ['Age','Driver_Vision','Driver_Action','Seating_Position']:
        df[f] = df[f].fillna(99)
    for f in ['Driver_Condition','Safety_Equipment','Airbag_Deployment','Ejected']:
        df[f] = df[f].fillna(9)
    for f in ['Driver_Condition']:
        df.loc[df[f]==0,f] = 9
    for f in ['BAC']:
        df[f] = df[f].fillna(96)
    for f in ['Injury_Severity']:
        df[f] = df[f].fillna(0)
    for f in ['CellPhoneUse']:
        df[f] = df[f].fillna('N')
    for f in ['EMS125','Hospital']:
        df.loc[df[f]==0,f] = None
    
    
    for f in ['Person_Type','Age','Driver_Condition','BAC', 'Ped_Action', 'Ped_Location', 'Ped_Bike_Visibility',
                'Driver_Vision', 'Driver_Action', 'Seating_Position','Injury_Severity', 'Safety_Equipment','Driver_Condition',
                'Airbag_Deployment', 'Ejected']:
        df[f] = df[f].astype(int,errors='ignore')
        #df.loc[~pd.isnull(df[f]),f] = df.loc[~pd.isnull(df[f]),f].astype(int)
    
    for f in ['CellPhoneUse']:
        df[f] = [{'Y':1,'N':0,'No':0,'(N/A)':0,'Yes':1}[v] for v in df[f]]
    
    df.DOB = [DOBtoDatetime(d) for d in df.DOB]
    OL = ['Person_Type','DOB','Age','Sex', 'Seating_Position','Injury_Severity',
          'Safety_Equipment','Airbag_Deployment','Ejected','Driver_Action',
          'Driver_Condition','BAC',  'Driver_Vision', 
          'Ped_Action', 'Ped_Location', 'Ped_Bike_Visibility','CellPhoneUse',
          'DriverLicenseState', 'EMS125', 'Hospital']
    df = df[OL]
    OL_N = ['PER_TYPE','DOB','AGE','SEX', 'SEAT_POS','INJ_SEV',
          'SAF_EQI','AIRBAG','EJECT','DR_ACTION',
          'DR_CON','BAC',  'DR_VISION', 
          'PD_ACTION', 'PD_LOC', 'PD_VIS','CELL_USE',
          'DR_LIC_ST', 'EMS125', 'HOSPITAL']
    df.columns = OL_N
    
    df = df[[
        'PER_TYPE','DOB','AGE','SEX','INJ_SEV', 'SEAT_POS',
        'SAF_EQI','AIRBAG','EJECT',
        'DR_LIC_ST', 'DR_ACTION', 'DR_VISION', 'DR_CON','BAC','CELL_USE', 
        'PD_ACTION', 'PD_LOC', 'PD_VIS',
        'EMS125', 'HOSPITAL'
        ]]
    print('[{}] Export {} to {}'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape,Out_CSV))
    df.to_csv(Out_CSV)
def CON_MDBExtToCSV(WDir,HSMPY_PATH,Crash_In_CSV,Veh_In_CSV,Occ_In_CSV,Crash_Out_CSV,Veh_Out_CSV,Occ_Out_CSV,Year):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'Crash_' + str(Year) + '_MDBExtToCSV.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Year = "{}"
print("MDB Extract to CSV: " + Year)
import os, sys
import pandas as pd
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Crash_In_CSV = r'{}'
Veh_In_CSV = r'{}'
Occ_In_CSV = r'{}'
Crash_Out_CSV = r'{}'
Veh_Out_CSV = r'{}'
Occ_Out_CSV = r'{}'
sys.path.append(HSMPY_PATH) 
import hsmpy3
import numpy as np
import arcpy
hsmpy3.il.Crash_MDBExtToCSV(Crash_In_CSV,Crash_Out_CSV)
hsmpy3.il.Veh_MDBExtToCSV(Veh_In_CSV,Veh_Out_CSV)
hsmpy3.il.Occ_MDBExtToCSV(Occ_In_CSV,Occ_Out_CSV)
""".format(Year,HSMPY_PATH,Crash_In_CSV,Veh_In_CSV,Occ_In_CSV,Crash_Out_CSV,Veh_Out_CSV,Occ_Out_CSV)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def CON_AddEADefinition(WDir,HSMPY_PATH,Crash_In_CSV,Veh_In_CSV,Occ_In_CSV,Crash_Out_CSV,Veh_Out_CSV,Occ_Out_CSV,Year):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'Crash_' + str(Year) + '_AddEADefinition.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Year = "{}"
print("Add EA Definition: " + Year)
import os, sys
import pandas as pd
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Crash_In_CSV = r'{}'
Veh_In_CSV = r'{}'
Occ_In_CSV = r'{}'
Crash_Out_CSV = r'{}'
Veh_Out_CSV = r'{}'
Occ_Out_CSV = r'{}'
sys.path.append(HSMPY_PATH) 
import hsmpy3
import numpy as np
import arcpy
hsmpy3.il.AddEADefinition(Crash_In_CSV,Veh_In_CSV,Occ_In_CSV,Crash_Out_CSV,Veh_Out_CSV,Occ_Out_CSV)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Year,HSMPY_PATH,Crash_In_CSV,Veh_In_CSV,Occ_In_CSV,Crash_Out_CSV,Veh_Out_CSV,Occ_Out_CSV)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def AddEADefinition(Crash_In_CSV,Veh_In_CSV,Occ_In_CSV,Crash_Out_CSV,Veh_Out_CSV,Occ_Out_CSV):
    # Add EA definitions
    import warnings
    warnings.filterwarnings('ignore')
    print('[{}] Read Data'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Crash_DF = pd.read_csv(Crash_In_CSV,index_col =0)
    cid_C = set(list(Crash_DF.index))
    print('[{}]  - Crash File {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Crash_DF.shape))

    Veh_DF = pd.read_csv(Veh_In_CSV,index_col =[0,1])
    cid_V = set(list(Veh_DF.index.droplevel(1)))
    V_C = cid_V-cid_C
    if len(V_C)>0:
        Veh_DF = Veh_DF[~Veh_DF.index.isin(Veh_DF.loc[list(V_C)].index)]
    print('[{}]  - Vehicle File {} - {} Orphan'.format(strftime("%Y-%m-%d %H:%M:%S"),Veh_DF.shape,len(cid_V-cid_C)))

    Occ_DF = pd.read_csv(Occ_In_CSV,index_col =[0,1,2], encoding='latin-1')
    cid_P = set(list(Occ_DF.index.droplevel([1,2])))
    P_C = cid_P-cid_C
    if len(P_C)>0:
        Occ_DF = Occ_DF[~Occ_DF.index.isin(Occ_DF.loc[list(P_C)].index)]
    Occ_DF['DOB'] = pd.to_datetime(Occ_DF.DOB)
    print('[{}]  - Person File {} - {} Orphan'.format(strftime("%Y-%m-%d %H:%M:%S"),Occ_DF.shape,len(cid_P-cid_C)))

    Crash_DF['DATE'] = pd.to_datetime(Crash_DF.DATE)
    Crash_DF['YEAR'] = [d.year for d in Crash_DF.DATE]
    CL = list(set(Crash_DF.YEAR))
    if len(CL)==1:
        Occ_DF['YEAR'] = CL[0]
    else:
        Occ_DF['YEAR'] = list(Crash_DF.YEAR.loc[Occ_DF.index.droplevel([1,2])])

    print('[{}] Add KABCO'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Occ_DF['index_backup'] = Occ_DF.index
    Occ_DF.index = Occ_DF.index.droplevel([1,2])
    def KABCO_Max(L):
        return({4:'K',3:'A',2:'B',1:'C',0:'O'}[max(L)])
    Occ_DF['CID'] = list(Occ_DF.index)
    Crash_DF['K'] = 0
    Crash_DF['A'] = 0
    Crash_DF['B'] = 0
    Crash_DF['C'] = 0
    Crash_DF['O'] = 0
    Crash_DF['KABCO'] = 'O'
    K = Occ_DF[Occ_DF.INJ_SEV==4].groupby('CID').size()
    A = Occ_DF[Occ_DF.INJ_SEV==3].groupby('CID').size()
    B = Occ_DF[Occ_DF.INJ_SEV==2].groupby('CID').size()
    C = Occ_DF[Occ_DF.INJ_SEV==1].groupby('CID').size()
    O = Occ_DF[Occ_DF.INJ_SEV==0].groupby('CID').size()
    KABCO = Occ_DF.groupby('CID')['INJ_SEV'].aggregate(KABCO_Max)
    Crash_DF.loc[K.index,'K'] = K
    Crash_DF.loc[A.index,'A'] = A
    Crash_DF.loc[B.index,'B'] = B
    Crash_DF.loc[C.index,'C'] = C
    Crash_DF.loc[O.index,'O'] = O
    Crash_DF.loc[KABCO.index,'KABCO'] = KABCO
    Occ_DF.index = pd.MultiIndex.from_tuples(Occ_DF.index_backup,names=['CID','UnitID','OccID'])
    print('[{}]  - K:{}, A:{}, B:{}, C:{}, O:{}'.format(strftime("%Y-%m-%d %H:%M:%S"),sum(K),sum(A),sum(B),sum(C),sum(O)))
    
    Crash_DF["DAY_NIGHT"] = [DayNight(d,s) for d,s in zip(Crash_DF.DATE,Crash_DF.SUN_ANG)]
    
    print('[{}] Find EA Inices'.format(strftime("%Y-%m-%d %H:%M:%S")))
    EADict = {}

    # Crash Level Index
    RD_idx = list(Crash_DF[Crash_DF.COL_TYPE.isin([5,6,13,14])].index)
    EADict.update({'EA_RD':RD_idx})

    IM_idx = list(set([i[0] for i in Occ_DF[(Occ_DF.PER_TYPE==1) & (Occ_DF.DR_CON.isin([2,3,6,7]))].index]))
    EADict.update({'EA_IM':IM_idx})

    IN_idx = list(Crash_DF[Crash_DF.INT_REL==1].index)
    EADict.update({'EA_IN':IN_idx})

    SA_idx = list(Crash_DF[Crash_DF.CAUSE_1.isin([1,27,28,50])].index)
    EADict.update({'EA_SA':SA_idx})

    OD_idx = list(set([i[0] for i in Occ_DF[(Occ_DF.PER_TYPE==1) & (Occ_DF.AGE>=65) & (Occ_DF.AGE!=99)].index]))
    EADict.update({'EA_OD':OD_idx})

    YD_idx = list(set([i[0] for i in Occ_DF[(Occ_DF.PER_TYPE==1) & (Occ_DF.AGE>=16) & (Occ_DF.AGE<=20)].index]))
    EADict.update({'EA_YD':YD_idx})

    HV_idx = list(set([i[0] for i in Veh_DF[Veh_DF.VEHT.isin([4,5,6,7,8])].index]))
    EADict.update({'EA_HV':HV_idx})

    if 'WZ_OCCUR' in Crash_DF.columns:
        WZ_idx = list(Crash_DF[(Crash_DF.WZ_OCCUR.isin([1]))].index)
    else:
        WZ_idx = list(Crash_DF[(Crash_DF.DEFECT.isin([2,3,4,5]))].index)
    EADict.update({'EA_WZ':WZ_idx})
    
    TN_idx = list(Crash_DF[Crash_DF.COL_TYPE.isin([3])].index)
    EADict.update({'EA_TN':TN_idx})

    odf1 = Occ_DF[Occ_DF.YEAR.isin(range(2010,2013))]
    odf2 = Occ_DF[Occ_DF.YEAR.isin(range(2013,2017))]
    L1 = list(set([i[0] for i in odf1[(odf1.PER_TYPE==1) & (odf1.DR_CON.isin([8,5]))].index]))
    L1.extend(list(set([i[0] for i in odf2[(odf2.PER_TYPE==1) & (odf2.DR_CON.isin([8,4]))].index])))

    df1 = Crash_DF[Crash_DF.YEAR.isin(range(2010,2013))]
    df2 = Crash_DF[Crash_DF.YEAR.isin(range(2013,2017))]
    L1.extend(list(df1[df1.CAUSE_1.isin([40,41,42,43])].index))
    L1.extend(list(df2[df2.CAUSE_1.isin([40,41,44,45])].index))
    DF_idx = list(set(L1))
    EADict.update({'EA_DF':DF_idx})
    
    Veh_DF['index_backup'] = Veh_DF.index
    Occ_DF['index_backup'] = Occ_DF.index
    Veh_DF.index = Veh_DF.index.droplevel(1)
    Occ_DF.index = Occ_DF.index.droplevel([1,2])
    for f in ['EA_RD','EA_IM','EA_IN','EA_DF','EA_TN','EA_WZ','EA_SA','EA_OD','EA_YD','EA_HV']:
        Crash_DF[f] = 0
        Crash_DF.loc[EADict[f],f] = 1
        Veh_DF[f] = 0
        Veh_DF.iloc[[i for i,l in enumerate(Veh_DF.index.isin(EADict[f])) if l==True],list(Veh_DF.columns).index(f)] = 1
        Occ_DF[f] = 0
        Occ_DF.iloc[[i for i,l in enumerate(Occ_DF.index.isin(EADict[f])) if l==True],list(Occ_DF.columns).index(f)] = 1
        print('[{}]  - {}: {}'.format(strftime("%Y-%m-%d %H:%M:%S"),f,len(EADict[f])))
    Veh_DF.index = pd.MultiIndex.from_tuples(Veh_DF.index_backup,names=['CID','UnitID'])
    Occ_DF.index = pd.MultiIndex.from_tuples(Occ_DF.index_backup,names=['CID','UnitID','OccID'])

    # Vehicle Lvele Index
    Occ_DF.index = Occ_DF.index.droplevel(2)
    MC_idx = list(Veh_DF[Veh_DF.VEHT.isin([10,11])].index)
    EADict.update({'EA_MC':MC_idx})
    for f in ['EA_MC']:
        Crash_DF[f] = 0
        Crash_DF.loc[pd.MultiIndex.from_tuples(EADict[f]).droplevel(1),f] = 1
        Veh_DF[f] = 0
        Veh_DF.loc[EADict[f],f] = 1
        Occ_DF[f] = 0
        Occ_DF.iloc[[i for i,l in enumerate(Occ_DF.index.isin(EADict[f])) if l==True],list(Occ_DF.columns).index(f)] = 1
        print('[{}]  - {}: {}'.format(strftime("%Y-%m-%d %H:%M:%S"),f,len(EADict[f])))
    Occ_DF.index = pd.MultiIndex.from_tuples(Occ_DF.index_backup,names=['CID','UnitID','OccID'])

    # Person Level Index
    L1 = list(Veh_DF[Veh_DF.VEHT.isin([1,2,3,6,7,8,14,15])].index)
    df = Occ_DF.iloc[[i for i,l in enumerate(Occ_DF.index.droplevel(2).isin(L1)) if l==True]]
    UO_idx = list(df[(df.PER_TYPE.isin([1,7])) & (df.SAF_EQI.isin([1,3,7,8]))].index)
    EADict.update({'EA_UO':UO_idx})

    PD_idx = list(Occ_DF[Occ_DF.PER_TYPE==2].index)
    EADict.update({'EA_PD':PD_idx})

    PC_idx = list(Occ_DF[Occ_DF.PER_TYPE==3].index)
    EADict.update({'EA_PC':PC_idx})
    for f in ['EA_UO','EA_PD','EA_PC']:
        Crash_DF[f] = 0
        Crash_DF.loc[pd.MultiIndex.from_tuples(EADict[f]).droplevel([1,2]),f] = 1
        Veh_DF[f] = 0
        Veh_DF.loc[Veh_DF.loc[Veh_DF.index.isin(pd.MultiIndex.from_tuples(EADict[f]).droplevel(2))].index,f] = 1
        Occ_DF[f] = 0
        Occ_DF.loc[EADict[f],f] = 1
        print('[{}]  - {}: {}'.format(strftime("%Y-%m-%d %H:%M:%S"),f,len(EADict[f])))

    Occ_DF = Occ_DF.drop(['index_backup','YEAR','CID'],axis=1)
    Veh_DF = Veh_DF.drop(['index_backup'],axis=1)
    Crash_DF = Crash_DF.drop('YEAR',axis=1)

    print('[{}] Export CSVs'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Crash_DF.to_csv(Crash_Out_CSV)
    Veh_DF.to_csv(Veh_Out_CSV)
    Occ_DF.to_csv(Occ_Out_CSV)

def CalAge(cdate,dob):
    try:
        diff = cdate-dob
        return(int(diff.days/364.0))
    except:
        pass

# Crash Assignment
def ExtCrash_RType(rt): #First digit represents the route type
    try:
        return(int(str(rt)[0]))
    except:
        pass
def ExtCrash_RNumber(rt): #Last three digits represent the route number
    try:
        rt = int(rt)
        return(int(str(rt)[1:]))
    except:
        pass
def FindBuffer(sw,mw,osw1,osw2,mt,direction): #Calculates the left and right buffer
    try:
        sw = float(sw)
    except:
        sw = 24
    try:
        mw = float(mw)
    except:
        mw = 0
    try:
        osw1 = float(osw1)
    except:
        osw1 = 6
    try:
        osw2 = float(osw2)
    except:
        osw2 = 0
    try:
        mt = int(mt)
    except:
        mt = 0
    osw = osw1+osw2
    if mt==0:
        return((sw+mw)/2.0 + osw)
    else:
        if direction == 'R':
            return(sw/4.0 + osw)
        if direction == 'L':
            return(3*sw/4.0 + mw + osw)
    return(18)
def ExtractMARKET_RT(S): 
    if not pd.isnull(S):
        if len(S)>2:
            s1 = S[0]
            try:
                s2 = int(S[1:])
                s3= ''
            except:
                s2 = int(S[1:-1])
                s3 = S[-1]
            s1 = s1+s3
            CDict = {'I':9,'IB':2,'U':1,'UB':3,'S':5}
            return([s1,s2])
        else:
            return([np.NaN,np.NaN])
    else:
        return([np.NaN,np.NaN])
def MatchRoute(c_rt,c_rn,i_rt,i_rn): # Marked routes
    ConvDict = {1:['U','UB'],2:['IB','I'],3:['UB','U'],4:['UB','U'],5:['S'],6:['S'],7:['I','IB'],8:[],9:['I','IB']}
    if True in [pd.isnull(i) for i in [c_rt,c_rn,i_rt,i_rn]]:
        return(0)  # missing info
    if i_rt in ConvDict[c_rt] and i_rn==c_rn:
        return(3)  # perfect match
    if i_rn==c_rn:
        return(2) # only route number matches
    if i_rt in ConvDict[c_rt]:
        return(1) # only route type matches
    return(0) # nothing matches
def MatchFC(c_fc,r_fc):
    if True in [pd.isnull(i) for i in [c_fc,r_fc]]:
        return(0)
    try:
        c_fc = int(c_fc)
        r_fc = int(r_fc)
    except:
        return(0)
    # 1 Interstate
    if c_fc==10:
        return({1:3,2:2,3:1,4:1,5:0,6:0,7:0}[r_fc])
    # 2 Freeway
    if c_fc==20:
        return({1:2,2:3,3:1,4:1,5:0,6:0,7:0}[r_fc])    
    # 3 Other Principal Arterial
    if c_fc==30:
        return({1:1,2:1,3:3,4:2,5:0,6:0,7:0}[r_fc])    
    # 4 Minor Arterial
    if c_fc==40:
        return({1:0,2:0,3:2,4:3,5:1,6:1,7:0}[r_fc])    
    if c_fc==70:
        return({1:0,2:0,3:2,4:3,5:1,6:1,7:0}[r_fc])    
    # 5 Major Collector
    if c_fc==50:
        return({1:0,2:0,3:1,4:1,5:3,6:2,7:1}[r_fc])    
    # 6 Minor Collector
    if c_fc==80:
        return({1:0,2:0,3:0,4:1,5:2,6:3,7:1}[r_fc])    
    # 7 Local Road
    if c_fc==60:
        return({1:0,2:0,3:0,4:1,5:1,6:2,7:3}[r_fc])    
    if c_fc==90:
        return({1:0,2:0,3:0,4:1,5:1,6:2,7:3}[r_fc])    
    return(0)
def MatchDist(offset,direction,r_bl,r_br):
    try:
        r_bl = int(r_bl)
    except:
        r_bl = 18
    try:
        r_br = int(r_br)
    except:
        r_br = 18
    if direction:
        if offset<r_br:
            return(3)
        if offset<1.5*r_br:
            return(2)
        if offset<2*r_br:
            return(1)
        return(0)
    if not direction:
        if offset<r_bl:
            return(3)
        if offset<1.5*r_bl:
            return(2)
        if offset<2*r_bl:
            return(1)
        return(0)
    return(0)
def CrashAssignment(GDB,CrashCSV,RouteFC,AttTable,CrashCSV_Out,Debug_CSV=''):
    warnings.filterwarnings('ignore')

    #Fields = ['FC','MED_TYP', 'MED_WTH', 'O_SHD1_WTH', 'O_SHD2_WTH', 'SURF_WTH','MARKED_RT']
    Fields = ['FUNC_CLASS','MED_TYP', 'MED_WTH', 'O_SHD1_WTH', 'O_SHD2_WTH', 'SURF_WTH','MARKED_RT']
    MaxDist = "500 Feet"
    print('[{}] Read Crash Data'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Crash_DF = pd.read_csv(CrashCSV,index_col =0)
    Crash_DF.index.name = 'CID'
    print('[{}]  - Crash {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Crash_DF.shape))

    print('[{}] Geocode Crash Data:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Crash_Out = GDB + '\\Crash_GEO' + strftime("_%Y%m%d_%H%M%S")
    arcpy.management.Delete(Crash_Out)
    arcpy.management.CreateFeatureclass(out_name = os.path.basename(Crash_Out),
                                    out_path = os.path.dirname(Crash_Out),
                                    spatial_reference=common.NAD1983IL,
                                    geometry_type='POINT',
                                    has_m='ENABLED',
                                    has_z='ENABLED')
    arcpy.AddField_management(Crash_Out,'CID','TEXT')
    ic = arcpy.InsertCursor(Crash_Out)
    for i,r in Crash_DF.iterrows():
        if not math.isnan(r.X) and not math.isnan(r.Y):
            Pt =  arcpy.PointGeometry(arcpy.Point(r.X,r.Y),common.NAD1983IL)
            row = ic.newRow()
            row.setValue('CID',str(i))
            row.shape = Pt
            ic.insertRow(row)
    del ic
    del row
    print('[{}]  - Crash {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.GetCount_management(Crash_Out))))

    print('[{}] SpatialJoin'.format(strftime("%Y-%m-%d %H:%M:%S")))
    SPJFC = GDB  + '\\Crash_SPJ' + strftime("_%Y%m%d_%H%M%S")
    arcpy.management.Delete(SPJFC)
    arcpy.SpatialJoin_analysis(
        target_features = Crash_Out, 
        join_features = RouteFC, 
        out_feature_class = SPJFC, 
        join_operation="JOIN_ONE_TO_MANY", 
        join_type="KEEP_COMMON", 
        match_option="INTERSECT", 
        search_radius=MaxDist, 
        distance_field_name=""
    )
    print('[{}] Read SpatialJoin'.format(strftime("%Y-%m-%d %H:%M:%S")))
    SPJ_DF = common.FCtoDF(SPJFC,selectedFields=['CID','INVENTORY'])
    SPJ_DF.index = SPJ_DF.CID
    SPJ_DF = SPJ_DF[['INVENTORY']]
    SPJ_DF = SPJ_DF[~pd.isnull(SPJ_DF.INVENTORY)]
    L = list(set(SPJ_DF.index))

    print('[{}] Dissolve'.format(strftime("%Y-%m-%d %H:%M:%S")))
    IRIS_Diss = GDB + '\\Diss' + strftime("_%Y%m%d_%H%M%S")
    
    #arcpy.management.Delete(IRIS_Diss)
#    arcpy.DissolveRouteEvents_lr(in_events = AttTable, 
#                                 in_event_properties = ' '.join(['INVENTORY','LINE','BEG_STA','END_STA']), 
#                                 dissolve_field = ';'.join(Fields), 
#                                 out_table = IRIS_Diss, 
#                                 out_event_properties = ' '.join(['INVENTORY','LINE','BEG_STA','END_STA']), 
#                                 dissolve_type="DISSOLVE", 
#                                 build_index="INDEX")    
#    arcpy.DissolveRouteEvents_lr(in_events = AttTable, 
#                                 in_event_properties = ' '.join(['RID','LINE','BMP','EMP']), 
#                                 dissolve_field = ';'.join(Fields), 
#                                 out_table = IRIS_Diss, 
#                                 out_event_properties = ' '.join(['RID','LINE','BMP','EMP']), 
#                                 dissolve_type="DISSOLVE", 
#                                 build_index="INDEX")    
    IRIS_Diss = AttTable
    #Diss_DF = common.FCtoDF(IRIS_Diss,['FUNC_CLASS','MED_TYP', 'MED_WTH', 'O_SHD1_WTH', 'O_SHD2_WTH', 'SURF_WTH','MARKED_RT','RID','BMP','EMP']) 
    Diss_DF = Diss_DF.rename(columns={'FUNC_CLASS':'FC','RID':'INVENTORY','BMP':'BEG_STA','EMP':'END_STA'})
    Diss_DF.index = pd.MultiIndex.from_tuples([(inv,bmp,emp) for inv,bmp,emp in zip(Diss_DF.INVENTORY,Diss_DF.BEG_STA,Diss_DF.END_STA)],names=['RID','BMP','EMP'])
    Diss_DF = Diss_DF.sort_index()
    #Diss_DF['Tot_Width'] = Diss_DF.SURF_WTH + Diss_DF.MED_WTH + (Diss_DF.O_SHD1_WTH + Diss_DF.O_SHD2_WTH) * 2 
    Diss_DF['Width_Rt'] = [FindBuffer(sw,mw,osw1,osw2,mt,'R') for sw,mw,osw1,osw2,mt in zip(Diss_DF.SURF_WTH, Diss_DF.MED_WTH, Diss_DF.O_SHD1_WTH, Diss_DF.O_SHD2_WTH, Diss_DF.MED_TYP)] 
    Diss_DF['Width_Lt'] = [FindBuffer(sw,mw,osw1,osw2,mt,'L') for sw,mw,osw1,osw2,mt in zip(Diss_DF.SURF_WTH, Diss_DF.MED_WTH, Diss_DF.O_SHD1_WTH, Diss_DF.O_SHD2_WTH, Diss_DF.MED_TYP)]     
    
    print('[{}] Route Data Frame'.format(strftime("%Y-%m-%d %H:%M:%S")))
    R_DF = common.FCtoDF(RouteFC,readGeometry=True)
    R_DF.index = R_DF.INVENTORY
    R_DF = R_DF.sort_index()
    R_DF = R_DF[['Shape']]

    print('[{}] Crash Data Frame'.format(strftime("%Y-%m-%d %H:%M:%S")))
    CDF = common.FCtoDF(Crash_Out,readGeometry=True)
    CDF.index = CDF.CID
    CDF = CDF.sort_index()
    CDF = CDF[['Shape']]
    C_ATT_DF = Crash_DF
    C_ATT_DF.index = [str(s) for s in C_ATT_DF.index]
    
    print('[{}] Calculate Offsets'.format(strftime("%Y-%m-%d %H:%M:%S")))
    SPJ_DF['Crash_Shape'] = CDF.loc[SPJ_DF.index,'Shape']
    SPJ_DF['Route_Shape'] = list(R_DF.loc[list(SPJ_DF.INVENTORY),'Shape'])
    SPJ_DF['QPAR'] = [l.queryPointAndDistance(p) for l,p in zip(SPJ_DF.Route_Shape,SPJ_DF.Crash_Shape)]
    SPJ_DF['MP'] = [q[0].firstPoint.M for q in SPJ_DF.QPAR]
    SPJ_DF['MinMP'] = list(Diss_DF.groupby('INVENTORY')['BEG_STA'].aggregate(min).loc[SPJ_DF.INVENTORY])
    SPJ_DF['MaxMP'] = list(Diss_DF.groupby('INVENTORY')['END_STA'].aggregate(max).loc[SPJ_DF.INVENTORY])
    SPJ_DF.loc[SPJ_DF.MP<SPJ_DF.MinMP,'MP'] = SPJ_DF[SPJ_DF.MP<SPJ_DF.MinMP]['MinMP']
    SPJ_DF.loc[SPJ_DF.MP>SPJ_DF.MaxMP,'MP'] = SPJ_DF[SPJ_DF.MP>SPJ_DF.MaxMP]['MaxMP']
    SPJ_DF['Offset'] = [q[2] for q in SPJ_DF.QPAR]
    SPJ_DF['Direction'] = [q[3] for q in SPJ_DF.QPAR]
    
    print('[{}] Import Crash Attributes'.format(strftime("%Y-%m-%d %H:%M:%S")))
    SPJ_DF['Crash_RTNBR'] = list(C_ATT_DF.RT_NBR.loc[SPJ_DF.index])
    SPJ_DF['Crash_RTYPE'] = [ExtCrash_RType(rt) for rt in SPJ_DF['Crash_RTNBR']]
    SPJ_DF['Crash_RTNumber'] = [ExtCrash_RNumber(rt) for rt in SPJ_DF['Crash_RTNBR']]
    SPJ_DF['Crash_FC'] = list(C_ATT_DF.FUNC_CLASS.loc[SPJ_DF.index])
    SPJ_DF.index = pd.MultiIndex.from_tuples([(i,inv) for i,inv in zip(SPJ_DF.index,SPJ_DF.INVENTORY)],names=['CID','INVENTORY'])
    SPJ_DF['CID'] = [i[0] for i in SPJ_DF.index]
    SPJ_DF = SPJ_DF.sort_values(['CID','Offset'])
    
    print('[{}] Import Roadway Attributes'.format(strftime("%Y-%m-%d %H:%M:%S")))
    PG = []
    FC = []
    BR = []
    BL = []
    RT = []
    MT = []
    for i,r in SPJ_DF.iterrows():
        inv = r.INVENTORY
        mp = r.MP
        dissdf = Diss_DF.loc[inv]
        try:
            k = dissdf[(dissdf.BEG_STA<=mp) & (dissdf.END_STA>=mp)].iloc[0]
            PG.append(k.PG)
            FC.append(k.FC)
            BR.append(k.Width_Rt)
            BL.append(k.Width_Lt)
            RT.append(k.MARKED_RT)
            MT.append(k.MED_TYP)
        except:
            PG.append(np.NaN)
            FC.append(np.NaN)
            BR.append(np.NaN)
            BL.append(np.NaN)
            RT.append(np.NaN)
            MT.append(np.NaN)
    SPJ_DF['IRIS_FC'] = FC
    SPJ_DF['IRIS_PG'] = PG
    SPJ_DF['IRIS_Buff_R'] = BR
    SPJ_DF['IRIS_Buff_L'] = BL
    SPJ_DF['IRIS_RT'] = RT    
    SPJ_DF['IRIS_MT'] = MT    
    SPJ_DF['IRIS_RTYPE']    = [ExtractMARKET_RT(i)[0] for i in list(SPJ_DF.IRIS_RT)]
    SPJ_DF['IRIS_RTNumber'] = [ExtractMARKET_RT(i)[1] for i in list(SPJ_DF.IRIS_RT)]   
    
    print('[{}] Sort and Match'.format(strftime("%Y-%m-%d %H:%M:%S")))
    SPJ_DF['Match_Rt'] = [MatchRoute(c_rt,c_rn,i_rt,i_rn) for c_rt,c_rn,i_rt,i_rn in zip(SPJ_DF.Crash_RTYPE,SPJ_DF.Crash_RTNumber,SPJ_DF.IRIS_RTYPE,SPJ_DF.IRIS_RTNumber)]
    SPJ_DF['Match_FC'] = [MatchFC(c_fc,r_fc) for c_fc,r_fc in zip(SPJ_DF.Crash_FC,SPJ_DF.IRIS_FC)]
    SPJ_DF['Match_Dist'] = [MatchDist(offset,direction,r_bl,r_br) for offset,direction,r_bl,r_br in zip(SPJ_DF.Offset,SPJ_DF.Direction,SPJ_DF.IRIS_Buff_L,SPJ_DF.IRIS_Buff_R)]
    SPJ_DF = SPJ_DF.sort_values(['CID','Match_Rt','Match_FC','Match_Dist','Offset'],ascending=[True,False,False,False,True])
    if Debug_CSV!='':
        SPJ_DF.to_csv(Debug_CSV)
    L1 = list(SPJ_DF.CID)
    L2 = ['']
    L2.extend(L1[:-1])
    SPJ_DF.CID1 = L2
    df = SPJ_DF[SPJ_DF.CID!=SPJ_DF.CID1]  
    df.index = df.index.droplevel(1)
    df['Offset'] = [{False:-o,True:o}[d] for o,d in zip(df.Offset,df.Direction)]
    df = df[['INVENTORY','MP','Offset']]
    COrder = ['INVENTORY','MP','OFFSET']
    COrder.extend(list(Crash_DF))
    Crash_DF.loc[df.index,'INVENTORY'] = list(df.INVENTORY)
    Crash_DF.loc[df.index,'MP'] = list(df.MP)
    Crash_DF.loc[df.index,'OFFSET'] = list(df.Offset)
    Crash_DF = Crash_DF[COrder]
    Crash_DF.to_csv(CrashCSV_Out)
    arcpy.management.Delete(Crash_Out)
    arcpy.management.Delete(SPJFC)
    #arcpy.management.Delete(IRIS_Diss)
def CON_CrashAssignment(WDir,HSMPY_PATH,GDB,CrashCSV,RouteFC,AttTable,CrashCSV_Out,Year):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'Crash_' + str(Year) + '_Assignment.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Year = "{}"
print("Crash Assignment: " + Year)
import os, sys
import pandas as pd
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
GDB = r'{}'
CrashCSV = r'{}'
RouteFC = r'{}'
AttTable = r'{}'
CrashCSV_Out = r'{}'
sys.path.append(HSMPY_PATH) 
import hsmpy3
import numpy as np
import arcpy
hsmpy3.il.CrashAssignment(GDB,CrashCSV,RouteFC,AttTable,CrashCSV_Out)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(Year,HSMPY_PATH,GDB,CrashCSV,RouteFC,AttTable,CrashCSV_Out)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def AddDomainsToGDB(GDB,replace=False):
    print('[{}] Add Domains'.format(strftime("%Y-%m-%d %H:%M:%S")))
    ListDomains = [getattr(domains,f) for f in [i for i in dir(domains) if not '__' in i] if len(getattr(domains,f)['codes'])>0]
    GDBDomains = [d.name for d in arcpy.da.ListDomains(GDB)]
    for domain in ListDomains:
        if domain['name'] in GDBDomains:
            if replace:
                try:
                    arcpy.DeleteDomain_management (in_workspace=GDB, domain_name=domain['name'])
                except:
                    print('[{}]  - Failed to Delete {}'.format(strftime("%Y-%m-%d %H:%M:%S"),domain['name']))
                    continue
            else:
                continue
        print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),domain['name']))
        arcpy.CreateDomain_management(in_workspace=GDB,
                                      domain_name=domain['name'],
                                      domain_description=domain['alias'],
                                      field_type=domain['type'], 
                                      domain_type="CODED")
        for code in domain['codes'].keys():
            #print(domain['name'],code)
            arcpy.AddCodedValueToDomain_management(GDB,domain['name'],code,domain['codes'][code])
    print('[{}] Done!'.format(strftime("%Y-%m-%d %H:%M:%S")))
def GeocodeCrashes(Crash_In_CSV,Veh_In_CSV,Occ_In_CSV,GDB,year,translate=False):
    Crash_Out = GDB + '\\Crash_' + str(year)
    Veh_Out = GDB + '\\Vehicle_' + str(year)
    Occ_Out = GDB + '\\Person_' + str(year)
    AddDomainsToGDB(GDB,replace=False)
    GDBDomains = [d.name for d in arcpy.da.ListDomains(GDB)]

    print('[{}] Read Data'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Crash_DF = pd.read_csv(Crash_In_CSV,index_col =0,low_memory=False)
    Crash_DF['DATE'] = pd.to_datetime(Crash_DF.DATE)
    print('[{}]  - Crash {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Crash_DF.shape))
    Veh_DF = pd.read_csv(Veh_In_CSV,index_col =[0,1],low_memory=False)
    print('[{}]  - Veh {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Veh_DF.shape))
    Occ_DF = pd.read_csv(Occ_In_CSV,index_col =[0,1,2], encoding='latin-1',low_memory=False)
    Occ_DF['DOB'] = pd.to_datetime(Occ_DF.DOB)
    print('[{}]  - Occ {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Occ_DF.shape))

    print('[{}] Create Output:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    arcpy.management.Delete(Crash_Out)
    arcpy.management.CreateFeatureclass(out_name = os.path.basename(Crash_Out),
                                    out_path = os.path.dirname(Crash_Out),
                                    spatial_reference=common.NAD1983IL,
                                    geometry_type='POINT',
                                    has_m='DISABLED',
                                    has_z='DISABLED')
    arcpy.AddField_management(Crash_Out,'CID','TEXT')
    Crash_Fields = ['INVENTORY','MP','OFFSET',
        'DATE','NO_VEH',
        'CITY_CLASS','AGENCY',
        'INT_REL','FUNC_CLASS','TWAY_CLASS','TWAY_DESC','TCONT_DEV','TCONT_CON',
        'SURF_CON','ALIGN','DEFECT','LIGHT','SUN_ANG','DAY_NIGHT','WEATHER',
        'COL_TYPE','CAUSE_1','CAUSE_2','HIT_RUN',
        'WZ_OCCUR','WZ_TYPE','WZ_WORKER',
        'K','A','B','C','O','KABCO',
        'EA_RD','EA_IM','EA_IN','EA_DF','EA_TN','EA_WZ','EA_SA','EA_OD','EA_YD','EA_HV','EA_MC','EA_UO','EA_PD','EA_PC'
        ]
    for f in Crash_Fields:
        if getattr(domains,f)['name'] in GDBDomains:
            if translate:
                Crash_DF = common.TranslateDomains(Crash_DF,domains,[f])
                max_len = max([Crash_DF[f].astype(str).apply(len).max(),100])
                arcpy.AddField_management(in_table=Crash_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = 'Text',
                                    field_alias = getattr(domains,f)['alias'],
                                    field_length = max_len
                                    )
            else:
                arcpy.AddField_management(in_table=Crash_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = getattr(domains,f)['type'],
                                    field_alias = getattr(domains,f)['alias'],
                                    field_domain=getattr(domains,f)['name']
                                    )
        else:
            arcpy.AddField_management(in_table=Crash_Out,
                                  field_name=getattr(domains,f)['name'],
                                  field_type = getattr(domains,f)['type'],
                                  field_alias = getattr(domains,f)['alias']
                                 )
    ic = arcpy.InsertCursor(Crash_Out)
    for i,r in Crash_DF.iterrows():
        row = ic.newRow()
        row.setValue('CID',str(i))
        for f in Crash_Fields:
            if not pd.isnull(r[f]):
                row.setValue(f,r[f])
        if not math.isnan(r.X) and not math.isnan(r.Y):
            Pt =  arcpy.PointGeometry(arcpy.Point(r.X,r.Y),common.NAD1983IL)
            row.shape = Pt
        ic.insertRow(row)
    del ic
    del row
    print('[{}]  - Crash {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.GetCount_management(Crash_Out))))

    arcpy.management.Delete(Veh_Out)
    arcpy.management.Delete(Occ_Out)
    arcpy.CreateTable_management (out_path = os.path.dirname(Veh_Out), 
                                  out_name = os.path.basename(Veh_Out))
    Veh_Fields = ['NO_OCC','VEHT', 'VEHU', 'MANV', 'DIRP', 'EXC_SPL', 
        'EVNT1', 'LOC1', 'EVNT2', 'LOC2', 'EVNT3', 'LOC3', 'MHE', 'MHE_LOC', 'MHE_NO',
        'FRST_CONT', 'VEHD', 'TOW', 
        'FIRE_IND', 'HAZMAT', 'CV_IND','V_YEAR', 'V_MAKE', 'V_MODEL',#'VIN11',
        'EA_RD','EA_IM','EA_IN','EA_DF','EA_TN','EA_WZ','EA_SA','EA_OD','EA_YD','EA_HV','EA_MC','EA_UO','EA_PD','EA_PC'
        ]
    arcpy.AddField_management(Veh_Out,'CID','TEXT')
    arcpy.AddField_management(Veh_Out,'CID_UID','TEXT')
    for f in Veh_Fields:
        if getattr(domains,f)['name'] in GDBDomains:
            if translate:
                Veh_DF = common.TranslateDomains(Veh_DF,domains,[f])
                max_len = max([Veh_DF[f].astype(str).apply(len).max(),100])
                arcpy.AddField_management(in_table=Veh_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = 'Text',
                                    field_alias = getattr(domains,f)['alias'],
                                    field_length=max_len
                                    )
            else:
                arcpy.AddField_management(in_table=Veh_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = getattr(domains,f)['type'],
                                    field_alias = getattr(domains,f)['alias'],
                                    field_domain=getattr(domains,f)['name']
                                    )
        else:
            arcpy.AddField_management(in_table=Veh_Out,
                                  field_name=getattr(domains,f)['name'],
                                  field_type = getattr(domains,f)['type'],
                                  field_alias = getattr(domains,f)['alias']
                                 )
    ic = arcpy.InsertCursor(Veh_Out)
    for i,r in Veh_DF.iterrows():
        row = ic.newRow()
        row.setValue('CID',str(i[0]))
        row.setValue('CID_UID','{}_{}'.format(i[0],i[1]))
        for f in Veh_Fields:
            if not pd.isnull(r[f]):
                if getattr(domains,f)['type']=='TEXT':
                    row.setValue(f,str(r[f]))
                else:
                    row.setValue(f,r[f])
        ic.insertRow(row)
    del ic
    del row
    print('[{}]  - Vehicle {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.GetCount_management(Veh_Out))))
    
    
    arcpy.CreateTable_management (out_path = os.path.dirname(Occ_Out), 
                                  out_name = os.path.basename(Occ_Out))
    Occ_Fields = ['PER_TYPE','DOB','AGE','SEX','INJ_SEV', 'SEAT_POS',
        'SAF_EQI','AIRBAG','EJECT',
        'DR_LIC_ST', 'DR_ACTION', 'DR_VISION', 'DR_CON','BAC','CELL_USE', 
        'PD_ACTION', 'PD_LOC', 'PD_VIS',
        'EMS125', 'HOSPITAL',
        'EA_RD','EA_IM','EA_IN','EA_DF','EA_TN','EA_WZ','EA_SA','EA_OD','EA_YD','EA_HV','EA_MC','EA_UO','EA_PD','EA_PC'
        ]
    arcpy.AddField_management(Occ_Out,'CID','TEXT')
    arcpy.AddField_management(Occ_Out,'CID_UID','TEXT')
    arcpy.AddField_management(Occ_Out,'OID','SHORT')
    for f in Occ_Fields:
        if getattr(domains,f)['name'] in GDBDomains:
            if translate:
                Occ_DF = common.TranslateDomains(Occ_DF,domains,[f])
                max_len = max([Occ_DF[f].astype(str).apply(len).max(),100])
                arcpy.AddField_management(in_table=Occ_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = 'Text',
                                    field_alias = getattr(domains,f)['alias'],
                                    field_length = max_len
                                    )
            else:
                arcpy.AddField_management(in_table=Occ_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = getattr(domains,f)['type'],
                                    field_alias = getattr(domains,f)['alias'],
                                    field_domain=getattr(domains,f)['name']
                                    )
        else:
            arcpy.AddField_management(in_table=Occ_Out,
                                  field_name=getattr(domains,f)['name'],
                                  field_type = getattr(domains,f)['type'],
                                  field_alias = getattr(domains,f)['alias']
                                 )
    ic = arcpy.InsertCursor(Occ_Out)
    for i,r in Occ_DF.iterrows():
        row = ic.newRow()
        row.setValue('CID',str(i[0]))
        row.setValue('CID_UID','{}_{}'.format(i[0],i[1]))
        row.setValue('OID',int(i[2]))
        for f in Occ_Fields:
            if not pd.isnull(r[f]):
                if getattr(domains,f)['type']=='TEXT':
                    row.setValue(f,str(r[f]))
                else:
                    row.setValue(f,r[f])
        ic.insertRow(row)
    del ic
    del row
    print('[{}]  - Occupant {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.GetCount_management(Occ_Out))))    

    print('[{}]  Create Relationships'.format(strftime("%Y-%m-%d %H:%M:%S")))    
    arcpy.management.Delete(GDB+'\\Crash_Veh' + str(year))
    arcpy.CreateRelationshipClass_management(
        origin_table = Crash_Out,
        destination_table = Veh_Out,
        out_relationship_class = GDB+'\\Crash_Veh' + str(year),
        relationship_type = "SIMPLE",
        forward_label = "Veh" + str(year),
        backward_label = "Crash" + str(year),
        message_direction = "NONE",
        cardinality = "ONE_TO_MANY",
        attributed = "NONE",
        origin_primary_key = 'CID',
        origin_foreign_key = 'CID')

    arcpy.management.Delete(GDB+'\\Crash_Occ' + str(year))
    arcpy.CreateRelationshipClass_management(
        origin_table = Crash_Out,
        destination_table = Occ_Out,
        out_relationship_class = GDB+'\\Crash_Occ' + str(year),
        relationship_type = "SIMPLE",
        forward_label = "Occ" + str(year),
        backward_label = "Crash" + str(year),
        message_direction = "NONE",
        cardinality = "ONE_TO_MANY",
        attributed = "NONE",
        origin_primary_key = 'CID',
        origin_foreign_key = 'CID')

    arcpy.management.Delete(GDB+'\\Veh_Occ' + str(year))
    arcpy.CreateRelationshipClass_management(
        origin_table = Veh_Out,
        destination_table = Occ_Out,
        out_relationship_class = GDB + '\\Veh_Occ' + str(year),
        relationship_type = "SIMPLE",
        forward_label = "Occ" + str(year),
        backward_label = "Veh" + str(year),
        message_direction = "NONE",
        cardinality = "ONE_TO_MANY",
        attributed = "NONE",
        origin_primary_key = 'CID_UID',
        origin_foreign_key = 'CID_UID')
    Route_Out = GDB + '\\Route_{}'.format(year)
    #arcpy.management.Delete(GDB + '\\Route_Crash' + str(year))
    #arcpy.CreateRelationshipClass_management(
    #    origin_table = Route_Out,
    #    destination_table = Crash_Out,
    #    out_relationship_class = GDB + '\\Route_Crash' + str(year),
    #    relationship_type = "SIMPLE",
    #    forward_label = "Crash" + str(year),
    #    backward_label = "Route" + str(year),
    #    message_direction = "NONE",
    #    cardinality = "ONE_TO_MANY",
    #    attributed = "NONE",
    #    origin_primary_key = 'INVENTORY',
    #    origin_foreign_key = 'INVENTORY')

    print('[{}] Done!'.format(strftime("%Y-%m-%d %H:%M:%S")))
def GeocodeCrashes_FCs(Crash_In_CSV,Veh_In_CSV,Occ_In_CSV,GDB,year,translate=False):
    Crash_Out = GDB + '\\Crash_' + str(year)
    Veh_Out = GDB + '\\Vehicle_' + str(year)
    Occ_Out = GDB + '\\Person_' + str(year)
    AddDomainsToGDB(GDB,replace=False)
    GDBDomains = [d.name for d in arcpy.da.ListDomains(GDB)]

    print('[{}] Read Data'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Crash_DF = pd.read_csv(Crash_In_CSV,index_col =0,low_memory=False)
    Crash_DF['DATE'] = pd.to_datetime(Crash_DF.DATE)
    print('[{}]  - Crash {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Crash_DF.shape))
    Veh_DF = pd.read_csv(Veh_In_CSV,index_col =[0,1],low_memory=False)
    print('[{}]  - Veh {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Veh_DF.shape))
    Occ_DF = pd.read_csv(Occ_In_CSV,index_col =[0,1,2], encoding='latin-1',low_memory=False)
    Occ_DF['DOB'] = pd.to_datetime(Occ_DF.DOB)
    print('[{}]  - Occ {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Occ_DF.shape))

    print('[{}] Create Output:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    arcpy.management.Delete(Crash_Out)
    arcpy.management.CreateFeatureclass(out_name = os.path.basename(Crash_Out),
                                    out_path = os.path.dirname(Crash_Out),
                                    spatial_reference=common.NAD1983IL,
                                    geometry_type='POINT',
                                    has_m='DISABLED',
                                    has_z='DISABLED')
    arcpy.AddField_management(Crash_Out,'CID','TEXT')
    Crash_Fields = ['INVENTORY','MP','OFFSET',
        'DATE','NO_VEH',
        'CITY_CLASS','AGENCY',
        'INT_REL','FUNC_CLASS','TWAY_CLASS','TWAY_DESC','TCONT_DEV','TCONT_CON',
        'SURF_CON','ALIGN','DEFECT','LIGHT','SUN_ANG','DAY_NIGHT','WEATHER',
        'COL_TYPE','CAUSE_1','CAUSE_2','HIT_RUN',
        'WZ_OCCUR','WZ_TYPE','WZ_WORKER',
        'K','A','B','C','O','KABCO',
        'EA_RD','EA_IM','EA_IN','EA_DF','EA_TN','EA_WZ','EA_SA','EA_OD','EA_YD','EA_HV','EA_MC','EA_UO','EA_PD','EA_PC'
        ]
    for f in Crash_Fields:
        if getattr(domains,f)['name'] in GDBDomains:
            if translate:
                Crash_DF = common.TranslateDomains(Crash_DF,domains,[f])
                max_len = max([Crash_DF[f].astype(str).apply(len).max(),100])
                arcpy.AddField_management(in_table=Crash_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = 'Text',
                                    field_alias = getattr(domains,f)['alias'],
                                    field_length = max_len
                                    )
            else:
                arcpy.AddField_management(in_table=Crash_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = getattr(domains,f)['type'],
                                    field_alias = getattr(domains,f)['alias'],
                                    field_domain=getattr(domains,f)['name']
                                    )
        else:
            arcpy.AddField_management(in_table=Crash_Out,
                                  field_name=getattr(domains,f)['name'],
                                  field_type = getattr(domains,f)['type'],
                                  field_alias = getattr(domains,f)['alias']
                                 )
    ic = arcpy.InsertCursor(Crash_Out)
    for i,r in Crash_DF.iterrows():
        row = ic.newRow()
        row.setValue('CID',str(i))
        for f in Crash_Fields:
            if not pd.isnull(r[f]):
                row.setValue(f,r[f])
        if not math.isnan(r.X) and not math.isnan(r.Y):
            Pt =  arcpy.PointGeometry(arcpy.Point(r.X,r.Y),common.NAD1983IL)
            row.shape = Pt
        ic.insertRow(row)
    del ic
    del row
    print('[{}]  - Crash {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.GetCount_management(Crash_Out))))

    Veh_DF.reset_index(inplace=True)
    Veh_DF.index = Veh_DF.CID
    Veh_DF['X'] = Crash_DF.X.loc[Veh_DF.index]
    Veh_DF['Y'] = Crash_DF.Y.loc[Veh_DF.index]
    Veh_DF.index = pd.MultiIndex.from_arrays([Veh_DF.CID,Veh_DF.UnitID])

    arcpy.management.Delete(Veh_Out)
    arcpy.management.Delete(Occ_Out)
    arcpy.management.CreateFeatureclass(out_name = os.path.basename(Veh_Out),
                                    out_path = os.path.dirname(Veh_Out),
                                    spatial_reference=common.NAD1983IL,
                                    geometry_type='POINT',
                                    has_m='DISABLED',
                                    has_z='DISABLED')
    Veh_Fields = ['NO_OCC','VEHT', 'VEHU', 'MANV', 'DIRP', 'EXC_SPL', 
        'EVNT1', 'LOC1', 'EVNT2', 'LOC2', 'EVNT3', 'LOC3', 'MHE', 'MHE_LOC', 'MHE_NO',
        'FRST_CONT', 'VEHD', 'TOW', 
        'FIRE_IND', 'HAZMAT', 'CV_IND','V_YEAR', 'V_MAKE', 'V_MODEL',#'VIN11',
        'EA_RD','EA_IM','EA_IN','EA_DF','EA_TN','EA_WZ','EA_SA','EA_OD','EA_YD','EA_HV','EA_MC','EA_UO','EA_PD','EA_PC'
        ]
    arcpy.AddField_management(Veh_Out,'CID','TEXT')
    arcpy.AddField_management(Veh_Out,'CID_UID','TEXT')
    for f in Veh_Fields:
        if getattr(domains,f)['name'] in GDBDomains:
            if translate:
                Veh_DF = common.TranslateDomains(Veh_DF,domains,[f])
                max_len = max([Veh_DF[f].astype(str).apply(len).max(),100])
                arcpy.AddField_management(in_table=Veh_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = 'Text',
                                    field_alias = getattr(domains,f)['alias'],
                                    field_length=max_len
                                    )
            else:
                arcpy.AddField_management(in_table=Veh_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = getattr(domains,f)['type'],
                                    field_alias = getattr(domains,f)['alias'],
                                    field_domain=getattr(domains,f)['name']
                                    )
        else:
            arcpy.AddField_management(in_table=Veh_Out,
                                  field_name=getattr(domains,f)['name'],
                                  field_type = getattr(domains,f)['type'],
                                  field_alias = getattr(domains,f)['alias']
                                 )
    ic = arcpy.InsertCursor(Veh_Out)
    for i,r in Veh_DF.iterrows():
        row = ic.newRow()
        row.setValue('CID',str(i[0]))
        row.setValue('CID_UID','{}_{}'.format(i[0],i[1]))
        for f in Veh_Fields:
            if not pd.isnull(r[f]):
                if getattr(domains,f)['type']=='TEXT':
                    row.setValue(f,str(r[f]))
                else:
                    row.setValue(f,r[f])
        if not math.isnan(r.X) and not math.isnan(r.Y):
            Pt =  arcpy.PointGeometry(arcpy.Point(r.X,r.Y),common.NAD1983IL)
            row.shape = Pt
        ic.insertRow(row)
    del ic
    del row
    print('[{}]  - Vehicle {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.GetCount_management(Veh_Out))))
    
    Occ_DF.reset_index(inplace=True)
    Occ_DF.index = Occ_DF.CID
    Occ_DF['X'] = Crash_DF.X.loc[Occ_DF.index]
    Occ_DF['Y'] = Crash_DF.Y.loc[Occ_DF.index]
    Occ_DF.index = pd.MultiIndex.from_arrays([Occ_DF.CID,Occ_DF.UnitID,Occ_DF.OccID])
    
    arcpy.management.CreateFeatureclass(out_name = os.path.basename(Occ_Out),
                                    out_path = os.path.dirname(Occ_Out),
                                    spatial_reference=common.NAD1983IL,
                                    geometry_type='POINT',
                                    has_m='DISABLED',
                                    has_z='DISABLED')
    Occ_Fields = ['PER_TYPE','DOB','AGE','SEX','INJ_SEV', 'SEAT_POS',
        'SAF_EQI','AIRBAG','EJECT',
        'DR_LIC_ST', 'DR_ACTION', 'DR_VISION', 'DR_CON','BAC','CELL_USE', 
        'PD_ACTION', 'PD_LOC', 'PD_VIS',
        'EMS125', 'HOSPITAL',
        'EA_RD','EA_IM','EA_IN','EA_DF','EA_TN','EA_WZ','EA_SA','EA_OD','EA_YD','EA_HV','EA_MC','EA_UO','EA_PD','EA_PC'
        ]
    arcpy.AddField_management(Occ_Out,'CID','TEXT')
    arcpy.AddField_management(Occ_Out,'CID_UID','TEXT')
    arcpy.AddField_management(Occ_Out,'OID','SHORT')
    for f in Occ_Fields:
        if getattr(domains,f)['name'] in GDBDomains:
            if translate:
                Occ_DF = common.TranslateDomains(Occ_DF,domains,[f])
                max_len = max([Occ_DF[f].astype(str).apply(len).max(),100])
                arcpy.AddField_management(in_table=Occ_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = 'Text',
                                    field_alias = getattr(domains,f)['alias'],
                                    field_length = max_len
                                    )
            else:
                arcpy.AddField_management(in_table=Occ_Out,
                                    field_name=getattr(domains,f)['name'],
                                    field_type = getattr(domains,f)['type'],
                                    field_alias = getattr(domains,f)['alias'],
                                    field_domain=getattr(domains,f)['name']
                                    )
        else:
            arcpy.AddField_management(in_table=Occ_Out,
                                  field_name=getattr(domains,f)['name'],
                                  field_type = getattr(domains,f)['type'],
                                  field_alias = getattr(domains,f)['alias']
                                 )
    ic = arcpy.InsertCursor(Occ_Out)
    for i,r in Occ_DF.iterrows():
        row = ic.newRow()
        row.setValue('CID',str(i[0]))
        row.setValue('CID_UID','{}_{}'.format(i[0],i[1]))
        row.setValue('OID',int(i[2]))
        for f in Occ_Fields:
            if not pd.isnull(r[f]):
                if getattr(domains,f)['type']=='TEXT':
                    row.setValue(f,str(r[f]))
                else:
                    row.setValue(f,r[f])
        if not math.isnan(r.X) and not math.isnan(r.Y):
            Pt =  arcpy.PointGeometry(arcpy.Point(r.X,r.Y),common.NAD1983IL)
            row.shape = Pt
        ic.insertRow(row)
    del ic
    del row
    print('[{}]  - Occupant {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.GetCount_management(Occ_Out))))    

    print('[{}]  Create Relationships'.format(strftime("%Y-%m-%d %H:%M:%S")))    
    arcpy.management.Delete(GDB+'\\Crash_Veh' + str(year))
    arcpy.CreateRelationshipClass_management(
        origin_table = Crash_Out,
        destination_table = Veh_Out,
        out_relationship_class = GDB+'\\Crash_Veh' + str(year),
        relationship_type = "SIMPLE",
        forward_label = "Veh" + str(year),
        backward_label = "Crash" + str(year),
        message_direction = "NONE",
        cardinality = "ONE_TO_MANY",
        attributed = "NONE",
        origin_primary_key = 'CID',
        origin_foreign_key = 'CID')

    arcpy.management.Delete(GDB+'\\Crash_Occ' + str(year))
    arcpy.CreateRelationshipClass_management(
        origin_table = Crash_Out,
        destination_table = Occ_Out,
        out_relationship_class = GDB+'\\Crash_Occ' + str(year),
        relationship_type = "SIMPLE",
        forward_label = "Occ" + str(year),
        backward_label = "Crash" + str(year),
        message_direction = "NONE",
        cardinality = "ONE_TO_MANY",
        attributed = "NONE",
        origin_primary_key = 'CID',
        origin_foreign_key = 'CID')

    arcpy.management.Delete(GDB+'\\Veh_Occ' + str(year))
    arcpy.CreateRelationshipClass_management(
        origin_table = Veh_Out,
        destination_table = Occ_Out,
        out_relationship_class = GDB + '\\Veh_Occ' + str(year),
        relationship_type = "SIMPLE",
        forward_label = "Occ" + str(year),
        backward_label = "Veh" + str(year),
        message_direction = "NONE",
        cardinality = "ONE_TO_MANY",
        attributed = "NONE",
        origin_primary_key = 'CID_UID',
        origin_foreign_key = 'CID_UID')
    Route_Out = GDB + '\\Route_{}'.format(year)
    #arcpy.management.Delete(GDB + '\\Route_Crash' + str(year))
    #arcpy.CreateRelationshipClass_management(
    #    origin_table = Route_Out,
    #    destination_table = Crash_Out,
    #    out_relationship_class = GDB + '\\Route_Crash' + str(year),
    #    relationship_type = "SIMPLE",
    #    forward_label = "Crash" + str(year),
    #    backward_label = "Route" + str(year),
    #    message_direction = "NONE",
    #    cardinality = "ONE_TO_MANY",
    #    attributed = "NONE",
    #    origin_primary_key = 'INVENTORY',
    #    origin_foreign_key = 'INVENTORY')

    print('[{}] Done!'.format(strftime("%Y-%m-%d %H:%M:%S")))

def CON_GeocodeCrashes(WDir,HSMPY_PATH,Crash_In_CSV,Veh_In_CSV,Occ_In_CSV,GDB,year,translate=False):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'Crash_' + str(year) + '_Geocode.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Year = "{}"
print("Crash Geocode: " + Year)
import os, sys
import pandas as pd
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Crash_In_CSV = r'{}'
Veh_In_CSV = r'{}'
Occ_In_CSV = r'{}'
GDB = r'{}'
translate = {}
sys.path.append(HSMPY_PATH) 
import hsmpy3
import numpy as np
import arcpy
hsmpy3.il.GeocodeCrashes(Crash_In_CSV,Veh_In_CSV,Occ_In_CSV,GDB,Year,translate)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(year,HSMPY_PATH,Crash_In_CSV,Veh_In_CSV,Occ_In_CSV,GDB,translate)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)

def GetMarkedRoute(m,t=None):
    s1 = ''
    s2 = ''
    s3 = ''
    if not pd.isnull(m):
        m = str(m)
        if m[0].upper() in ['I','U','S']:
            s1 = m[0].upper()
            s1 = {'I':'I','U':'US','S':'IL'}[s1]
            if m[-1]=='B':
                s2 = int(m[1:-1])
                s3 = 'B'
            else:
                s2 = int(m[1:])
            return('{} {} {}'.format(s1,s2,s3))
        else:
            if not pd.isnull(t):
                t = str(t)
                if t.upper() in ['I','U','S']:
                    s1 = t.upper()
                    s1 = {'I':'I','U':'US','S':'IL'}[s1]
                    if m[-1]=='B':
                        s2 = int(m[:-1])
                        s3 = 'B'
                    else:
                        s2 = int(m)
                    return('{} {} {}'.format(s1,s2,s3))
def GetMarkedRouteType(r1,r2,r3,r4):
    t = []
    try:
        t.append(r1.split(' ')[0])
    except:
        pass
    try:
        t.append(r2.split(' ')[0])
    except:
        pass    
    try:
        t.append(r3.split(' ')[0])
    except:
        pass    
    try:
        t.append(r4.split(' ')[0])
    except:
        pass    
    t = list(set(t))
    if len(t)>0:
        my_order = ['I','US','IL']
        order = {key: i for i, key in enumerate(my_order)}
        t = sorted(t, key=lambda d: order[d])
        return(';'.join(t))
def IRIS_Cleanup(CSV_In,Output,year):
    warnings.filterwarnings('ignore')

    print('[{}] Read Data: {}'.format(strftime("%Y-%m-%d %H:%M:%S"),CSV_In))
    IRIS_DF = pd.read_csv(CSV_In,low_memory=False)
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),IRIS_DF.shape))

    print('[{}] Clean ups:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    IRIS_DF.YEAR = year
    IRIS_DF.index = pd.MultiIndex.from_tuples([(inv,bmp,emp) for inv,bmp,emp in zip(IRIS_DF.INVENTORY,IRIS_DF.BEG_STA,IRIS_DF.END_STA)],names=['INVENTORY','BMP','EMP'])
    IRIS_DF['LENGTH'] = IRIS_DF.END_STA - IRIS_DF.BEG_STA
    IRIS_DF = IRIS_DF.sort_index()
    for f in ['MARKED_RT','MARKED_RT2','MARKED_RT3','MARKED_RT4','MRK_RT_TYP','MRK_RT_TY2','MRK_RT_TY3','MRK_RT_TY4','ROAD_NAME']:
        if f in IRIS_DF.columns:
            IRIS_DF.loc[IRIS_DF[f]==' ',f] = None
    for r,t in zip(['MARKED_RT','MARKED_RT2','MARKED_RT3','MARKED_RT4'],['MRK_RT_TYP','MRK_RT_TY2','MRK_RT_TY3','MRK_RT_TY4']):
        if t in IRIS_DF.columns:
            IRIS_DF[r] = [GetMarkedRoute(r1,t1) for r1,t1 in zip(IRIS_DF[r],IRIS_DF[t])]
        else:
            IRIS_DF[r] = [GetMarkedRoute(r1,None) for r1 in IRIS_DF[r]]
    IRIS_DF['MRK_RT_TYP'] = [GetMarkedRouteType(r1,r2,r3,r4) for r1,r2,r3,r4 in zip(IRIS_DF.MARKED_RT,IRIS_DF.MARKED_RT2,IRIS_DF.MARKED_RT3,IRIS_DF.MARKED_RT4)]
    for f in ['JUR_TYPE','OP_1_2_WAY','SP_LIM']:
        if f in IRIS_DF.columns:
            IRIS_DF[f] = IRIS_DF[f].astype(str)
            IRIS_DF.loc[IRIS_DF[f] == ' ',f] = None
            IRIS_DF.loc[IRIS_DF[f] == '0',f] = None
            IRIS_DF[f] = IRIS_DF[f].astype(int,errors='ignore')
    for f in ['AADT','SU_VOL','MU_VOL','HCV']:
        if f in IRIS_DF.columns:
            IRIS_DF[f] = IRIS_DF[f].fillna(0)
            IRIS_DF[f] = IRIS_DF[f].astype(int)
            IRIS_DF.loc[IRIS_DF[f]==0,f] = np.NaN
            IRIS_DF[f] = IRIS_DF[f].astype(int,errors='ignore')
    for f in ['AADT_YR','HCV_MU_YR','SURF_YR']: 
        if f in IRIS_DF.columns:
            try:
                IRIS_DF.loc[IRIS_DF[f]==' ',f] = 0
            except:
                pass
            IRIS_DF[f] = IRIS_DF[f].astype(int)
            IRIS_DF.loc[IRIS_DF[f]==0,f] = np.NaN
            IRIS_DF[f] = IRIS_DF[f].astype(int,errors='ignore')
    IRIS_DF.loc[pd.isnull(IRIS_DF['AADT']),'AADT_YR'] = np.NaN
    IRIS_DF.loc[pd.isnull(IRIS_DF['HCV']),'HCV_MU_YR'] = np.NaN
    IRIS_DF.LENGTH = IRIS_DF.END_STA - IRIS_DF.BEG_STA
    for f in ['FUNC_CLASS','FC']:
        if f in IRIS_DF.columns:
            IRIS_DF[f] = IRIS_DF[f].astype(str)
            IRIS_DF.loc[IRIS_DF[f]==' ',f] = 0
            IRIS_DF[f] = IRIS_DF[f].fillna(0)
            IRIS_DF[f] = IRIS_DF[f].astype(float)
            IRIS_DF[f] = IRIS_DF[f].fillna(0)
            IRIS_DF[f] = IRIS_DF[f].astype(int)
            IRIS_DF.loc[IRIS_DF[f]==0,f] = np.NaN
            IRIS_DF[f] = IRIS_DF[f].astype(int,errors='ignore')
    if not 'FUNC_CLASS' in IRIS_DF.columns:
        IRIS_DF['FUNC_CLASS'] = IRIS_DF.FC
    IRIS_DF.FUNC_CLASS.loc[IRIS_DF.FUNC_CLASS.isin([10])] = 1
    IRIS_DF.FUNC_CLASS.loc[IRIS_DF.FUNC_CLASS.isin([20])] = 2
    IRIS_DF.FUNC_CLASS.loc[IRIS_DF.FUNC_CLASS.isin([30])] = 3
    IRIS_DF.FUNC_CLASS.loc[IRIS_DF.FUNC_CLASS.isin([40,70])] = 4
    IRIS_DF.FUNC_CLASS.loc[IRIS_DF.FUNC_CLASS.isin([50,80])] = 5
    IRIS_DF.FUNC_CLASS.loc[IRIS_DF.FUNC_CLASS.isin([55])] = 6
    IRIS_DF.FUNC_CLASS.loc[IRIS_DF.FUNC_CLASS.isin([60,90])] = 7
    for f in ['ACC_CNTL','TOLL','TRK_RT','URBAN']: 
        if f in IRIS_DF.columns:
            try:
                IRIS_DF.loc[IRIS_DF[f]==' ',f] = 0
            except:
                pass
            IRIS_DF[f] = IRIS_DF[f].fillna(0)
            IRIS_DF[f] = IRIS_DF[f].astype(int)
    for f in ['I_SHD1_TYP', 'I_SHD2_TYP','O_SHD1_TYP', 'O_SHD2_TYP','MED_TYP','SURF_TYP']:
        if f in IRIS_DF.columns:
            try:
                IRIS_DF.loc[IRIS_DF[f]==' ',f] = 0
            except:
                pass
            IRIS_DF[f] = IRIS_DF[f].fillna(0)
            IRIS_DF[f] = IRIS_DF[f].astype(int)
    for f in ['I_SHD1_WTH', 'I_SHD2_WTH','O_SHD1_WTH', 'O_SHD2_WTH','LN_WTH','LN_SPC_WTH','MED_WTH','SURF_WTH']:
        if f in IRIS_DF.columns:
            try:
                IRIS_DF.loc[IRIS_DF[f]==' ',f] = 0
            except:
                pass
            IRIS_DF[f] = IRIS_DF[f].fillna(0)
            IRIS_DF[f] = IRIS_DF[f].astype(int)

    for f in ['LNS','LANES','LN_SPC_NBR']:
        if f in IRIS_DF.columns:
            try:
                IRIS_DF.loc[IRIS_DF[f]==' ',f] = 0
            except:
                pass
            IRIS_DF[f] = IRIS_DF[f].fillna(0)
            IRIS_DF[f] = IRIS_DF[f].astype(int)
    if not 'LANES' in IRIS_DF.columns:
        IRIS_DF['LANES'] = IRIS_DF.LNS
    IRIS_DF = IRIS_DF.rename(columns={'LN_SPC':'LN_SPC_TYP'})
    IRIS_DF = IRIS_DF.rename(columns={'LN_SPC_NBR':'LN_SPC'})
    for f in ['LN_SPC']:
        if f in IRIS_DF.columns:
            IRIS_DF[f] = IRIS_DF[f].astype(str)
            IRIS_DF.loc[IRIS_DF[f]==' ',f] = 0
            IRIS_DF[f] = IRIS_DF[f].fillna(0)
            IRIS_DF[f] = IRIS_DF[f].astype(float)
            IRIS_DF[f] = IRIS_DF[f].fillna(0)
            IRIS_DF[f] = IRIS_DF[f].astype(int)
            IRIS_DF.loc[IRIS_DF[f]==0,f] = np.NaN
            IRIS_DF[f] = IRIS_DF[f].astype(int,errors='ignore')

    for f in ['LN_WTH','LANES','LN_SPC_WTH','SURF_WTH','PRK_LT','PRK_RT']:
        if f in IRIS_DF.columns:
            IRIS_DF.loc[IRIS_DF[f]==0,f] = np.NaN
            IRIS_DF[f] = IRIS_DF[f].astype(int,errors='ignore')

    IRIS_DF.loc[pd.isnull(IRIS_DF['LN_SPC']),'LN_SPC_TYP'] = np.NaN
    IRIS_DF.loc[pd.isnull(IRIS_DF['LN_SPC']),'LN_SPC_WTH'] = np.NaN
    IRIS_DF.loc[pd.isnull(IRIS_DF['SURF_WTH']),'SURF_YR'] = np.NaN

    IRIS_DF.loc[IRIS_DF['I_SHD1_TYP']==0,'I_SHD1_WTH'] = np.NaN
    IRIS_DF.loc[IRIS_DF['I_SHD2_TYP']==0,'I_SHD2_WTH'] = np.NaN
    IRIS_DF.loc[IRIS_DF['O_SHD1_TYP']==0,'O_SHD1_WTH'] = np.NaN
    IRIS_DF.loc[IRIS_DF['O_SHD2_TYP']==0,'O_SHD2_WTH'] = np.NaN
    IRIS_DF.loc[IRIS_DF['MED_TYP']==0,'MED_WTH'] = np.NaN
    IRIS_DF['COUNTY'] = [int(inv[0:3]) for inv in IRIS_DF.INVENTORY]
    IRIS_DF['KEY_RT_SEG'] = [str(inv[3:5]) for inv in IRIS_DF.INVENTORY]
    IRIS_DF['KEY_RT_TYP'] = [int(inv[5:6]) for inv in IRIS_DF.INVENTORY]
    IRIS_DF['KEY_RT_NBR'] = [int(inv[6:10]) for inv in IRIS_DF.INVENTORY]
    IRIS_DF['KEY_RT_SUF'] = [str(inv[10:11]) for inv in IRIS_DF.INVENTORY]
    IRIS_DF['KEY_RT_APP'] = [int(inv[11:12]) for inv in IRIS_DF.INVENTORY]
    IRIS_DF['KEY_RT_APN'] = [int(inv[12:17]) for inv in IRIS_DF.INVENTORY]
    for f in ['KEY_RT_SEG','KEY_RT_SUF']: 
        if f in IRIS_DF.columns:
            IRIS_DF.loc[IRIS_DF[f].isin([' ','  ']),f] = np.NaN
    IRIS_DF['PG'] = [FindPG_Cleaned(JUR_TYPE,URBAN,KEY_RT_APP,FCNAME,LNS,MED_TYP,OP_1_2_WAY) for JUR_TYPE,URBAN,KEY_RT_APP,FCNAME,LNS,MED_TYP,OP_1_2_WAY in 
                     zip(IRIS_DF.JUR_TYPE,IRIS_DF.URBAN,IRIS_DF.KEY_RT_APP,IRIS_DF.FUNC_CLASS,IRIS_DF.LANES,IRIS_DF.MED_TYP,IRIS_DF.OP_1_2_WAY)]

    IRIS_DF = IRIS_DF[['LENGTH','COUNTY','KEY_RT_SEG','KEY_RT_TYP','KEY_RT_NBR','KEY_RT_SUF','KEY_RT_APP','KEY_RT_APN',
        'MARKED_RT','MARKED_RT2','MARKED_RT3','MARKED_RT4','MRK_RT_TYP','ROAD_NAME',
                       'FUNC_CLASS','JUR_TYPE','URBAN','OP_1_2_WAY','SP_LIM',
                       'ACC_CNTL','TOLL','TRK_RT','PG',
                       'AADT','AADT_YR',
                       'HCV','SU_VOL','MU_VOL','HCV_MU_YR',
                       'LANES','LN_WTH','LN_SPC','LN_SPC_TYP','LN_SPC_WTH',
                       'MED_TYP','MED_WTH',
                       'O_SHD1_TYP','O_SHD1_WTH', 'O_SHD2_TYP', 'O_SHD2_WTH',
                       'I_SHD1_TYP','I_SHD1_WTH', 'I_SHD2_TYP', 'I_SHD2_WTH',
                       'SURF_TYP','SURF_WTH','SURF_YR',
                       'PRK_LT','PRK_RT'
                       ]]
    IRIS_DF = IRIS_DF.sort_values(['KEY_RT_TYP','KEY_RT_NBR','COUNTY'])
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),IRIS_DF.shape))


    print('[{}] Export:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Project_Dir = r'\\CHCFPP01\Proj\ILDOT\650511SAFETYPROGRAM\4_WorkData\WO19\IL_Crash_Assignment'
    SourceDir = Project_Dir + '\\IRIS_Original'
    OutputDir = Project_Dir + '\\IRIS_Cleaned'
    IRIS_DF.to_csv(OutputDir + '\\HWY_{}_Cleaned.csv'.format(year))

    GDB = os.path.dirname(Output)
    Diss = GDB + '\\Diss_{}'.format(year)
    GDBDomains = [d.name for d in arcpy.da.ListDomains(GDB)]
    arcpy.management.Delete(Diss)
    arcpy.CreateTable_management(out_path=GDB,out_name=os.path.basename(Diss))
    for f,ft in zip(['RID','BMP','EMP'],['TEXT','DOUBLE','DOUBLE']):
        arcpy.management.AddField(Diss,f,ft)
    for f in list(IRIS_DF.columns):
        if getattr(domains,f)['name'] in GDBDomains:
            arcpy.AddField_management(in_table=Diss,
                                  field_name=getattr(domains,f)['name'],
                                  field_type = getattr(domains,f)['type'],
                                  field_alias = getattr(domains,f)['alias'],
                                  field_domain=getattr(domains,f)['name']
                                 )
        else:
            arcpy.AddField_management(in_table=Diss,
                                  field_name=getattr(domains,f)['name'],
                                  field_type = getattr(domains,f)['type'],
                                  field_alias = getattr(domains,f)['alias']
                                 )
    ic = arcpy.InsertCursor(Diss)
    for i,r in IRIS_DF.iterrows():
        row = ic.newRow()
        row.setValue('RID',str(i[0]))
        row.setValue('BMP',i[1])
        row.setValue('EMP',i[2])
        for f in list(IRIS_DF.columns):
            if not pd.isnull(r[f]):
                try:
                    row.setValue(f,r[f])
                except:
                    print(f,r[f])
        ic.insertRow(row)
    del ic
    del row
    n1 = arcpy.management.GetCount(Diss)[0]
    print('[{}]  - Initial Table {}:'.format(strftime("%Y-%m-%d %H:%M:%S"),n1))

    arcpy.management.Delete(Output)
    Fields = [f.name for f in arcpy.ListFields(Diss)]
    [Fields.remove(x) for x in ['RID','BMP','EMP','OBJECTID']]
    arcpy.lr.DissolveRouteEvents(
        in_events = Diss, 
        in_event_properties = ' '.join(['RID','LINE','BMP','EMP']), 
        dissolve_field = ';'.join(Fields), 
        out_table = Output, 
        out_event_properties = ' '.join(['RID','LINE','BMP','EMP'])
        )
    arcpy.CalculateField_management(Output,'LENGTH','!EMP!-!BMP!','PYTHON3')
    n2 = arcpy.management.GetCount(Output)[0]
    print('[{}]  - Final Dissolved Table {}:'.format(strftime("%Y-%m-%d %H:%M:%S"),n2))
    arcpy.management.Delete(Diss)
    #IRIS_DF.to_csv(CSV_Out)
    print('[{}] Done!'.format(strftime("%Y-%m-%d %H:%M:%S")))
def CON_IRIS_Cleanup(WDir,HSMPY_PATH,CSV_In,CSV_Out,year):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'IRIS_' + str(year) + '_Cleanup.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Year = "{}"
print("IRIS Cleanup: " + Year)
import os, sys
import pandas as pd
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
CSV_In = r'{}'
CSV_Out = r'{}'
sys.path.append(HSMPY_PATH) 
import hsmpy3
import numpy as np
import arcpy
hsmpy3.il.IRIS_Cleanup(CSV_In,CSV_Out,Year)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(year,HSMPY_PATH,CSV_In,CSV_Out)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def DissolveTimeMP(CSV_In,Fields,CSV_Out):
    FList = Fields
    print('[{}] read {}:'.format(strftime("%Y-%m-%d %H:%M:%S"),CSV_In))
    IRIS_DF = pd.read_csv(CSV_In,low_memory=False)
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),IRIS_DF.shape))
    print('[{}] indexing and sorting ...'.format(strftime("%Y-%m-%d %H:%M:%S")))
    idx1 = pd.Index(IRIS_DF.INVENTORY)
    idx2 = pd.IntervalIndex.from_tuples([(bmp,emp) for bmp,emp in zip(IRIS_DF.BMP,IRIS_DF.EMP)],closed = 'left')
    idx3 = pd.IntervalIndex.from_tuples([(datetime(year,1,1),datetime(year+1,1,1)) for year in IRIS_DF.YEAR],closed='left')
    IRIS_DF.index = pd.MultiIndex.from_arrays([idx1,idx2,idx3],names=['INVENTORY','Milepost','Time'])
    IRIS_DF = IRIS_DF.sort_index()
    print('[{}] start dissolving:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Diss_DF = pd.DataFrame()
    for inv in list(set(IRIS_DF.INVENTORY)):
        # Query the data and list indices
        df = IRIS_DF.loc[inv][FList + ['BMP','EMP','YEAR']]
        df = df[~df.duplicated()]
        idx = list(df.index)
        df1 = pd.DataFrame(columns=['BMP','EMP','StartTime','EndTime'])
        for i,n in enumerate(idx):
            df1.loc[i] = [idx[i][0].left,idx[i][0].right,idx[i][1].left,idx[i][1].right]
        mps = list(set(df1.BMP).union(set(df1.EMP)))
        mps.sort()
        tss = list(set(df1.StartTime).union(set(df1.EndTime)))
        tss.sort()

        #explode events
        df2 = pd.DataFrame(columns=FList,index= pd.MultiIndex.from_product([pd.IntervalIndex.from_breaks(mps,'left'),
                                                                            pd.IntervalIndex.from_breaks(tss,'left')]))
        idf = pd.DataFrame(columns=df2.index.levels[1],index=df2.index.levels[0])
        for c in idf.columns:
            df3 = df[df.YEAR==c.left.year].unstack()

            for i in idf.index:
                try:
                    idf.loc[i,c] = list(df3.loc[[i]].index)
                except:
                    print('{}: {} Not found in {}'.format(inv,i,c))

        for ts in df2.index.droplevel(0):
            df3 = df[df.YEAR==ts.left.year]
            df3.index = df3.index.droplevel(1)
            for f in FList:
                df4 = df3[f]
                for mp in df2.index.droplevel(1):
                    try:
                        df2.loc[mp].loc[ts][f] = df4.loc[idf.loc[mp][ts]].item()
                    except:
                        pass
        #dissolve events
        df5 = pd.DataFrame()
        for mp_int in df2.index.levels[0]:
            df3 = df2.loc[mp_int]
            BMP = [i.left for i in df3.index]
            EMP = [i.right for i in df3.index]
            BMP_N = [BMP[0]]
            EMP_N = [EMP[0]]
            df4 = pd.DataFrame(columns=range(df3.shape[1]))
            df4.loc[0] = list(df3.iloc[0])
            for i in range(1,len(BMP)):
                if BMP[i]==EMP[i-1] and df3.iloc[i].equals(df3.iloc[i-1]):
                    EMP_N[-1] = EMP[i]
                else:
                    df4.loc[i] = list(df3.iloc[i])
                    BMP_N.append(BMP[i])
                    EMP_N.append(EMP[i])
            df4.columns = df3.columns
            idx1 = pd.IntervalIndex([mp_int]*len(BMP_N))
            idx2 = pd.IntervalIndex.from_tuples([(bmp,emp) for bmp,emp in zip(BMP_N,EMP_N)],'left')
            df4.index = pd.MultiIndex.from_arrays([idx1,idx2])
            df5 = pd.concat([df5,df4])
        df5 = pd.concat([df5], keys=[inv])
        Diss_DF = pd.concat([Diss_DF,df5])
        print('[{}] {}: {} dissolved to {}'.format(strftime("%Y-%m-%d %H:%M:%S"),inv,df.shape[0],df5.shape[0]))
    print('[{}] finished: {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Diss_DF.shape))
    print('[{}] export {}'.format(strftime("%Y-%m-%d %H:%M:%S"),CSV_Out))
    Diss_DF.to_csv(CSV_Out)
    print('[{}] done!'.format(strftime("%Y-%m-%d %H:%M:%S"),Diss_DF.shape))
def CON_DissolveTimeMP(WDir,HSMPY_PATH,CSV_In,Fields,CSV_Out):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'DissolveTimeMP.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
print("Dissolve By Time and MP")
import os, sys
HSMPY_PATH = r'{}'
sys.path.append(HSMPY_PATH) 
import hsmpy3
import atexit
atexit.register(input, 'Press Enter to continue...')
CSV_In = r'{}'
Fields = {}
CSV_Out = r'{}'
hsmpy3.il.DissolveTimeMP(CSV_In,Fields,CSV_Out)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,CSV_In,Fields,CSV_Out)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def CON_CrashCSVBySeverity(WDir,HSMPY_PATH,CrashDict,OutputDict):
    sys.path.append(HSMPY_PATH)
    pyFN = os.path.join(WDir , 'CrashbySev.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
Year = "{}"
print("Crash By Severity")
import os, sys
import pandas as pd
import atexit
atexit.register(input, 'Press Enter to continue...')
CrashDict = {}
OutputDict = {}
for y in list(CrashDict.keys()):
    df = pd.read_csv(DB_Dir+'\\{}_Crash_Assigned.csv'.format(year),index_col=0)
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['YEAR'] = year
    Crash_DF = pd.concat([Crash_DF,df])
    df = pd.read_csv(DB_Dir+'\\{}_Vehicle_Cleaned_EA.csv'.format(year),index_col=[0,1])
    df['YEAR'] = year
    Veh_DF = pd.concat([Veh_DF,df])
    df = pd.read_csv(DB_Dir+'\\{}_Person_Cleaned_EA.csv'.format(year),index_col=[0,1,2], encoding='latin-1',low_memory=False)
    df['DOB'] = pd.to_datetime(df['DOB'])
    df['YEAR'] = year
    Occ_DF = pd.concat([Occ_DF,df])
    print(year)

print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(year,HSMPY_PATH,CSV_In,CSV_Out)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def NewBMPEMP(RID,BMP,EMP,NextRID,NextBMP,PrevRID,PrevEMP):
        NewBMP = BMP
        NewEMP = EMP
        if NextRID == RID:
            if NextBMP<EMP:
                NewEMP = np.mean([NextBMP,EMP])
        if PrevRID==RID:
            if PrevEMP>BMP:
                NewBMP = np.mean([PrevEMP,BMP])
        return([NewBMP,NewEMP])

def OverlayIntersections(IntInput,Routes,AttTab,year):
    print('[{}] locate features along routes:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Project_GDB = os.path.dirname(IntInput)
    EventTable = common.CreateOutPath(MainFile=Project_GDB + '\\Int_'+str(year),appendix='EventTable',Extension='')
    arcpy.LocateFeaturesAlongRoutes_lr(
        in_features                = IntInput, 
        in_routes                = Routes, 
        route_id_field            = 'INVENTORY', 
        radius_or_tolerance        = '70 Feet', 
        out_table                = EventTable, 
        out_event_properties    = " ".join(['RID', "POINT", "MP"]),
        route_locations            = "ALL", 
        in_fields                = "FIELDS", 
        m_direction_offsetting    = "M_DIRECTON"
    )
    df = common.FCtoDF(EventTable)
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape[0]))

    print('[{}] attribute table to pandas:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Att_DF = common.FCtoDF(AttTab)
    Att_DF = Att_DF.sort_values(by=['RID','BMP'])
    Att_DF['Len'] = Att_DF.EMP-Att_DF.BMP
    Att_DF = Att_DF[(Att_DF.Len>0)]

    Att_DF['SurfWid'] = 24.0
    for i,r in Att_DF.iterrows():
        nl = 2
        try:
            nl = int(r.LANES)
        except:
            pass
        nsl = 0
        try:
            nsl = int(r.LN_SPC)
        except:
            pass
        lw = 12.0
        try:
            lw = float(r.LN_WTH)
        except:
            pass
        slw = 12
        try:
            slw = float(r.LN_SPC_WTH)
        except:
            pass
        mdw = 0
        try:
            mdw = int(r.MED_WTH)
        except:
            pass
        osh1 = 0
        try:
            osh1 = int(r.O_SHD1_WTH)
        except:
            pass
        osh2 = 0
        try:
            osh2 = int(r.O_SHD2_WTH)
        except:
            pass
        surfwid = max(24,nl*lw+nsl*slw+mdw+osh1+osh2)
        Att_DF.set_value(i,'SurfWid',surfwid)

        aadt = r.AADT
        try:
            aadt = int(aadt)
        except:
            aadt = 0
        Att_DF.set_value(i,'AADT',aadt)
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Att_DF.shape[0]))

    print('[{}] join att data to int:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    df['SurfWid'] = 30.0
    df['AADT'] = 0.0
    df['FType'] = ''
    for i,r in df.iterrows():
        att_df = Att_DF[(Att_DF['RID']==r.RID) & (Att_DF.BMP<=r.MP) & (Att_DF.EMP>=r.MP)]
        if att_df.shape[0]>0:
            df.set_value(i,'SurfWid',max(list(att_df.SurfWid)))
            df.set_value(i,'AADT',max(list(att_df.AADT)))
            #df.set_value(i,'FType',list(att_df.FType)[0])
    
    print('[{}] routes to pandas:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    df['fpM'] = 0.0
    df['lpM'] = 0.0
    Routes_DF = common.FCtoDF(Routes,True)
    Routes_DF = Routes_DF.rename(columns={'INVENTORY':"RID",'BEG_STA':'BMP','END_STA':'EMP'})
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Att_DF.shape[0]))

    print('[{}] join route data to int:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    for i,r in df.iterrows():
        Rdf = Routes_DF[(Routes_DF['RID']==r.RID) & (Routes_DF['BMP']<=r.MP) & (Routes_DF['EMP']>=r.MP)]
        M = [s.M for s in list(Rdf.Shape)[0][0]]
        df.set_value(i,'fpM',M[0])
        df.set_value(i,'lpM',M[-1])
        
    print('[{}] identify major approach:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    df['Major'] = 0
    intL = list(set(df.Int_ID))
    for intid in intL:
        Rdf = df[df.Int_ID==intid]
        maxAADT = max(Rdf.AADT)
        i = list(Rdf[Rdf.AADT==maxAADT].index)[0]
        rid = Rdf.loc[i,'RID']
        ridL = [rid]
        for ind in list(Rdf.index):
            if Rdf.loc[ind,'RID'] in ridL:
                df.set_value(ind,'Major',1)
            else:
                df.set_value(ind,'Major',0)
        
    print('[{}] create approach dataframe:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    App_DF = df
    App_DF['Int_ID2'] = App_DF.Int_ID
    App_DF['RID'] = App_DF.RID
    App_Tab = pd.DataFrame(columns=['RID','BMP','EMP','IntProx','Int_ID2','Major'])
    x = 0
    for i,r in Routes_DF.iterrows():
        rid = r.RID
        app_all = App_DF[(App_DF.RID==rid) & (App_DF.Int_ID2!=0) & (~pd.isnull(App_DF.MP))]
        mp_List = list(set(app_all.MP))
        mp_List.sort()
        int_id_List = [list(app_all[app_all.MP==mp]['Int_ID2'])[0] for mp in mp_List]
        for int_id,mp in zip(int_id_List,mp_List):
            app    = App_DF[(App_DF.RID==rid) & (App_DF.Int_ID2==int_id)]
            app_x  = App_DF[(App_DF.Int_ID2==int_id) & (App_DF.RID!=rid)]

            int_w = [40.0]
            int_w.extend(list(app_x.SurfWid))
            int_w = float(max(int_w))/5280.0

            int_b = 250.0/5280.0

            #if (1 in list(app.Signal)) and 1 in list(app.Major):
            #    int_b = 250.0/5280.0 + int_w
            #if (1 in list(app.Signal)) and not (1 in list(app.Major)):
            #    int_b = 250.0/5280.0 + int_w
            #if not (1 in list(app.Signal)) and 1 in list(app.Major):
            #    int_b = 250.0/5280.0 + int_w
            #if not (1 in list(app.Signal)) and not (1 in list(app.Major)):
            #    int_b = 150.0/5280.0 + int_w

            bmp1 = max(mp - int_w - int_b,list(app.fpM)[0])
            #emp1 = max(mp - int_w,list(app.fpM)[0])
            #if emp1>bmp1:
            #    x += 1
            #    App_Tab.loc[x] = [rid,bmp1,emp1,1,int_id,{True:1,False:0}[1 in list(app.Major)]]

            #bmp2 = max(mp - int_w,list(app.fpM)[0])
            #emp2 = min(mp + int_w,list(app.lpM)[0])
            #if emp2>bmp2:
            #    x += 1
            #    App_Tab.loc[x] = [rid,bmp2,emp2,2,int_id,{True:1,False:0}[1 in list(app.Major)]]

            #bmp3 = min(mp + int_w,list(app.lpM)[0])
            emp3 = min(mp + int_w + int_b,list(app.lpM)[0])
            if emp3>bmp1:
                x += 1
                App_Tab.loc[x] = [rid,bmp1,emp3,1,int_id,{True:1,False:0}[1 in list(app.Major)]]
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),App_Tab.shape[0]))

    print('[{}] adjust overlaping approaches:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    App_Tab = App_Tab.sort_values(by=['RID','BMP'])
    r = list(App_Tab.RID)[1:]
    r.append('')
    App_Tab['NextRID'] = r
    r = list(App_Tab.BMP)[1:]
    r.append('')
    App_Tab['NextBMP'] = r

    r = ['']
    r.extend(list(App_Tab.RID)[:-1])
    App_Tab['PrevRID'] = r
    r = ['']
    r.extend(list(App_Tab.EMP)[:-1])
    App_Tab['PrevEMP'] = r

    App_Tab['NewBMPEMP']  = [NewBMPEMP(rid,bmp,emp,nrid,nbmp,prid,pemp) for rid,bmp,emp,nrid,nbmp,prid,pemp in 
                             zip(App_Tab.RID,App_Tab.BMP,App_Tab.EMP,App_Tab.NextRID,App_Tab.NextBMP,App_Tab.PrevRID,App_Tab.PrevEMP)]

    print('[{}] create int approach table:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    App_Table = common.CreateOutPath(Project_GDB + '\\CreateInt_AppTab',str(year),'')
    arcpy.management.CreateTable(out_name=os.path.basename(App_Table),out_path=Project_GDB)
    arcpy.management.AddField(App_Table,'RID','Text')
    arcpy.management.AddField(App_Table,'BMP','Double')
    arcpy.management.AddField(App_Table,'EMP','Double')
    arcpy.management.AddField(App_Table,'Int_ID','Long')
    arcpy.management.AddField(App_Table,'IntProx','Short')
    arcpy.management.AddField(App_Table,'Major','Short')
    ic = arcpy.InsertCursor(App_Table)
    for i,r in App_Tab.iterrows():
        row = ic.newRow()
        row.setValue('RID',r.RID)
        row.setValue('BMP',r.NewBMPEMP[0])
        row.setValue('EMP',r.NewBMPEMP[1])
        row.setValue('Int_ID',r.Int_ID2)
        row.setValue('Major',r.Major)
        row.setValue('IntProx',r.IntProx)
        ic.insertRow(row)
    del ic
    del row    
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.management.GetCount(App_Table))))

    print('[{}] intersect overlay int approach table:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    IntAppOverlay = common.CreateOutPath(MainFile=Project_GDB+'\\IntApp_Overlay',appendix=str(year),Extension='')
    arcpy.lr.OverlayRouteEvents(
            in_table                 = Project_GDB+'\\CreateInt_AppTab_' + str(year),
            in_event_properties      = ' '.join(['RID','LINE','BMP','EMP']), 
            overlay_table            = AttTab,
            overlay_event_properties = ' '.join(['RID','LINE','BMP','EMP']),
            overlay_type             = "INTERSECT", 
            out_table                = IntAppOverlay, 
            out_event_properties     = ' '.join(['RID','LINE','BMP','EMP']),
            zero_length_events       = "ZERO", 
            in_fields                = "FIELDS", 
            build_index              = "INDEX"
    )
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.management.GetCount(IntAppOverlay))))
    
    print('[{}] union overlay int approach table:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    SegIntAtt = common.CreateOutPath(MainFile=Project_GDB+'\\SegInt_Att',appendix=str(year),Extension='')
    arcpy.lr.OverlayRouteEvents(
            in_table                 = AttTab,
            in_event_properties      = ' '.join(['RID','LINE','BMP','EMP']), 
            overlay_table            = Project_GDB+'\\CreateInt_AppTab_' + str(year),
            overlay_event_properties = ' '.join(['RID','LINE','BMP','EMP']),
            overlay_type             = "UNION", 
            out_table                = SegIntAtt, 
            out_event_properties     = ' '.join(['RID','LINE','BMP','EMP']),
            zero_length_events       = "ZERO", 
            in_fields                = "FIELDS", 
            build_index              = "INDEX"
    )
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.management.GetCount(SegIntAtt))))

    print('[{}] update cursor int FC:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    df = common.FCtoDF(SegIntAtt)
    df = df[df.Int_ID>0]
    df = df.sort_values('Int_ID')
    Int = common.CreateOutPath(MainFile=Project_GDB+'\\Int',Extension='',appendix=str(year))
    arcpy.conversion.FeatureClassToFeatureClass(in_features=IntInput,out_name=os.path.basename(Int),out_path=Project_GDB)
    #arcpy.management.AddField(Int,'IFType','Text',10)
    #arcpy.management.AddField(Int,'I_URBANCODE','Long')
    #arcpy.management.AddField(Int,'FType_Major','Text',10)
    #arcpy.management.AddField(Int,'FType_Minor','Text',10)
    #arcpy.management.AddField(Int,'F_SYSTEM_Major','Short')
    #arcpy.management.AddField(Int,'F_SYSTEM_Minor','Short')
    #arcpy.management.AddField(Int,'OWNERSHIP_Major','Short')
    #arcpy.management.AddField(Int,'OWNERSHIP_Minor','Short')
    arcpy.management.AddField(Int,'AADT_Major','Long')    
    arcpy.management.AddField(Int,'AADT_Minor','Long')    
    uc = arcpy.UpdateCursor(Int)
    for row in uc:
        int_id = row.getValue('IID')
        signal = row.getValue('TCON_TYP')
        legs = row.getValue('LEGS_COUNT')
        type_major = ''
        
        idf = df[df.Int_ID==int_id]

        ft = list(idf[idf.Major==1]['AADT'])
        if len(ft)>0:
            row.setValue('AADT_Major',int(max(ft)))

        ft = list(idf[idf.Major==0]['AADT'])
        if len(ft)>0:
            row.setValue('AADT_Minor',int(max(ft)))

        #ft = [t for t in set(list(idf[idf.Major==1]['FType'])) if t]
        #if len(ft)>0:
        #    row.setValue('FType_Major',ft[0]) 
        #    type_major = ft[0]
        #ft = [t for t in set(list(idf[idf.Major==0]['FType'])) if t]
        #if len(ft)>0:
        #    row.setValue('FType_Minor',ft[0]) 

        #ft = [t for t in set(list(idf[idf.Major==1]['F_SYSTEM'])) if t]
        #if len(ft)>0:
        #    row.setValue('F_SYSTEM_Major',int(ft[0])) 

        #ft = [t for t in set(list(idf[idf.Major==0]['F_SYSTEM'])) if t]
        #if len(ft)>0:
        #    row.setValue('F_SYSTEM_Minor',int(ft[0])) 

        #ft = [t for t in set(list(idf[idf.Major==1]['OWNERSHIP'])) if t]
        #if len(ft)>0:
        #    row.setValue('OWNERSHIP_Major',int(ft[0]))

        #ft = [t for t in set(list(idf[idf.Major==0]['OWNERSHIP'])) if t]
        #if len(ft)>0:
        #    row.setValue('OWNERSHIP_Minor',int(ft[0]))

        #ft = [t for t in set(list(idf[idf.Major==1]['URBAN_CODE'])) if t]
        #if len(ft)>0:
        #    row.setValue('I_URBANCODE',int(ft[0])) 
        
        #row.setValue('IFType',FindIntPG(Type_Major=type_major,Legs=legs,Signal=signal))
        
        uc.updateRow(row)   
    del uc
    del row
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.management.GetCount(Int))))
def CON_OverlayIntersections(WDir,HSMPY_PATH,IntInput,Routes,AttTab,year):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'OverlayInt_' + str(year) + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
IntInput = r'{}'
Routes = r'{}'
AttTab = r'{}'
year = {}

print("Overlay Intersections " + str(year))

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
hsmpy3.il.OverlayIntersections(IntInput,Routes,AttTab,year)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,IntInput,Routes,AttTab,year)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)

def JoinCrash_RouteAtt(Crash_CSV_In,Att_Tab,Crash_CSV_Out,year):
    print('[{}] Read Crash Data:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    df = pd.read_csv(Crash_CSV_In,index_col=0)
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape))
    
    print('[{}] Convert Crash Data to ArcGIS Table:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    GDB  = os.path.dirname(Att_Tab)
    C_N = common.CreateOutPath(MainFile=GDB + '\\CA_{}'.format(strftime("%Y%m%d%H%M%S")),Extension='',appendix=str(year))
    arcpy.management.CreateTable(out_name=os.path.basename(C_N),out_path=os.path.dirname(C_N))
    for f,t in zip(['CID','RID','MP'],['TEXT','TEXT','DOUBLE']):
        arcpy.management.AddField(in_table=C_N,field_name=f,field_type=t)
    ic = arcpy.InsertCursor(C_N)
    for i,r in df[~pd.isnull(df.INVENTORY)].iterrows():
        row = ic.newRow()
        row.setValue('RID',r.INVENTORY)
        row.setValue('MP',r.MP)
        row.setValue('CID',str(i))
        ic.insertRow(row)
    del ic
    del row
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.management.GetCount(C_N))))

    print('[{}] Overlay with Route Attributes:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    AttTab = Att_Tab
    OL_T = common.CreateOutPath(MainFile=GDB + '\\OL_{}'.format(strftime("%Y%m%d%H%M%S")),Extension='',appendix=str(year))
    arcpy.lr.OverlayRouteEvents(
            in_table                 = C_N,
            in_event_properties      = ' '.join(['RID','POINT','MP']), 
            overlay_table            = AttTab,
            overlay_event_properties = ' '.join(['RID','LINE','BMP','EMP']),
            overlay_type             = "INTERSECT", 
            out_table                = OL_T, 
            out_event_properties     = ' '.join(['RID','POINT','MP']),
            zero_length_events       = "ZERO", 
            in_fields                = "FIELDS", 
            build_index              = "INDEX"
    )    
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.management.GetCount(OL_T))))

    print('[{}] Read Overlay Results and Export:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    odf = common.FCtoDF(OL_T)
    odf = odf.drop_duplicates(subset=['CID'])
    odf.index = odf.CID
    odf.index = odf.index.astype(np.int64)
    odf = odf.drop(['CID','LENGTH','RID','MP'],axis=1)
    cdf = pd.concat([df,odf],axis=1)
    cdf['DATE'] = pd.to_datetime(cdf['DATE'])
    cdf.index.name = 'CID'
    cdf.to_csv(Crash_CSV_Out)
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),cdf.shape))
    
    arcpy.management.Delete(C_N)
    arcpy.management.Delete(OL_T)
    print('[{}] Done!'.format(strftime("%Y-%m-%d %H:%M:%S")))

def CON_JoinCrash_RouteAtt(WDir,HSMPY_PATH,Crash_CSV_In,Att_Tab,Crash_CSV_Out,year):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'JoinCrashAtt_' + str(year) + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Crash_CSV_In = r'{}'
Att_Tab = r'{}'
Crash_CSV_Out = r'{}'
year = {}

print("Join Crash Data and Roadway Data  " + str(year))

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
hsmpy3.il.JoinCrash_RouteAtt(Crash_CSV_In,Att_Tab,Crash_CSV_Out,year)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Crash_CSV_In,Att_Tab,Crash_CSV_Out,year)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)

def SLUR_from_TWAY_CALSS(v):
    try:
        s = {0:'SR',1:'SR',2:'SR',3:'LR',4:'SR',5:'SU',6:'SU',7:'SU',8:'LU',9:'SU',np.nan:'UNK'}[v]
        return({'SR':'State Rural','SU':'State Urban','LU':'Local Urban','LR':'Local Rural'}[s])
    except:
        pass
def SLUR_from_RoadwayJU(JUR_TYPE,URBAN):
    try:
        if JUR_TYPE in [1,2]:
            s1 = 'State'
        elif JUR_TYPE in [7]:
            s1 = 'Private'
        else:
            s1 = 'Local'    
        if URBAN == 0:
            s2 = 'Rural'
        else:
            s2 = 'Urban'
        return('{} {}'.format(s1,s2))
    except:
        pass






# CMF Calculations
def CMF_Calculation(SelectedRegion,BootSamples=1000):
    print(strftime("%Y-%m-%d %H:%M:%S"))    
    Project_DIR  = r'\\CHCFPP01\Proj\ILDOT\650511SAFETYPROGRAM\4_WorkData\WO19\HSIP_Tracking_Tool'
    Cleaned_Dir  = Project_DIR + '\\14.CleanedUp_Data'
    Const_Int  = Cleaned_Dir + '\\Cont_Int.shp'
    Const_Seg  = Cleaned_Dir + '\\Cont_Seg.shp'

    HSIP_DF = pd.read_csv  (Cleaned_Dir + '\\01.HSIP_Data.csv')
    HSIP_DF.index = HSIP_DF.HSIPID.astype(str)
    HSIP_DF.RuralOrUrban = HSIP_DF.RuralOrUrban.fillna('')
    HSIP_DF.FiscalYear = HSIP_DF.FiscalYear.fillna(-1).astype(int)

    Cont_DF = pd.read_csv(Cleaned_Dir + '\\03.Contracts_Data.csv',index_col=0)
    Cont_DF['ContNum'] = Cont_DF.index
    Pay_DF  = pd.read_csv(Cleaned_Dir + '\\05.Contract_PayItems.csv')
    Pay_DF.index = pd.MultiIndex.from_arrays([Pay_DF.ContNum,Pay_DF.PayItem])

    Cont_IRIS = pd.read_csv(Cleaned_Dir + '\\06.Contracts_IRIS_Crashes.csv')
    idx2 = pd.IntervalIndex.from_tuples([(bmp,emp) for bmp,emp in zip(Cont_IRIS.BEG_STA,Cont_IRIS.END_STA)],'left')
    Cont_IRIS.index = pd.MultiIndex.from_arrays([Cont_IRIS.RID,idx2,Cont_IRIS.YEAR],names = ['INVENTORY','Milepost','Year'])
    Cont_IRIS = Cont_IRIS.sort_index()
    Cont_IRIS.CID = Cont_IRIS.CID.fillna('')
    Cont_IRIS.CID = Cont_IRIS.CID.apply(lambda x:[int(i) for i in x.split(';') if len(i)>0])

    Cont_Crash_DF = pd.read_csv(Cleaned_Dir + '\\07.Contracts_Crashes.csv')
    Cont_Crash_DF.index = pd.MultiIndex.from_arrays([Cont_Crash_DF.ContNum,Cont_Crash_DF.Period,Cont_Crash_DF.CID])

    T_DF = pd.read_excel(Cleaned_Dir + '\\08.Contracts_Treatments.xlsx')
    T_DF.index = T_DF.ContNum

    Res_Ag_DF = pd.read_csv(Cleaned_Dir + '\\32.Reduction_Type_CV.csv',index_col=[0,1,2,3])
    Res_Ag_DF = Res_Ag_DF[(~pd.isnull(Res_Ag_DF.Reduction)) & (Res_Ag_DF.Num_Contracts>0) & (Res_Ag_DF['S.E.']>0)]
    Res_Ag_DF.insert(0, 'CMF_ID', range(1, 1 + len(Res_Ag_DF)))

    print('Total HSIP Applications: {}'.format(len(HSIP_DF.HSIPID.unique())))
    print('Total WPPS Contracts: {}'.format(len(Cont_DF.index.unique())))
    print('Total Geocoded Contracts: {}'.format(len(Cont_DF[Cont_DF.IsGeocoded=='Yes'].index.unique())))
    print('Total Int: {}, Seg: {}, Mileage: {:0.2f}'.format(len(Cont_DF[Cont_DF.NumInt>0].index.unique()),len(Cont_DF[Cont_DF.NumSeg>0].index.unique()),Cont_DF.SegMileage.sum()))
    print('Total Contracts with IRIS Data: {}'.format(len(Cont_IRIS.ContNum.unique())))
    print('Total Contracts with Crash Data: {}'.format(len(Cont_Crash_DF.ContNum.unique())))
    print('Total Crashes Before: {:,}, After: {:,}'.format(Cont_Crash_DF[Cont_Crash_DF.Period=='Before'].shape[0],Cont_Crash_DF[Cont_Crash_DF.Period=='After'].shape[0]))

    # Aggregated Results, Crash Type, Contracts, EAs, All at one

    def FillAgDF(idf,V,Cont_DF):
        S = pd.Series(index=['Num_Contracts','ListofContNums','NumIntSites','NumSegSites','Mileage',
                            'Before_Cont-Years','After_Cont-Years','BeforeCrashes','AfterCrashes','Reduction',
                            'S.E.','C.V.','Significance','Bootstraps'])
        a = idf.loc[idf.Period=='After','Total']
        b = idf.loc[idf.Period=='Before','Total']
        r = (a.sum()/a.count())/(b.sum()/b.count())
        cl = list(set([i[0] for i in idf.index]))
        S.loc['Num_Contracts']  = len(cl)
        S.loc['ListofContNums'] = ';'.join(cl)
        S.loc['NumIntSites'] = Cont_DF.loc[cl].NumInt.sum()
        S.loc['NumSegSites'] = Cont_DF.loc[cl].NumSeg.sum()
        S.loc['Mileage'    ] = Cont_DF.loc[cl].SegMileage.sum()
        S.loc['Before_Cont-Years'] = b.count()
        S.loc['After_Cont-Years' ] = a.count()
        S.loc['BeforeCrashes'] = b.sum()
        S.loc['AfterCrashes' ] = a.sum()
        S.loc['Reduction'   ] = (a.sum()/a.count())/(b.sum()/b.count())
        S.loc['S.E.'        ] = np.std(V)
        S.loc['C.V.'        ] = np.std(V)/r
        S.loc['Significance'] = 1-scipy.stats.norm(r,np.std(V)).cdf(1)
        S.loc['Bootstraps'  ] = len(V)
        return(S)
    def FilterRegions(DF,Filter):
        if Filter == 'Total':
            return(DF)
        elif 'District' in Filter:
            d = Filter[-1]
            L = Cont_DF.loc[Cont_DF.District.apply(lambda x:d in x)].index.tolist()
            return(DF.loc[L])
        elif 'Contract' in Filter:
            return(DF)
    def FilterTreatments(DF,Filter):
        if Filter == 'Total':
            return(DF)
        elif Filter in [i[0] for i in DF.index]:
            return(DF.loc[[Filter]])
        else:
            TrtGrp = Filter.split(';')
            df = T_DF
            T2L = list(T_DF.T2.unique())
            T3L = list(T_DF.T3.unique())
            for t in TrtGrp:
                if t in T2L:
                    df = df[df.ContNum.isin(df.loc[df.T2==t]['ContNum'])]
                if t in T3L:
                    df = df[df.ContNum.isin(df.loc[df.T3==t]['ContNum'])]
            L = df.ContNum.astype(str).tolist()
            return(DF.loc[L])
    def FilterCrashTypes(DF,Filter):
        if Filter == 'Total':
            return(DF[CTypes+['Period']])
        df = DF[[C for C in Filter.split(';')]+['Period']]
        #df['Period'] = DF['Period']
        return(df)
    def FilterCrashSeverity(DF,Filter):
        if Filter == 'Total':
            return(DF)
        L = list(set([i[0] for i in DF.columns.unique() if not i[0]=='Period']))
        return(DF[[(C,s) for C in L for s in list(Filter)]+[('Period','')]])

    def Bootstrap(DF,C,Bootstraps=10000):
        v = []
        unq_idx_s = pd.Series(list(set(DF.index)))
        for b in range(Bootstraps):
            s_idx = unq_idx_s.sample(n=unq_idx_s.count(),replace=True)
            smp = DF.loc[s_idx]
            A = smp.loc[smp.Period=='After',C].sum()/smp.loc[smp.Period=='After',C].count()
            B = smp.loc[smp.Period=='Before',C].sum()/smp.loc[smp.Period=='Before',C].count()
            v.append(A/B)
        return(v)
    def Bootstrap2(Before,After,Bootstraps=10000):
        v = []
        for b in range(Bootstraps):
            b_s = Before.sample(n=Before.count(),replace=True)
            a_s = After.sample(n=After.count(),replace=True)
            A = a_s.sum()/a_s.count()
            B = b_s.sum()/b_s.count()
            v.append(A/B)
        return(v)    

    RegionalFilters = ['Total'] + ['District{}'.format(i+1) for i in range(9)]
    TreatmentFilter = ['Total'] + list(T_DF.T2.unique()) + list(T_DF.T3.unique())

    CTypes = ['Angle', 'Animal', 'Fixed object', 'Head-on', 'Other non-collision', 'Other object', 'Overturned', 
            'Parked Motor vehicle', 'Pedalcyclist', 'Pedestrian', 'Rear-end', 'Sideswipe-opposite direction', 
            'Sideswipe-same direction', 'Train', 'Turning']
    EAs = ['EA_RD','EA_IM','EA_IN','EA_DF','EA_TN','EA_WZ','EA_SA','EA_OD','EA_YD','EA_HV','EA_MC','EA_UO','EA_PD','EA_PC']
    CTypeCombos = ['Fixed object;Head-on;Overturned;Sideswipe-opposite direction']

    CTypeFilters    = ['Total'] + CTypeCombos + CTypes + EAs
    SeverityFilters = ['KABCO','KABC','KAB','KA','K','A','B','C','O']

    Crash_Type_DF = pd.read_csv(Cleaned_Dir + '\\25.Cont_CrashTypeSeverity_EA_Crashes.csv',header=[0, 1],skiprows=[2],index_col=[0,1])
    Crash_Type_DF = Crash_Type_DF.rename(columns={x[0]:x[0].split('.')[-1].lstrip() for x in Crash_Type_DF.columns.tolist()})
    Crash_Type_DF[('Period','')] = Crash_Type_DF.Period
    Crash_Type_DF = Crash_Type_DF.drop(columns=[('Period','Unnamed: 146_level_1')])
    Crash_Type_DF = Crash_Type_DF.loc[:,pd.MultiIndex.from_product([CTypes+EAs,list('KABCO')]).append(pd.MultiIndex.from_tuples([('Period','')]))]

    ContFilters      = list(Crash_Type_DF.index.levels[0])

    #Res_BS_DF1 = pd.DataFrame(columns=pd.MultiIndex.from_product([RegionalFilters,TreatmentFilter,CTypeFilters,SeverityFilters]),
    #                        index=range(BootSamples))
    Res_Ag_DF1 = pd.DataFrame(columns=pd.MultiIndex.from_product([RegionalFilters,TreatmentFilter,CTypeFilters,SeverityFilters]),
                            index=['Num_Contracts','ListofContNums','NumIntSites','NumSegSites','Mileage',
                                    'Before_Cont-Years','After_Cont-Years','BeforeCrashes','AfterCrashes','Reduction',
                                    'S.E.','C.V.','Significance','Bootstraps'])

    #Res_BS_DF2 = pd.DataFrame(columns=pd.MultiIndex.from_product([['Contract'],ContFilters,CTypeFilters,SeverityFilters]),
    #                        index=range(BootSamples))
    Res_Ag_DF2 = pd.DataFrame(columns=pd.MultiIndex.from_product([['Contract'],ContFilters,CTypeFilters,SeverityFilters]),
                            index=['Num_Contracts','ListofContNums','NumIntSites','NumSegSites','Mileage',
                                    'Before_Cont-Years','After_Cont-Years','BeforeCrashes','AfterCrashes','Reduction',
                                    'S.E.','C.V.','Significance','Bootstraps'])

    Res_Ag_DF = pd.concat([Res_Ag_DF1,Res_Ag_DF2],axis=1)
    #Res_BS_DF = pd.concat([Res_BS_DF1,Res_BS_DF2],axis=1)
    print(Res_Ag_DF.shape)#,Res_BS_DF.shape)

    if SelectedRegion=='Total':
        Res_Ag_DF = Res_Ag_DF[['Total']]
        #Res_BS_DF = Res_BS_DF[['Total']]
        print('Total Filter applied',Res_Ag_DF.shape)
    if 'District' in SelectedRegion:
        Res_Ag_DF = Res_Ag_DF[[SelectedRegion]]
        #Res_BS_DF = Res_BS_DF[[SelectedRegion]]
        print('District Filter applied',Res_Ag_DF.shape)
    if SelectedRegion=='Contract':
        Res_Ag_DF = Res_Ag_DF[['Contract']]
        #Res_BS_DF = Res_BS_DF[['Contract']]
        print('Contract Filter applied',Res_Ag_DF.shape)

    product = 1  
    for x in [len(i) for i in Res_Ag_DF.columns.levels]:
        product *= x
    for RegionFilter in set([k[0] for k in Res_Ag_DF.columns]):
        print(RegionFilter)
        for TreatmentFilter in set([k[1] for k in Res_Ag_DF.columns]):
            print(TreatmentFilter)
            for CrashTypeFilter in set([k[2] for k in Res_Ag_DF.columns]):
                for CrashSeverityFilter in set([k[3] for k in Res_Ag_DF.columns]):
                    DF = FilterRegions(Crash_Type_DF,RegionFilter)
                    DF = FilterTreatments(DF,TreatmentFilter)
                    DF = FilterCrashTypes(DF,CrashTypeFilter)
                    DF = FilterCrashSeverity(DF,CrashSeverityFilter)
                    idf = pd.DataFrame(DF.sum(axis=1),columns=['Total'])
                    idf['Period'] = DF['Period']
                    if DF.shape[0]>0:
                        V = Bootstrap2(After=idf.loc[idf.Period=='After','Total'],Before=idf.loc[idf.Period=='Before','Total'],Bootstraps=BootSamples)
                        #Res_BS_DF[RegionFilter,TreatmentFilter,CrashTypeFilter,CrashSeverityFilter] = V
                        Res_Ag_DF[RegionFilter,TreatmentFilter,CrashTypeFilter,CrashSeverityFilter] = FillAgDF(idf,V,Cont_DF)


    Res_Ag_DF.T.to_csv(Cleaned_Dir + '\\34.Reduction_Cont_CV_{}.csv'.format(SelectedRegion))
    #Res_BS_DF.to_csv(Cleaned_Dir + '\\35.Reduction_Cont_BS_{}.csv'.format(SelectedRegion))
    print(strftime("%Y-%m-%d %H:%M:%S"))

def CON_CMF_Calculation(WDir,HSMPY_PATH,SelectedRegion,BootSamples=1000):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'CMF_' + str(SelectedRegion) + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
SelectedRegion = '{}'
BootSamples = {}

print("CMFs for " + str(SelectedRegion))

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
hsmpy3.il.CMF_Calculation(SelectedRegion,BootSamples)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,SelectedRegion,BootSamples)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)


def BC_Calculation(SelectedRegion,BootSamples=1000):
    print(strftime("%Y-%m-%d %H:%M:%S"))    
    Project_DIR  = r'\\CHCFPP01\Proj\ILDOT\650511SAFETYPROGRAM\4_WorkData\WO19\HSIP_Tracking_Tool'
    Cleaned_Dir  = Project_DIR + '\\14.CleanedUp_Data'
    Const_Int  = Cleaned_Dir + '\\Cont_Int.shp'
    Const_Seg  = Cleaned_Dir + '\\Cont_Seg.shp'

    HSIP_DF = pd.read_csv  (Cleaned_Dir + '\\01.HSIP_Data.csv')
    HSIP_DF.index = HSIP_DF.HSIPID.astype(str)
    HSIP_DF.RuralOrUrban = HSIP_DF.RuralOrUrban.fillna('')
    HSIP_DF.FiscalYear = HSIP_DF.FiscalYear.fillna(-1).astype(int)

    Cont_DF = pd.read_csv(Cleaned_Dir + '\\03.Contracts_Data.csv',index_col=0)
    Cont_DF['ContNum'] = Cont_DF.index
    Pay_DF  = pd.read_csv(Cleaned_Dir + '\\05.Contract_PayItems.csv')
    Pay_DF.index = pd.MultiIndex.from_arrays([Pay_DF.ContNum,Pay_DF.PayItem])

    Cont_IRIS = pd.read_csv(Cleaned_Dir + '\\06.Contracts_IRIS_Crashes.csv')
    idx2 = pd.IntervalIndex.from_tuples([(bmp,emp) for bmp,emp in zip(Cont_IRIS.BEG_STA,Cont_IRIS.END_STA)],'left')
    Cont_IRIS.index = pd.MultiIndex.from_arrays([Cont_IRIS.RID,idx2,Cont_IRIS.YEAR],names = ['INVENTORY','Milepost','Year'])
    Cont_IRIS = Cont_IRIS.sort_index()
    Cont_IRIS.CID = Cont_IRIS.CID.fillna('')
    Cont_IRIS.CID = Cont_IRIS.CID.apply(lambda x:[int(i) for i in x.split(';') if len(i)>0])

    Cont_Crash_DF = pd.read_csv(Cleaned_Dir + '\\07.Contracts_Crashes.csv')
    Cont_Crash_DF.index = pd.MultiIndex.from_arrays([Cont_Crash_DF.ContNum,Cont_Crash_DF.Period,Cont_Crash_DF.CID])

    T_DF = pd.read_excel(Cleaned_Dir + '\\08.Contracts_Treatments.xlsx')
    T_DF.index = T_DF.ContNum

    Res_Ag_DF = pd.read_csv(Cleaned_Dir + '\\32.Reduction_Type_CV.csv',index_col=[0,1,2,3])
    Res_Ag_DF = Res_Ag_DF[(~pd.isnull(Res_Ag_DF.Reduction)) & (Res_Ag_DF.Num_Contracts>0) & (Res_Ag_DF['S.E.']>0)]
    Res_Ag_DF.insert(0, 'CMF_ID', range(1, 1 + len(Res_Ag_DF)))

    BC_DF = pd.read_csv(Cleaned_Dir  + '\\51.BC_Results.csv',index_col=0)

    print('Total HSIP Applications: {}'.format(len(HSIP_DF.HSIPID.unique())))
    print('Total WPPS Contracts: {}'.format(len(Cont_DF.index.unique())))
    print('Total Geocoded Contracts: {}'.format(len(Cont_DF[Cont_DF.IsGeocoded=='Yes'].index.unique())))
    print('Total Int: {}, Seg: {}, Mileage: {:0.2f}'.format(len(Cont_DF[Cont_DF.NumInt>0].index.unique()),len(Cont_DF[Cont_DF.NumSeg>0].index.unique()),Cont_DF.SegMileage.sum()))
    print('Total Contracts with IRIS Data: {}'.format(len(Cont_IRIS.ContNum.unique())))
    print('Total Contracts with Crash Data: {}'.format(len(Cont_Crash_DF.ContNum.unique())))
    print('Total Crashes Before: {:,}, After: {:,}'.format(Cont_Crash_DF[Cont_Crash_DF.Period=='Before'].shape[0],Cont_Crash_DF[Cont_Crash_DF.Period=='After'].shape[0]))

    # Aggregated Results, Crash Type, Contracts, EAs, All at one

    def FillAgDF(idf,V,Cont_DF,cs_df):
    
        S = pd.Series(index=['Num_Contracts','ListofContNums','NumIntSites','NumSegSites','Mileage',
                                    'Before_Cont-Years','After_Cont-Years',
                                    'BeforeKCrashes','BeforeACrashes','BeforeBCrashes',
                                    'AfterKCrashes','AfterACrashes','AfterBCrashes',
                                    'Total_Cost','Total_Benefit','BC',
                                    'S.E.','C.V.','Significance','Bootstraps'])
        bc = idf.Benefit_Tot.sum()/idf.Cost_Tot.sum()
        cl = list(set([i for i in idf.index]))
        S.loc['Num_Contracts']  = len(cl)
        S.loc['ListofContNums'] = ';'.join(cl)
        S.loc['NumIntSites'] = Cont_DF.loc[cl].NumInt.sum()
        S.loc['NumSegSites'] = Cont_DF.loc[cl].NumSeg.sum()
        S.loc['Mileage'    ] = Cont_DF.loc[cl].SegMileage.sum()
        S.loc['Before_Cont-Years'] = cs_df.loc[cs_df.Period=='Before','K'].count()
        S.loc['After_Cont-Years' ] = cs_df.loc[cs_df.Period=='After','K'].count()
        S.loc['BeforeKCrashes'] = cs_df.loc[cs_df.Period=='Before','K'].sum()
        S.loc['BeforeACrashes'] = cs_df.loc[cs_df.Period=='Before','A'].sum()
        S.loc['BeforeBCrashes'] = cs_df.loc[cs_df.Period=='Before','B'].sum()
        S.loc['AfterKCrashes' ] = cs_df.loc[cs_df.Period=='After','K'].sum()
        S.loc['AfterACrashes' ] = cs_df.loc[cs_df.Period=='After','A'].sum()
        S.loc['AfterBCrashes' ] = cs_df.loc[cs_df.Period=='After','B'].sum()
        S.loc['Total_Cost'    ] = idf.Cost_Tot.sum()
        S.loc['Total_Benefit' ] = idf.Benefit_Tot.sum()
        S.loc['BC'          ] = bc
        S.loc['S.E.'        ] = np.std(V)
        S.loc['C.V.'        ] = np.std(V)/bc
        S.loc['Significance'] = scipy.stats.norm(bc,np.std(V)).cdf(1)
        S.loc['Bootstraps'  ] = len(V)
        return(S)
    def FilterRegions(DF,Filter):
        if Filter == 'Total':
            return(DF)
        elif 'District' in Filter:
            d = int(Filter[-1])
            return(DF[DF.District==d])
        elif 'Contract' in Filter:
            return(DF)
    def FilterTreatments(DF,Filter):
        if Filter == 'Total':
            return(DF)
        elif Filter in [i for i in DF.index]:
            return(DF.loc[[Filter]])
        else:
            TrtGrp = Filter.split(';')
            df = T_DF
            T2L = list(T_DF.T2.unique())
            T3L = list(T_DF.T3.unique())
            for t in TrtGrp:
                if t in T2L:
                    df = df[df.ContNum.isin(df.loc[df.T2==t]['ContNum'])]
                if t in T3L:
                    df = df[df.ContNum.isin(df.loc[df.T3==t]['ContNum'])]
            L = list(set(df.ContNum.astype(str).tolist()))
            idx = [i for i in DF.index] 
            L = [i for i in L if i in idx]
            return(DF.loc[L])
    def FilterTypes(DF,Filter):
        if Filter == 'Total':
            return(DF)
        return(DF[DF.Systemic==Filter])
    def FilterJurisdiction(DF,Filter):
        if Filter == 'Total':
            return(DF)
        return(DF[DF.StateLocal==Filter])

    def Bootstrap(DF,Bootstraps=10000):
        v = []
        unq_idx_s = pd.Series(list(set(DF.index)))
        for b in range(Bootstraps):
            s_idx = unq_idx_s.sample(n=unq_idx_s.count(),replace=True)
            smp = DF.loc[s_idx]
            v.append(smp.Benefit_Tot.sum()/smp.Cost_Tot.sum())
        return(v)

    RegionalFilters = ['Total'] + ['District{}'.format(i+1) for i in range(9)]
    JurFilter       = ['Total', 'State'  , 'Local']
    TypeFilter      = ['Total', 'Hotspot','Systemic']
    TreatmentFilter = ['Total'] + list(T_DF.T2.unique()) + list(T_DF.T3.unique())
    ContFilters      = list(BC_DF.index)

    #Res_BS_DF1 = pd.DataFrame(columns=pd.MultiIndex.from_product([RegionalFilters,TreatmentFilter,CTypeFilters,SeverityFilters]),
    #                        index=range(BootSamples))
    Res_Ag_DF1 = pd.DataFrame(columns=pd.MultiIndex.from_product([RegionalFilters,JurFilter,TypeFilter,TreatmentFilter]),
                            index=['Num_Contracts','ListofContNums','NumIntSites','NumSegSites','Mileage',
                                    'Before_Cont-Years','After_Cont-Years',
                                    'BeforeKCrashes','BeforeACrashes','BeforeBCrashes',
                                    'AfterKCrashes','AfterACrashes','AfterBCrashes',
                                    'Total_Cost','Total_Benefit','BC',
                                    'S.E.','C.V.','Significance','Bootstraps'])

    #Res_BS_DF2 = pd.DataFrame(columns=pd.MultiIndex.from_product([['Contract'],ContFilters,CTypeFilters,SeverityFilters]),
    #                        index=range(BootSamples))
    Res_Ag_DF2 = pd.DataFrame(columns=pd.MultiIndex.from_arrays([['Contract']*BC_DF.shape[0],BC_DF.StateLocal,BC_DF.Systemic,[i for i in BC_DF.index]]),
                            index=['Num_Contracts','ListofContNums','NumIntSites','NumSegSites','Mileage',
                                    'Before_Cont-Years','After_Cont-Years',
                                    'BeforeKCrashes','BeforeACrashes','BeforeBCrashes',
                                    'AfterKCrashes','AfterACrashes','AfterBCrashes',
                                    'Total_Cost','Total_Benefit','BC',
                                    'S.E.','C.V.','Significance','Bootstraps'])

    Res_Ag_DF = pd.concat([Res_Ag_DF1,Res_Ag_DF2],axis=1)
    #Res_BS_DF = pd.concat([Res_BS_DF1,Res_BS_DF2],axis=1)
    print(Res_Ag_DF.shape)#,Res_BS_DF.shape)
    CS_DF = pd.read_csv(Cleaned_Dir + '\\21.Cont_CrashSeverity_Year_Crashes.csv',index_col=0)

    print(SelectedRegion)
    if SelectedRegion=='Total':
        Res_Ag_DF = Res_Ag_DF[['Total']]
        #Res_BS_DF = Res_BS_DF[['Total']]
        print('Total Filter applied',Res_Ag_DF.shape)
    if 'District' in SelectedRegion:
        Res_Ag_DF = Res_Ag_DF[[SelectedRegion]]
        #Res_BS_DF = Res_BS_DF[[SelectedRegion]]
        print('District Filter applied',Res_Ag_DF.shape)
    if SelectedRegion=='Contract':
        Res_Ag_DF = Res_Ag_DF[['Contract']]
        #Res_BS_DF = Res_BS_DF[['Contract']]
        print('Contract Filter applied',Res_Ag_DF.shape)

    for i,r in Res_Ag_DF.T.iterrows():
        RegionFilter = i[0]
        JurFilter  = i[1]
        TypeFilter = i[2]
        TreatmentFilter = i[3]
        DF = FilterRegions(BC_DF,RegionFilter)
        DF = FilterJurisdiction(DF,JurFilter)
        DF = FilterTypes(DF,TypeFilter)
        DF = FilterTreatments(DF,TreatmentFilter)
        if DF.shape[0]>0:
            print(RegionFilter,JurFilter,TypeFilter,TreatmentFilter,DF.shape[0])
            V = Bootstrap(DF,Bootstraps=BootSamples)
            Res_Ag_DF[RegionFilter,JurFilter,TypeFilter,TreatmentFilter] = FillAgDF(DF,V,Cont_DF,CS_DF.loc[DF.index])

    Res_Ag_DF.T.to_csv(Cleaned_Dir + '\\53.BC_Cont_CV_{}.csv'.format(SelectedRegion))
    print(strftime("%Y-%m-%d %H:%M:%S"))

def CON_BC_Calculation(WDir,HSMPY_PATH,SelectedRegion,BootSamples=1000):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'BC_{}.py'.format(SelectedRegion))
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
BootSamples = {}
SelectedRegion = '{}'
print("BC Calculations")

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
hsmpy3.il.BC_Calculation(SelectedRegion,BootSamples)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,BootSamples,SelectedRegion)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)



def PlotTreatmentCMFs(CMF_DF,TreatmentFilter,CrashTypeFilter,SeverityFilter,FN,Title,TX_DF):
    from numpy import ma
    import matplotlib
    from matplotlib import colors as mcolors
    from matplotlib import cbook
    from matplotlib.colors import Normalize
    from matplotlib.colors import LinearSegmentedColormap
    import matplotlib.patches as patches
    from mpl_toolkits.axes_grid1 import make_axes_locatable    
    import matplotlib.colors as mcolors
    Aspect = 'equal'
    CMF_DF['Sev'] = [i[3] for i in CMF_DF.index]
    CMF_DF['ty'] = [i[2] for i in CMF_DF.index]
    CMF_DF['Tr'] = [i[1] for i in CMF_DF.index]
    idf = CMF_DF[(CMF_DF.Tr==TreatmentFilter) & (CMF_DF.Sev.isin(SeverityFilter)) & (CMF_DF.ty.isin(CrashTypeFilter))]
    sdf = idf['Significance']
    sdf.index = sdf.index.droplevel([0,1])
    sdf = pd.DataFrame(sdf)
    sdf = sdf.unstack()
    sdf.columns = sdf.columns.droplevel(0)
    idx0 = sdf.index.tolist()
    idx1 = SeverityFilter
    idx0.pop(idx0.index('Total'))
    sdf = sdf.loc[idx0+['Total']][idx1]
    sdf = sdf.T
    
    rdf = idf['Reduction']
    rdf.index = rdf.index.droplevel([0,1])
    rdf = pd.DataFrame(rdf)
    df = rdf.unstack()
    df.columns = df.columns.droplevel(0)
    idx0 = df.index.tolist()
    idx1 = SeverityFilter
    idx0.pop(idx0.index('Total'))
    df = df.loc[idx0+['Total']][idx1]
    df = df.T
    df = df.rename(columns={i:getattr(hsmpy3.il.domains,i)['alias'] for i in ['EA_RD','EA_IM','EA_IN','EA_TN','EA_SA','EA_OD','EA_YD','EA_HV','EA_MC','EA_UO','EA_PD','EA_PC']})
    x = df.shape[0]
    y = df.shape[1]
    FigSize = (10,10)
    #if x>y:
    #    FigSize = (8.0*x/y,10)
        
        
    plt.figure(figsize=FigSize)
    plt.plot()
    plt.gca().set_aspect(Aspect)
    plt.gca().set_xlim((-0.5,df.shape[1]-0.5))
    plt.gca().set_ylim((-0.5,df.shape[0]-0.5))
    plt.xticks(range(df.shape[1]),df.columns,rotation=90)
    plt.yticks(range(df.shape[0]),df.index,rotation=0)
    
    offset = .1
    a = offset/(1-offset)
    b = 1/(1-offset)
    def DrawConfPatch(x,y,cmf,pvalue):
        if cmf<=1:
            pvalue = 1-pvalue
            COL = plt.cm.Greens_r(cmf/b)
        if cmf>1:
            COL = plt.cm.Reds(1-1/(cmf+a))
        CI_ranges = [(1,0.95),(0.95,0.90),(0.90,0.8)]
        FillCol   = [plt.cm.Greys_r(i) for i in np.linspace(0,0.5,len(CI_ranges))]
        FillCol   = ['none' for i in np.linspace(0,0.5,len(CI_ranges))]
        FillSize  = np.linspace(0.5,0.15,len(CI_ranges))
        for ci,c,o in zip(CI_ranges,FillCol,FillSize):
            if pvalue>=ci[1] and pvalue<ci[0]:
                rect = patches.Rectangle((y-o,x-o),o*2,o*2,linewidth=1,edgecolor=c,facecolor=COL)
                plt.gca().add_patch(rect)    
                plt.text(s='{:.2f}\n({:.0f}%)'.format(cmf,pvalue*100),x=j,y=i,horizontalalignment='center',verticalalignment='center')
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if not pd.isnull(df.iloc[i,j]):
                DrawConfPatch(i,j,df.iloc[i,j],sdf.iloc[i,j])
    plt.grid()
    colors1 = plt.cm.Greens_r(np.linspace(0.1/b,1-offset, 1000))
    colors2 = plt.cm.Reds(np.linspace(offset,1-1/(10+a), 1000))
    mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', np.vstack((colors1, colors2)))
    #matplotlib.colorbar.ColorbarBase(plt.gca(), cmap=mymap, orientation = 'vertical')
    
    lw = 2
    rect = patches.Rectangle((y+lw/100-1.5,-0.5+lw/100),1-2*lw/100,x-lw/100,linewidth=lw/2,edgecolor='blue',facecolor='none')
    plt.gca().add_patch(rect)    
    rect = patches.Rectangle((-0.5+lw/100,x+lw/100-1.5),y-2*lw/100,1-2*lw/100,linewidth=lw/2,edgecolor='blue',facecolor='none')
    plt.gca().add_patch(rect)    
    plt.title(Title)


    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("right", size="5%", pad=0.05)
    
    sm = plt.cm.ScalarMappable(cmap=mymap)
    sm.set_array([])
    cbar = plt.colorbar(sm,orientation='vertical',cax=cax)
    t1 = np.linspace(0,0.5,5)
    l1 = np.linspace(0.1,1,5)
    t2 = np.linspace(0.5,1,5)
    l2 = 1/np.linspace(1,.1,5)
    t = list(t1)[:-1]+list(t2)
    l = list(l1)[:-1]+list(l2)
    cbar.set_ticks(t)
    cbar.set_ticklabels(np.round(l,2))
    cbar.ax.set_ylabel('CMF Color Map', rotation=270)
    idf.index = idf.index.droplevel([0,1])
    t = ''
    t +=  '{:>30s} {:<,.0f}\n'.format('Number of Contracts:', idf.Num_Contracts.iloc[0])
    if idf.Mileage.iloc[0]>0:
        t +=  '{:>30s} {:<,.2f}\n'.format('Mileage:', idf.Mileage.iloc[0])
    if idf.NumIntSites.iloc[0]>0:
        t +=  '{:>30s} {:<7,.0f}\n'.format('Number of Intersections:', idf.NumIntSites.iloc[0])
    t += '\n'
    t +=  '{:>30s} {:<7,.2f}\n'.format('Average Before Years:', idf['Before_Cont-Years'].iloc[0]/idf.Num_Contracts.iloc[0])
    t +=  '{:>30s} {:<7,.2f}\n'.format('Average After Years:', idf['After_Cont-Years'].iloc[0]/idf.Num_Contracts.iloc[0])
    t += '\n'
    t += '{:>30s}\n'.format('Total Number of Crashes by Period')
    t +=  '{:>6s}{:>9s} {:>14s}\n'.format('Severity','Before','After')
    for sev in ['K','A','B','C','O']:
        n = idf.loc[('Total',sev),'BeforeCrashes']
        m = idf.loc[('Total',sev),'AfterCrashes']
        t += '{:>6s}:       {:>7,.0f}          {:>7,.0f}\n'.format(sev,n,m)
    
    #plt.gca().text(-19,0.35,t)
    
    t += '\n'
    tdf = TX_DF[(TX_DF.Treatment2==TreatmentFilter) & (TX_DF.NumberOfContracts>0)].sort_values('NumberOfContracts',ascending=False)[['Treatment2_X','NumberOfContracts']].iloc[1:6]
    n = min(tdf.shape[0],5)
    if tdf.shape[0]>0:
        t += '{:<80s}\n'.format('Top {} Overlapping Treatments:'.format(n))
        for i,r in tdf.iterrows():
            t += '{:<80s}\n'.format('{} ({})'.format(r.Treatment2_X[0:40],r.NumberOfContracts))
    plt.gca().text(+3,0.1,t,color='blue')
    
    plt.tight_layout()
    plt.savefig(FN,dpi=1200,transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()
class MidPointNorm(Normalize):    

    def __init__(self, midpoint=0, vmin=None, vmax=None, clip=False):
        Normalize.__init__(self,vmin, vmax, clip)
        self.midpoint = midpoint

    def __call__(self, value, clip=None):
        if clip is None:
            clip = self.clip

        result, is_scalar = self.process_value(value)

        self.autoscale_None(result)
        vmin, vmax, midpoint = self.vmin, self.vmax, self.midpoint

        if not (vmin < midpoint < vmax):
            print(vmin,vmax)
            raise ValueError("midpoint must be between maxvalue and minvalue.")       
        elif vmin == vmax:
            result.fill(0) # Or should it be all masked? Or 0.5?
        elif vmin > vmax:
            raise ValueError("maxvalue must be bigger than minvalue")
        else:
            vmin = float(vmin)
            vmax = float(vmax)
            if clip:
                mask = ma.getmask(result)
                result = ma.array(np.clip(result.filled(vmax), vmin, vmax),
                                  mask=mask)

            # ma division is very slow; we can take a shortcut
            resdat = result.data

            #First scale to -1 to 1 range, than to from 0 to 1.
            resdat -= midpoint            
            resdat[resdat>0] /= abs(vmax - midpoint)            
            resdat[resdat<0] /= abs(vmin - midpoint)

            resdat /= 2.
            resdat += 0.5
            result = ma.array(resdat, mask=result.mask, copy=False)                

        if is_scalar:
            result = result[0]            
        return result

    def inverse(self, value):
        if not self.scaled():
            raise ValueError("Not invertible until scaled")
        vmin, vmax, midpoint = self.vmin, self.vmax, self.midpoint

        if cbook.iterable(value):
            val = ma.asarray(value)
            val = 2 * (val-0.5)  
            val[val>0]  *= abs(vmax - midpoint)
            val[val<0] *= abs(vmin - midpoint)
            val += midpoint
            return val
        else:
            val = 2 * (val - 0.5)
            if val < 0: 
                return  val*abs(vmin-midpoint) + midpoint
            else:
                return  val*abs(vmax-midpoint) + midpoint
def PlotBCs(BC_DF,TreatmentTypeFilter,FN='test.png',Title=''):
    import matplotlib.colors as mcolors
    Aspect = 'equal'
    Xdf = BC_DF[['Significance','BC']]
    Xdf.Significance = Xdf.apply(lambda row:row.Significance if row.BC<1 else 1-row.Significance,axis=1)
    Xdf = Xdf[Xdf.Significance>=0.8]
    TreatmentTypeFilter = [i for i in TreatmentTypeFilter if i in list(Xdf['Significance'].unstack().columns) + ['Total']]
    
    sdf = Xdf['Significance'].unstack()[TreatmentTypeFilter]
    sdf.index = [' '.join(i) for i in sdf.index]
    sdf.index.name = 'Jurisdiction/Type'
    sdf.columns.name = 'Significance'
    idx1 = sdf.columns.tolist()
    idx1.pop(idx1.index('Total'))
    sdf = sdf[idx1+['Total']]
    

    df = Xdf['BC'].unstack()[TreatmentTypeFilter]
    df.index = [' '.join(i) for i in df.index]
    df.index.name = 'Jurisdiction/Type'
    df.columns.name = 'BC'
    
    df = df.rename(columns={'Add/Upgrade Signal Head/Mast Arm (LED, Backplate, per Lane)':'Add/Upgrade Signal Head/Mast Arm \n(LED, Backplate, per Lane)'})
    df = df.rename(columns={'Convert Protecetd/Permissive to Protected Only':'Convert Protecetd/Permissive\n to Protected Only'})
    df = df.rename(columns={'Time-Limited On-Street Parking Restrictions':'Time-Limited On-Street\nParking Restrictions'})
    df = df.rename(columns={'Advance Intersection Signs (with Flashers)':'Advance Intersection Signs\n(with Flashers)'})
    df = df.rename(columns={'WWD Improvements: Signing and Striping':'WWD Improvements:\nSigning and Striping'})
    df = df.rename(columns={'Upgrade Signs to conform with MUTCD':'Upgrade Signs to conform\nwith MUTCD'})
    
    idx1 = df.columns.tolist()
    idx1.pop(idx1.index('Total'))
    df = df[idx1+['Total']]
    df = df.T.rename(columns={i:getattr(hsmpy3.il.domains,i)['alias'] for i in ['EA_RD','EA_IM','EA_IN','EA_TN','EA_SA','EA_OD','EA_YD','EA_HV','EA_MC','EA_UO','EA_PD','EA_PC']}).T

    x = df.shape[1]
    y = df.shape[0]
    FigSize = (10,10)
    #if x>y:
    #    FigSize = (8.0*x/y,10)
    
    plt.figure(figsize=FigSize)
    plt.plot()
    plt.gca().set_aspect(Aspect)
    plt.gca().set_xlim((-0.5,df.shape[1]-0.5))
    plt.gca().set_ylim((-0.5,df.shape[0]-0.5))
    plt.xticks(range(df.shape[1]),df.columns,rotation=90)
    plt.yticks(range(df.shape[0]),df.index,rotation=0)
    
    MinBC = -150
    MaxBC = 950
    MinBC = df.min().min()
    MaxBC = np.log10(df.max().max())+1
    MinBC = -150
    MaxBC = np.log10(1000)+1
    offset = .1
    plt.grid()

    n = MidPointNorm(midpoint=1,vmax=MaxBC,vmin=MinBC)
    colors1 = plt.cm.Greens(np.linspace(offset,1, 1000))
    colors2 = plt.cm.Reds_r(np.linspace(offset,1, 1000))
    mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', np.vstack((colors2, colors1)))
    
    def DrawConfPatch(x,y,cmf,pvalue):
        if cmf>=1:
            #pvalue = 1-pvalue
            COL = mymap(n(np.log10(cmf)+1))
        if cmf<1:
            COL = mymap(n(cmf))
        CI_ranges = [(1,0.95),(0.95,0.90),(0.90,0.8)]
        FillCol   = [plt.cm.Greys_r(i) for i in np.linspace(0,0.5,len(CI_ranges))]
        FillCol   = ['none' for i in np.linspace(0,0.5,len(CI_ranges))]
        FillSize  = np.linspace(0.5,0.15,len(CI_ranges))
        for ci,c,o in zip(CI_ranges,FillCol,FillSize):
            
            if pvalue>=ci[1] and pvalue<ci[0]:
                rect = patches.Rectangle((y-o,x-o),o*2,o*2,linewidth=1,edgecolor=c,facecolor=COL)
                plt.gca().add_patch(rect)    
                        #plt.text(s='{:.0f}%'.format(sdf.iloc[i,j]*100),x=j,y=i,horizontalalignment='center',verticalalignment='center')
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if not pd.isnull(df.iloc[i,j]):
                #print(i,j,df.iloc[i,j],sdf.iloc[i,j])
                DrawConfPatch(i,j,df.iloc[i,j],sdf.iloc[i,j])
    
    lw = 2
    rect = patches.Rectangle((-0.5+lw/100,-0.5+lw/100),x-2*lw/100,3,linewidth=lw/2,edgecolor='blue',facecolor='none')
    plt.gca().add_patch(rect)    
    rect = patches.Rectangle((-0.5+lw/100,2.5),x-2*lw/100,3,linewidth=lw/2,edgecolor='blue',facecolor='none')
    plt.gca().add_patch(rect)    
    rect = patches.Rectangle((-0.5+lw/100,5.5),x-2*lw/100,3-lw/100,linewidth=lw/2,edgecolor='blue',facecolor='none')
    plt.gca().add_patch(rect)    
    rect = patches.Rectangle((x+lw/100-1.5,-0.5+lw/100),1-2*lw/100,9-lw/100,linewidth=lw/2,edgecolor='blue',facecolor='none')
    plt.gca().add_patch(rect)    
    plt.title(Title)

    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("right", size="5%", pad=0.05)

    sm = plt.cm.ScalarMappable(cmap=mymap)
    sm.set_array([])
    cbar = plt.colorbar(sm,orientation='vertical',cax=cax)
    t = list(np.linspace(MinBC,1,6))[:-1] + list(np.linspace(1,MaxBC,5))
    l = np.round(list(np.linspace(MinBC,1,6))[:-1] + list(np.logspace(0,MaxBC-1,5)),2)
    cbar.set_ticks([n(i) for i in t])
    cbar.set_ticklabels(l)
    cbar.ax.set_ylabel('BC Color Map', rotation=270)
    
    plt.tight_layout()
    plt.savefig(FN,dpi=1200,transparent=True,bbox_inches='tight', pad_inches=0)
    plt.close()
def PlotCMFs(CMF_DF,TreatmentFilter,CrashTypeFilter,SeverityFilter='KAB',CVFilter=100,SignificanceFilter=0.5,Min_Crash=1,FN='test.png',Title=''):
    import matplotlib.colors as mcolors
    Aspect = 'equal'
    CMF_DF['Sev'] = [i[3] for i in CMF_DF.index]
    CMF_DF['ty'] = [i[2] for i in CMF_DF.index]
    CMF_DF['Tr'] = [i[1] for i in CMF_DF.index]
    idf = CMF_DF[(CMF_DF['C.V.']<CVFilter) & 
                 (CMF_DF.Sev==SeverityFilter) & 
                 (CMF_DF.ty.isin(CrashTypeFilter)) & 
                 (CMF_DF.Tr.isin(TreatmentFilter)) &
                 ((CMF_DF.Significance<=SignificanceFilter) | (CMF_DF.Significance>=(1-SignificanceFilter))) &
                 (CMF_DF.BeforeCrashes>=Min_Crash) &
                 (CMF_DF.AfterCrashes>=Min_Crash)]
    sdf = idf['Significance']
    sdf.index = sdf.index.droplevel([0,3])
    sdf = pd.DataFrame(sdf)
    sdf = sdf.unstack()
    sdf.columns = sdf.columns.droplevel(0)
    idx0 = sdf.index.tolist()
    idx1 = sdf.columns.tolist()
    idx0.pop(idx0.index('Total'))
    idx1.pop(idx1.index('Total'))
    sdf = sdf.loc[idx0+['Total']][idx1+['Total']]
    sdf = sdf.T
    
    
    idf = idf['Reduction']
    idf.index = idf.index.droplevel([0,3])
    idf = pd.DataFrame(idf)
    df = idf.unstack()
    df.columns = df.columns.droplevel(0)
    df = df.rename(index={'Add/Upgrade Signal Head/Mast Arm (LED, Backplate, per Lane)':'Add/Upgrade Signal Head/Mast Arm \n(LED, Backplate, per Lane)'})
    df = df.rename(index={'Convert Protecetd/Permissive to Protected Only':'Convert Protecetd/Permissive\n to Protected Only'})
    df = df.rename(index={'Time-Limited On-Street Parking Restrictions':'Time-Limited On-Street\nParking Restrictions'})
    df = df.rename(index={'Advance Intersection Signs (with Flashers)':'Advance Intersection Signs\n(with Flashers)'})
    df = df.rename(index={'WWD Improvements: Signing and Striping':'WWD Improvements:\nSigning and Striping'})
    df = df.rename(index={'Upgrade Signs to conform with MUTCD':'Upgrade Signs to conform\nwith MUTCD'})
    
    
    idx0 = df.index.tolist()
    idx1 = df.columns.tolist()
    idx0.pop(idx0.index('Total'))
    idx1.pop(idx1.index('Total'))
    df = df.loc[idx0+['Total']][idx1+['Total']]
    df = df.T
    df = df.rename(columns={i:getattr(hsmpy3.il.domains,i)['alias'] for i in ['EA_RD','EA_IM','EA_IN','EA_TN','EA_SA','EA_OD','EA_YD','EA_HV','EA_MC','EA_UO','EA_PD','EA_PC']})
    x = df.shape[1]
    y = df.shape[0]
    FigSize = (10,10)
    #if x>y:
    #    FigSize = (8.0*x/y,10)
        
        
    plt.figure(figsize=FigSize)
    plt.plot()
    plt.gca().set_aspect(Aspect)
    plt.gca().set_xlim((-0.5,df.shape[1]-0.5))
    plt.gca().set_ylim((-0.5,df.shape[0]-0.5))
    plt.xticks(range(df.shape[1]),df.columns,rotation=90)
    plt.yticks(range(df.shape[0]),df.index,rotation=0)
    
    offset = .1
    a = offset/(1-offset)
    b = 1/(1-offset)
    def DrawConfPatch(x,y,cmf,pvalue):
        if cmf<=1:
            pvalue = 1-pvalue
            COL = plt.cm.Greens_r(cmf/b)
        if cmf>1:
            COL = plt.cm.Reds(1-1/(cmf+a))
        CI_ranges = [(1,0.95),(0.95,0.90),(0.90,0.8)]
        FillCol   = [plt.cm.Greys_r(i) for i in np.linspace(0,0.5,len(CI_ranges))]
        FillCol   = ['none' for i in np.linspace(0,0.5,len(CI_ranges))]
        FillSize  = np.linspace(0.5,0.15,len(CI_ranges))
        for ci,c,o in zip(CI_ranges,FillCol,FillSize):
            if pvalue>=ci[1] and pvalue<ci[0]:
                rect = patches.Rectangle((y-o,x-o),o*2,o*2,linewidth=1,edgecolor=c,facecolor=COL)
                plt.gca().add_patch(rect)    
                        #plt.text(s='{:.0f}%'.format(sdf.iloc[i,j]*100),x=j,y=i,horizontalalignment='center',verticalalignment='center')
    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if not pd.isnull(df.iloc[i,j]):
                DrawConfPatch(i,j,df.iloc[i,j],sdf.iloc[i,j])
    plt.grid()
    colors1 = plt.cm.Greens_r(np.linspace(0.1/b,1-offset, 1000))
    colors2 = plt.cm.Reds(np.linspace(offset,1-1/(10+a), 1000))
    mymap = mcolors.LinearSegmentedColormap.from_list('my_colormap', np.vstack((colors1, colors2)))
    #matplotlib.colorbar.ColorbarBase(plt.gca(), cmap=mymap, orientation = 'vertical')
    
    lw = 2
    rect = patches.Rectangle((x+lw/100-1.5,-0.5+lw/100),1-2*lw/100,y-lw/100,linewidth=lw/2,edgecolor='blue',facecolor='none')
    plt.gca().add_patch(rect)    
    rect = patches.Rectangle((-0.5+lw/100,y+lw/100-1.5),x-2*lw/100,1-2*lw/100,linewidth=lw/2,edgecolor='blue',facecolor='none')
    plt.gca().add_patch(rect)    
    plt.title(Title)


    divider = make_axes_locatable(plt.gca())
    cax = divider.append_axes("right", size="5%", pad=0.05)
    
    sm = plt.cm.ScalarMappable(cmap=mymap)
    sm.set_array([])
    cbar = plt.colorbar(sm,orientation='vertical',cax=cax)
    t1 = np.linspace(0,0.5,5)
    l1 = np.linspace(0.1,1,5)
    t2 = np.linspace(0.5,1,5)
    l2 = 1/np.linspace(1,.1,5)
    t = list(t1)[:-1]+list(t2)
    l = list(l1)[:-1]+list(l2)
    cbar.set_ticks(t)
    cbar.set_ticklabels(np.round(l,2))
    cbar.ax.set_ylabel('CMF Color Map', rotation=270)
    
    plt.tight_layout()
    plt.savefig(FN,dpi=1200,transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()