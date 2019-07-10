#HSMPY3
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
import hsmpy3.il as il
import matplotlib.pyplot as plt
from time import gmtime, strftime

NAD83_NM = arcpy.SpatialReference(6529)
UTM13N    = arcpy.SpatialReference(26913)


class domains(object):
    ACC_CNTL = {'name':'ACC_CNTL'   ,'alias':'Access Control'               ,'type':'SHORT','codes':{0:'Uncontrolled',
                1:'Partial control',
                2:'Full control'}}
    F_SYSTEM = {'name':'F_SYSTEM'   ,'alias':'Functional Class'               ,'type':'SHORT','codes':{
                1: 'Interstate',
                2: 'Principal Arterial – Other Freeways and Expressways',
                3: 'Principal Arterial – Other',
                4: 'Minor Arterial',
                5: 'Major Collector',
                6: 'Minor Collector',
                7: 'Local'}}

FACILITY_TYPE = {'name':'FACILITY_TYPE'   ,'alias':'Facility Type'               ,'type':'SHORT','codes':{
                1: 'One-Way Roadway',
                2: 'Two-Way Roadway',
                4: 'Ramp',
                5: 'Non Mainline',
                6: 'Non Inventory Direction',
                7: 'Planned/Unbuilt'
                }}

Median_Type = {'name':'Median_Type'   ,'alias':'Median Type'               ,'type':'SHORT','codes':{
                1: 'None',
                2: 'Unprotected',
                3: 'Curbed',
                4: 'Positive Barrier'
                }}
Ownership = {'name':'Ownership'   ,'alias':'Ownership'               ,'type':'SHORT','codes':{
                0:'Not Provided',
                1:'State Highway Agency',
                2:'County Highway Agency',
                4:'City or Municipality Agency',
                26:'Private (Other than Railroad)',
                50:'Indian Tribe Nation',
                60:'Other Federal Agency',
                62:'Bureau of Indian Affairs',
                64:'US Forest Services',
                74:'Army',
                80:'Other'
}}
def ConvToFloat(value):
    try:
        out = float(value)
    except:
        out = 0.0
    return(out)
def ConvToInt(value):
    try:
        out = int(value)
    except:
        out = 0
    return(out)
def FindKABCO(K=0,A=0,B=0,C=0):
    if K>0:
        s = 'K'
    else:
        if A > 0:
            s = 'A'
        else:
            if B>0:
                s = 'B'
            else:
                if C>0:
                    s = 'C'
                else:
                    s = 'O'
    return(s)
def FindDate(d,t):
    if str(t) in ['9999','9998' ,'00:00','24:00']:
        t = '00:00'
    return(datetime.strptime(d + ' ' + str(t), '%m/%d/%Y %H:%M'))
def LR_Overlay(Tab1,Tab2,Output):
    arcpy.lr.OverlayRouteEvents(
        in_table                 = Tab1,
        in_event_properties      = ' '.join([RouteID,'LINE',BEG_STA,END_STA]), 
        overlay_table            = Tab2, 
        overlay_event_properties = ' '.join([RouteID,'LINE',BEG_STA,END_STA]),
        overlay_type             = "UNION", 
        out_table                = Output, 
        out_event_properties     = ' '.join([RouteID,'LINE',BEG_STA,END_STA]),
        zero_length_events       = "ZERO", 
        in_fields                = "FIELDS", 
        build_index              = "INDEX"
    )
def FindFType(RID,F_SYSTEM,FACILITY_TYPE,THROUGH_LANES,URBAN_CODE,MEDIAN_TYPE):
    if FACILITY_TYPE==2 and THROUGH_LANES>0:
        S1 = 'U'
        if URBAN_CODE in [99999,0]:
            S1 = 'R'

        S2 = str(int(THROUGH_LANES))
        if THROUGH_LANES in [3,5,7,9] and F_SYSTEM == 1:
            S2 = str(int(THROUGH_LANES-1))

        S3 = 'U'
        if MEDIAN_TYPE in [2,3,4,5,6,7]:
            S3 = 'D'
        if F_SYSTEM in [1,2]:
            S3 = 'F'
        if F_SYSTEM == 7:
            S3 = 'L'
        return (S1+S2+S3)
    else:
        if 'X' in RID:
            return('Ramp')
        return('')
def GeocodeCrashes(Src_Loc,Src_Unit,Src_Occ,OutputDict,Years):
    loc_DF = pd.read_csv(Src_Loc,low_memory=False)
    loc_DF['Date' ] = [FindDate (r.CrashDate,r.MilitaryTime) for i,r in loc_DF.iterrows()]
    loc_DF['KABCO'] = [FindKABCO(r.Killed,r.ClassA,r.ClassB,r.ClassC) for i,r in loc_DF.iterrows()]
    loc_DF.index = loc_DF.UCRnumber

    Occ_DF = pd.read_csv(Src_Occ)
    Occ_DF['Ped_K'] = 0
    Occ_DF['Ped_A'] = 0
    Occ_DF['Ped_B'] = 0
    for i,r in Occ_DF.iterrows():
        if r.TypeV==7:
            if r.Injury=='K':
                Occ_DF.set_value(i,'Ped_K',1)
            if r.Injury=='A':
                Occ_DF.set_value(i,'Ped_A',1)
            if r.Injury=='B':
                Occ_DF.set_value(i,'Ped_B',1)

    #Fields = ['Date','GIS_UTMX','GIS_UTMY','GIS_NATAMER_USCENSUS','Class','Analysis','CrashOccurrence','HitRun','Light','Weather',
    #          'RoadCharacter','RoadGrade','Killed','ClassA','ClassB','ClassC','nVeh','TopCFacc','Alcinv','Druginv','PEDinv','MCinv',
    #          'PECinv','TRKinv','KABCO','Severity','GIS_Route']
    #loc_DF = loc_DF[Fields]

    CrashDict = {}
    for year in Years:
        CrashDict.update({year:loc_DF[[(r.Date.year == year) for i,r in loc_DF.iterrows()]]})
        #N = common.CreateOutPath(MainFile=Project_GDB+'\\Crash',appendix=str(year),Extension='')
        N = OutputDict[year]
        try:
            arcpy.management.Delete(N)
        except:pass
        arcpy.management.CreateFeatureclass(out_name = os.path.basename(N),
                                        out_path = os.path.dirname(N),
                                        spatial_reference=NAD83_NM,
                                        geometry_type='POINT',
                                        has_m='ENABLED',
                                        has_z='DISABLED')
        arcpy.AddField_management(N,'UCRnum','Text')
        arcpy.AddField_management(N,'GIS_Route','Text')
        arcpy.AddField_management(N,'Date','Date')
        arcpy.AddField_management(N,'KABCO','Text')
        arcpy.AddField_management(N,'Killed','Short')
        arcpy.AddField_management(N,'ClassA','Short')
        arcpy.AddField_management(N,'ClassB','Short')
        #arcpy.AddField_management(N,'PedInv','Short')
        #arcpy.AddField_management(N,'Severity','Text')
        arcpy.AddField_management(N,'PedK','Long')
        arcpy.AddField_management(N,'PedA','Long')
        arcpy.AddField_management(N,'PedB','Long')
        ic = arcpy.InsertCursor(N)
        for i,r in CrashDict[year].iterrows():
            if not math.isnan(r.GIS_UTMX) and not math.isnan(r.GIS_UTMY):
                Pt =  arcpy.PointGeometry(arcpy.Point(r.GIS_UTMX,r.GIS_UTMY),UTM13N).projectAs(NAD83_NM)
                row = ic.newRow()
                row.setValue('Date',r.Date)
                row.setValue('UCRnum',str(r.name))
                row.setValue('KABCO',r.KABCO)
                row.setValue('Killed',r.Killed)
                row.setValue('ClassA',r.ClassA)
                row.setValue('ClassB',r.ClassB)
                #row.setValue('PedInv',r.PEDinv)
                row.setValue('GIS_Route',r.GIS_Route)
                #row.setValue('Severity',r.Severity)

                r2 = Occ_DF[(Occ_DF.year==year) & (Occ_DF.UCRnumber ==int(str(r.name)))]
                if r2.shape[0]>0:
                    row.setValue('PedK',int(sum(r2.Ped_K)))
                    row.setValue('PedA',int(sum(r2.Ped_A)))
                    row.setValue('PedB',int(sum(r2.Ped_B)))
                else:
                    row.setValue('PedK',0)
                    row.setValue('PedA',0)
                    row.setValue('PedB',0)


                row.shape = Pt
                ic.insertRow(row)

        del ic
        del row
        print (year,len(CrashDict[year]),float(str(arcpy.GetCount_management(N)))/float(len(CrashDict[year])))

def OppositeDirID(InpID):
    out = InpID[:-2]
    ext = InpID[-1]
    if ext == 'P':
        return('{}-M'.format(out))
    if ext == 'M':
        return('{}-P'.format(out))
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
def FindIntPG(Type_Major, Legs, Signal):
    if Type_Major=='R2U':
        if Signal == 0:
            if Legs==3:
                return('R3ST')
            if Legs == 4:
                return('R4ST')
        if Signal == 1:
            if Legs==3:
                return('R3SG')
            if Legs == 4:
                return('R4SG')
    if Type_Major in ['R4U','R4D']:
        if Signal == 0:
            if Legs==3:
                return('RM3ST')
            if Legs == 4:
                return('RM4ST')
        if Signal == 1:
            if Legs==3:
                return('RM3SG')
            if Legs == 4:
                return('RM4SG')
    if Type_Major in ['U2U','U4U','U4D']:
        if Signal == 0:
            if Legs==3:
                return('U3ST')
            if Legs == 4:
                return('U4ST')
        if Signal == 1:
            if Legs==3:
                return('U3SG')
            if Legs == 4:
                return('U4SG')
def OverlayIntersections(IntInput,Routes,AttTab,year):
    print('[{}] locate features along routes:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Project_GDB = os.path.dirname(IntInput)
    EventTable = common.CreateOutPath(MainFile=Project_GDB + '\\Int_'+str(year),appendix='EventTable',Extension='')
    arcpy.LocateFeaturesAlongRoutes_lr(
        in_features                = IntInput, 
        in_routes                = Routes, 
        route_id_field            = 'ROUTE_ID', 
        radius_or_tolerance        = '70 Feet', 
        out_table                = EventTable, 
        out_event_properties    = " ".join(['ROUTE_ID', "POINT", "MP"]),
        route_locations            = "ALL", 
        in_fields                = "FIELDS", 
        m_direction_offsetting    = "M_DIRECTON"
    )
    df = common.FCtoDF(EventTable)
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape[0]))

    print('[{}] attribute table to pandas:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Att_DF = common.FCtoDF(AttTab)
    Att_DF = Att_DF.sort_values(by=['ROUTE_ID','BEG_POINT'])
    Att_DF['Len'] = Att_DF.END_POINT-Att_DF.BEG_POINT
    Att_DF = Att_DF[(Att_DF.Len>0)]

    Att_DF['SurfWid'] = 24.0
    for i,r in Att_DF.iterrows():
        nl = 2
        try:
            nl = int(r.THROUGH_LANES)
        except:
            pass
        lw = 12.0
        try:
            lw = float(r.LANE_WIDTH)
        except:
            pass
        mdw = {1:0,2:4,3:4,4:6,5:6,6:6,7:6,0:0}
        md = 1
        try:
            md = int(r.MEDIAN_TYPE)
        except:
            pass
        surfwid = max(24,nl*lw+mdw[md])
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
        att_df = Att_DF[(Att_DF['ROUTE_ID']==r.ROUTE_ID) & (Att_DF.BEG_POINT<=r.MP) & (Att_DF.END_POINT>=r.MP)]
        if att_df.shape[0]>0:
            df.set_value(i,'SurfWid',max(list(att_df.SurfWid)))
            df.set_value(i,'AADT',max(list(att_df.AADT)))
            df.set_value(i,'FType',list(att_df.FType)[0])
    
    print('[{}] routes to pandas:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    df['fpM'] = 0.0
    df['lpM'] = 0.0
    Att_DF = Att_DF
    Routes_DF = common.FCtoDF(Routes,True)
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Att_DF.shape[0]))

    print('[{}] join route data to int:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    for i,r in df.iterrows():
        Rdf = Routes_DF[(Routes_DF['ROUTE_ID']==r.ROUTE_ID) & (Routes_DF['BEG_POINT']<=r.MP) & (Routes_DF['END_POINT']>=r.MP)]
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
        rid = Rdf.loc[i,'ROUTE_ID']
        ridL = [rid,OppositeDirID(rid)]
        for ind in list(Rdf.index):
            if Rdf.loc[ind,'ROUTE_ID'] in ridL:
                df.set_value(ind,'Major',1)
            else:
                df.set_value(ind,'Major',0)
        
    print('[{}] create approach dataframe:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    App_DF = df
    App_DF['Int_ID2'] = App_DF.Int_ID
    App_DF['RID'] = App_DF.ROUTE_ID
    App_Tab = pd.DataFrame(columns=['RID','BMP','EMP','IntProx','Int_ID2','Major'])
    x = 0
    for i,r in Routes_DF.iterrows():
        rid = r.ROUTE_ID
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

            if (1 in list(app.Signal)) and 1 in list(app.Major):
                int_b = 250.0/5280.0 + int_w
            if (1 in list(app.Signal)) and not (1 in list(app.Major)):
                int_b = 250.0/5280.0 + int_w
            if not (1 in list(app.Signal)) and 1 in list(app.Major):
                int_b = 250.0/5280.0 + int_w
            if not (1 in list(app.Signal)) and not (1 in list(app.Major)):
                int_b = 150.0/5280.0 + int_w

            bmp1 = max(mp - int_w - int_b,list(app.fpM)[0])
            emp1 = max(mp - int_w,list(app.fpM)[0])
            #if emp1>bmp1:
            #    x += 1
            #    App_Tab.loc[x] = [rid,bmp1,emp1,1,int_id,{True:1,False:0}[1 in list(app.Major)]]

            bmp2 = max(mp - int_w,list(app.fpM)[0])
            emp2 = min(mp + int_w,list(app.lpM)[0])
            #if emp2>bmp2:
            #    x += 1
            #    App_Tab.loc[x] = [rid,bmp2,emp2,2,int_id,{True:1,False:0}[1 in list(app.Major)]]

            bmp3 = min(mp + int_w,list(app.lpM)[0])
            emp3 = min(mp + int_w + int_b,list(app.lpM)[0])
            if emp3>bmp3:
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
            overlay_table            = Project_GDB+'\\SegAtt_' + str(year),
            overlay_event_properties = ' '.join(['ROUTE_ID','LINE','BEG_STA','END_STA']),
            overlay_type             = "INTERSECT", 
            out_table                = IntAppOverlay, 
            out_event_properties     = ' '.join(['ROUTE_ID','LINE','BEG_STA','END_STA']),
            zero_length_events       = "ZERO", 
            in_fields                = "FIELDS", 
            build_index              = "INDEX"
    )
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.management.GetCount(IntAppOverlay))))
    
    print('[{}] union overlay int approach table:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    SegIntAtt = common.CreateOutPath(MainFile=Project_GDB+'\\SegInt_Att',appendix=str(year),Extension='')
    arcpy.lr.OverlayRouteEvents(
            in_table                 = Project_GDB+'\\SegAtt_' + str(year),
            in_event_properties      = ' '.join([RouteID,'LINE',BEG_STA,END_STA]), 
            overlay_table            = Project_GDB+'\\CreateInt_AppTab_' + str(year),
            overlay_event_properties = ' '.join(['RID','LINE','BMP','EMP']),
            overlay_type             = "UNION", 
            out_table                = SegIntAtt, 
            out_event_properties     = ' '.join(['ROUTE_ID','LINE','BEG_STA','END_STA']),
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
    arcpy.conversion.FeatureClassToFeatureClass(in_features=Project_GDB+'\\CreateInt_Final',out_name=os.path.basename(Int),out_path=Project_GDB)
    arcpy.management.AddField(Int,'IFType','Text',10)
    arcpy.management.AddField(Int,'I_URBANCODE','Long')
    arcpy.management.AddField(Int,'FType_Major','Text',10)
    arcpy.management.AddField(Int,'FType_Minor','Text',10)
    arcpy.management.AddField(Int,'F_SYSTEM_Major','Short')
    arcpy.management.AddField(Int,'F_SYSTEM_Minor','Short')
    arcpy.management.AddField(Int,'OWNERSHIP_Major','Short')
    arcpy.management.AddField(Int,'OWNERSHIP_Minor','Short')
    arcpy.management.AddField(Int,'AADT_Major','Long')    
    arcpy.management.AddField(Int,'AADT_Minor','Long')    
    uc = arcpy.UpdateCursor(Int)
    for row in uc:
        int_id = row.getValue('Int_ID')
        signal = row.getValue('Signal')
        legs = row.getValue('Legs')
        type_major = ''
        
        idf = df[df.Int_ID==int_id]

        ft = list(idf[idf.Major==1]['AADT'])
        if len(ft)>0:
            row.setValue('AADT_Major',int(max(ft)))

        ft = list(idf[idf.Major==0]['AADT'])
        if len(ft)>0:
            row.setValue('AADT_Minor',int(max(ft)))

        ft = [t for t in set(list(idf[idf.Major==1]['FType'])) if t]
        if len(ft)>0:
            row.setValue('FType_Major',ft[0]) 
            type_major = ft[0]
        ft = [t for t in set(list(idf[idf.Major==0]['FType'])) if t]
        if len(ft)>0:
            row.setValue('FType_Minor',ft[0]) 

        ft = [t for t in set(list(idf[idf.Major==1]['F_SYSTEM'])) if t]
        if len(ft)>0:
            row.setValue('F_SYSTEM_Major',int(ft[0])) 

        ft = [t for t in set(list(idf[idf.Major==0]['F_SYSTEM'])) if t]
        if len(ft)>0:
            row.setValue('F_SYSTEM_Minor',int(ft[0])) 

        ft = [t for t in set(list(idf[idf.Major==1]['OWNERSHIP'])) if t]
        if len(ft)>0:
            row.setValue('OWNERSHIP_Major',int(ft[0]))

        ft = [t for t in set(list(idf[idf.Major==0]['OWNERSHIP'])) if t]
        if len(ft)>0:
            row.setValue('OWNERSHIP_Minor',int(ft[0]))

        ft = [t for t in set(list(idf[idf.Major==1]['URBAN_CODE'])) if t]
        if len(ft)>0:
            row.setValue('I_URBANCODE',int(ft[0])) 
        
        row.setValue('IFType',FindIntPG(Type_Major=type_major,Legs=legs,Signal=signal))
        
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
hsmpy3.nm.OverlayIntersections(IntInput,Routes,AttTab,year)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,IntInput,Routes,AttTab,year)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def AddRouteDirection(Routes):
    print(strftime("%Y-%m-%d %H:%M:%S"))
    Route_Dict = common.FCtoDF(Routes,True)
    Route_Dict['Direction'] = ''
    Route_Dict['Angle'] = 0.0
    for i,r in Route_Dict.iterrows():
        Shape = r.Shape
        a = 180 + math.atan2((Shape.lastPoint.Y - Shape.firstPoint.Y),(Shape.lastPoint.X - Shape.firstPoint.X)) * (180 / math.pi)  
        Route_Dict.set_value(i,'Angle',a)
        if a<=45 or a>=315:
            d = 'W'
        if a>45 and a<135:
            d = 'S'
        if a>=135 and a<=225:
            d = 'E'
        if a>225 and a<315:
            d = 'N'
        if str(r.ROUTE_ID).split('-')[2]=='M':
            d = {'N':'S','S':'N','E':'W','W':'E'}[d]
        Route_Dict.set_value(i,'Direction',d)
    for i,r in Route_Dict.iterrows():
        if str(r.ROUTE_ID).split('-')[2]=='M' and OppositeDirID(r.ROUTE_ID) in list(Route_Dict.ROUTE_ID):
            rdf = Route_Dict
            rdf = rdf[rdf.ROUTE_ID==OppositeDirID(r.ROUTE_ID)]
            d = {'N':'S','S':'N','E':'W','W':'E'}[list(rdf['Direction'])[0]]
            Route_Dict.set_value(i,'Direction',d)
    if not 'Direction' in [k.name for k in arcpy.ListFields(Routes)]:
        arcpy.management.AddField(Routes,'Direction','Text',1)
    uc = arcpy.UpdateCursor(Routes)
    for j in uc:
        rid = j.getValue('ROUTE_ID')
        j.setValue('Direction',list(Route_Dict[Route_Dict['ROUTE_ID']==rid]['Direction'])[0])
        uc.updateRow(j)
    del uc
    del j
    print(strftime("%Y-%m-%d %H:%M:%S"))
def CON_AddRouteDirection(WDir,HSMPY_PATH,Routes):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'AddDirection.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Routes = r'{}'

print("Add Route Direction")

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
hsmpy3.nm.AddRouteDirection(Routes)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Routes)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)



def GetPred(Seg_DF,rid,bmp,emp,a,b,SW):
    df = Seg_DF[Seg_DF.ROUTE_ID==rid][['ROUTE_ID','BEG_POINT','END_POINT','AADT']]
    #display(df)
    df = df.sort_values('BEG_POINT')
    df = df[(df.BEG_POINT>=bmp) | ((df.BEG_POINT<bmp) & (df.END_POINT>bmp))]
    df = df[(df.END_POINT<=emp) | ((df.BEG_POINT<emp) & (df.END_POINT>emp))]
    df.set_value(list(df.index)[0],'BEG_POINT',bmp)
    df.set_value(list(df.index)[-1],'END_POINT',emp)
    df['Length'] = df.END_POINT - df.BEG_POINT
    df['a'] = a
    df['b'] = b
    df['pred'] = [math.exp(a)*aadt**b*leng for a,b,aadt,leng in zip(df.a,df.b,df.AADT,df.Length)]
    #df['pred'] = df['pred']/df['Length']*SW
    #display(df)
    o = df.pred.sum()/df.Length.sum()*SW
    return(o)
def GetPred_Sum(p12,p13,p14,p15,p16):
    df = pd.DataFrame(columns=['Pred'],index=range(2012,2017))
    df.loc[2012,'Pred'] = p12
    df.loc[2013,'Pred'] = p13    
    df.loc[2014,'Pred'] = p14    
    df.loc[2015,'Pred'] = p15    
    df.loc[2016,'Pred'] = p16
    df = df[df.Pred>0]
    if df.shape[0]>0:
        return(5*df.Pred.mean())
    else:
        return(0)

def DissolveDF(df):
    df1 = pd.DataFrame(columns=['BMP','EMP','CrashFreq'])
    j = 0
    for i,r in df.iterrows():
        if i==0:
            j += 1
            df1.loc[j] = [r.BMP,r.EMP,r.CrashFreq]
        else:
            if r.CrashFreq>df1.loc[j,'CrashFreq']:
                if r.BMP < df1.loc[j,'BMP']:
                    df1.loc[j] = [df1.loc[j-1,'EMP'],r.EMP,r.CrashFreq]
                else:
                    df1.loc[j,'EMP'] = r.BMP
                    j += 1
                    df1.loc[j] = [r.BMP,r.EMP,r.CrashFreq]
            if r.CrashFreq<df1.loc[j,'CrashFreq']:
               j += 1
               df1.loc[j] = [df1.loc[j-1,'EMP'],r.EMP,r.CrashFreq]
            if r.CrashFreq==df1.loc[j,'CrashFreq']:
                df1.loc[j,'EMP'] = r.EMP
    if df1.EMP.max()<df.EMP.max():
        df1.loc[j,'EMP'] = df.EMP.max()
    return(df1)
def SlidingWindow(BMP,EMP,CL,Len,Inc):
    n = 0
    if EMP-BMP>Len:
        n = int(float(EMP-BMP-Len)/Inc)
    BMPList = [BMP + i*Inc for i in range(0,n+1)]
    df = pd.DataFrame(columns = ['BMP','EMP','CrashFreq'])
    for i,bmp in enumerate(BMPList):
        if bmp+Len <= EMP:
            cl = [c for c in CL if c>=bmp and c<bmp+Len]
            df.loc[i] = [bmp,bmp+Len,len(cl)]
        else:
            cl = [c for c in CL if c>=bmp and c<=EMP]
            df.loc[i] = [bmp,EMP,len(cl)]
    Max_EMP = df.EMP.max()
    if Max_EMP<EMP:
        cl = [c for c in CL if c>=EMP-Len and c<=EMP]
        df.loc[i+1] = [EMP-Len,EMP,len(cl)]

    return(df)
def CalculatePSIValues(Segs,CrashData,SPFsCSV,PSI_CSVOut,GDB):

    print('[{}] Read SPFs: {}'.format(strftime("%Y-%m-%d %H:%M:%S"),SPFsCSV))
    SPF = pd.read_csv(SPFsCSV,index_col=0)
    SPF.index = SPF.Type
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),SPF.shape))


    print('[{}] Read {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Segs[2016]))
    Segs_DF = common.FCtoDF(Segs[2016])
    Segs_DF = Segs_DF.loc[[s.split('-')[2]=='P' for s in Segs_DF.ROUTE_ID]]
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Segs_DF.shape))

    print('[{}] Read {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Segs[2015]))
    Segs_DF15 = common.FCtoDF(Segs[2015])
    Segs_DF15 = Segs_DF15.loc[[s.split('-')[2]=='P' for s in Segs_DF15.ROUTE_ID]]
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Segs_DF15.shape))

    print('[{}] Read {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Segs[2014]))
    Segs_DF14 = common.FCtoDF(Segs[2014])
    Segs_DF14 = Segs_DF14.loc[[s.split('-')[2]=='P' for s in Segs_DF14.ROUTE_ID]]
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Segs_DF14.shape))

    print('[{}] Read {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Segs[2013]))
    Segs_DF13 = common.FCtoDF(Segs[2013])
    Segs_DF13 = Segs_DF13.loc[[s.split('-')[2]=='P' for s in Segs_DF13.ROUTE_ID]]
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Segs_DF13.shape))

    print('[{}] Read {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Segs[2012]))
    Segs_DF12 = common.FCtoDF(Segs[2012])
    Segs_DF12 = Segs_DF12.loc[[s.split('-')[2]=='P' for s in Segs_DF12.ROUTE_ID]]
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Segs_DF12.shape))

    print('[{}] Read Crash Data'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Crash_DF = pd.concat([common.FCtoDF(CrashData[year],readGeometry=True) for year in range(2012,2018)])
    Crash_DF['Year'] = [d.year for d in Crash_DF.Date]
    Crash_DF['PedCrashCount'] = [{True:1,False:0}[sum([k,a,b])>0] for k,a,b in zip(Crash_DF.PedK,Crash_DF.PedA,Crash_DF.PedB)]
    Crash_DF['Count'] = 1
    Crash_DF['KAB'] = Crash_DF.Killed + Crash_DF.ClassA + Crash_DF.ClassB
    Crash_DF.index = ['{}_{}'.format(y,u) for u,y in zip(Crash_DF.UCRnum,Crash_DF.Year)]
    Crash_DF.index.name = 'CID'
    Crash_DF = Crash_DF.drop('CID',axis=1)
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Crash_DF.shape))

    print('[{}] Calculate PSIs'.format(strftime("%Y-%m-%d %H:%M:%S")))
    PSI_DF = pd.DataFrame()
    for i,r in Segs_DF.iterrows():
        rid = r.ROUTE_ID
        bmp = r.BEG_POINT
        emp = r.END_POINT
        df = Crash_DF[(Crash_DF.RID_P==rid) & (Crash_DF.MP_P>=bmp) & (Crash_DF.MP_P<=emp)]
        CL_R = list(df[df.Int_ID==0]['MP_P'])
        CL_R.sort()
        #if len(CL_R)==0:
        #    continue
        if r.URBAN_CODE in [0,99999]:
            SW = 1
            Inc = 0.2
        else:
            SW = 0.25
            Inc = .05
        df2 = SlidingWindow(bmp,emp,CL_R,SW,Inc)
        df3 = DissolveDF(df2)
        df3['RID'] = rid
        df3['FType'] = r.FType
        df3['AADT'] = r.AADT
        df3['F_SYSTEM'] = r.F_SYSTEM
        df3['FACILITY_TYPE'] = r.FACILITY_TYPE
        df3['OWNERSHIP'] = r.OWNERSHIP
        df3['URBAN_CODE'] = r.URBAN_CODE
        df3['THROUGH_LANES'] = r.THROUGH_LANES
        df3['MEDIAN_TYPE'] = r.MEDIAN_TYPE
        df3['SPEED_LIMIT'] = r.SPEED_LIMIT
    
        df3['Length'] = df3.EMP-df3.BMP
        if r.FType in SPF.index and r.AADT>0:
            df3['a'] = SPF.loc[r.FType,'Intercept']
            df3['b'] = SPF.loc[r.FType,'AADT']
            df3['k'] = SPF.loc[r.FType,'Dispersion']
            df3['k_l'] = df3['k']/SW
            df3['pred16'] = [math.exp(a)*aadt**b*SW for a,b,aadt in zip(df3.a,df3.b,df3.AADT)]
            df3['pred15'] = [GetPred(Segs_DF15,rid,bmp1,emp1,a,b,SW) for a,b,bmp1,emp1 in zip(df3.a,df3.b,df3.BMP,df3.EMP)]
            df3['pred14'] = [GetPred(Segs_DF14,rid,bmp1,emp1,a,b,SW) for a,b,bmp1,emp1 in zip(df3.a,df3.b,df3.BMP,df3.EMP)]
            df3['pred13'] = [GetPred(Segs_DF13,rid,bmp1,emp1,a,b,SW) for a,b,bmp1,emp1 in zip(df3.a,df3.b,df3.BMP,df3.EMP)]
            df3['pred12'] = [GetPred(Segs_DF12,rid,bmp1,emp1,a,b,SW) for a,b,bmp1,emp1 in zip(df3.a,df3.b,df3.BMP,df3.EMP)]
            df3['pred'] = [GetPred_Sum(p12,p13,p14,p15,p16) for p12,p13,p14,p15,p16 in zip(df3.pred16,df3.pred15,df3.pred14,df3.pred13,df3.pred12)]
            df3['w'] = [1.0/(1.0+k*p) for k,p in zip(df3.k,df3.pred)]
            df3['exp'] = [p*w+(1-w)*o for p,w,o in zip(df3.pred,df3.w,df3.CrashFreq)]
            df3['psi'] = df3.exp - df3.pred
        PSI_DF = pd.concat([PSI_DF,df3])
    PSI_DF.rename(columns={'a':'SPF_a','b':'SPF_b','exp':'CF_Exp','pred':'CF_Pred','psi':'PSI','w':'EB_w','k':'SPF_k','k_l':'Seg_k',
                          'CrashFreq':'CF_Obs','AADT':'AADT_2016','pred12':'CF_Pred_2012','pred13':'CF_Pred_2013','pred14':'CF_Pred_2014',
                          'pred15':'CF_Pred_2015','pred16':'CF_Pred_2016'},inplace=True)
    PSI_DF = PSI_DF[['RID', 'BMP','EMP', 'Length','FType','AADT_2016',
            'F_SYSTEM','FACILITY_TYPE','OWNERSHIP','URBAN_CODE','THROUGH_LANES','MEDIAN_TYPE','SPEED_LIMIT',
            'CF_Obs','CF_Pred','CF_Exp','PSI','CF_Pred_2012','CF_Pred_2013','CF_Pred_2014','CF_Pred_2015','CF_Pred_2016', 
            'SPF_a', 'SPF_b', 'SPF_k', 'Seg_k', 'EB_w']]
    PSI_DF.to_csv(PSI_CSVOut)
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),PSI_DF.shape))

    print('[{}] Export to GIS'.format(strftime("%Y-%m-%d %H:%M:%S")))
    #GDB = Project_DIR +'\\8.Deliverable\\CompiledData.gdb'
    TopSeg_PSI_Table = common.CreateOutPath(MainFile=GDB+'\\TopSeg_PSI',Extension='',appendix='table')
    arcpy.management.CopyRows(
        in_rows=PSI_CSVOut,
        out_table=TopSeg_PSI_Table
    )
    TopSeg_PSI_Layer = common.CreateOutLayer('TopSeg_PSI_Layer')
    arcpy.lr.MakeRouteEventLayer(
        in_routes = GDB+'\\Routes_2016', 
        route_id_field = 'ROUTE_ID', 
        in_table = TopSeg_PSI_Table, 
        in_event_properties = 'RID Line BMP EMP', 
        out_layer = TopSeg_PSI_Layer
    )
    TopSeg_PSI_FC = common.CreateOutPath(MainFile=GDB+'\\TopSeg',Extension='',appendix='PSI')
    arcpy.management.CopyFeatures(
        in_features=TopSeg_PSI_Layer,
        out_feature_class=TopSeg_PSI_FC
    )
    arcpy.management.Delete(TopSeg_PSI_Layer)
    arcpy.management.Delete(TopSeg_PSI_Table)
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),arcpy.GetCount_management(TopSeg_PSI_FC)[0]))

    print('[{}] Done!'.format(strftime("%Y-%m-%d %H:%M:%S")))
def CON_CalculatePSIValues(WDir,HSMPY_PATH,Segs,CrashData,SPFsCSV,PSI_CSVOut,GDB):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'CalPSI.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Segs = {}
CrashData = {}
SPFsCSV = r'{}'
PSI_CSVOut = r'{}'
GDB = r'{}'

print("Calculate PSI")

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
hsmpy3.nm.CalculatePSIValues(Segs,CrashData,SPFsCSV,PSI_CSVOut,GDB)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Segs,CrashData,SPFsCSV,PSI_CSVOut,GDB)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)

def CreateDiagnosticsFigures():
    def SHSP_EABarStateLine(Crash_DF,Selection,Field,png_out,Order=[],Length=0,r=''):
        df = pd.DataFrame(Crash_DF.groupby([Field])['KAB'].aggregate(sum))
        df.KAB = df.KAB/float(sum(df.KAB))
        df.columns = [Field]
        if len(Order) == 0:
            df = df.sort_index(ascending=True)
        else:
            df = df.loc[Order]
        if 1<2:
            plt.figure(figsize=(13, 7), dpi=300, facecolor='w', edgecolor='k')
            eadf = pd.DataFrame(Crash_DF.loc[Selection].groupby([Field])['KAB'].aggregate(sum))
            eadf = eadf.fillna(0)
            eadf.KAB = eadf.KAB/float(sum(eadf.KAB))
            eadf.columns = [Field]
            if Length>0:
                eadf = eadf.sort_values(Field,ascending=False)
                eadf = eadf.iloc[range(min(Length,len(eadf)))]
                df = pd.DataFrame(Crash_DF.groupby([Field])['KAB'].aggregate(sum))
                df.KAB = df.KAB/float(sum(df.KAB))
                df.columns = [Field]
                if len(Order) == 0:
                    df = df.sort_index(ascending=True)
                else:
                    df = df.loc[Order]
                df  = df.loc[list(eadf.index)]
            else:
                eadf = eadf.loc[df.index]
            eadf = eadf.fillna(0)
            V = [v1-v2 for v1,v2 in zip(eadf[Field],df[Field])]
            my_cmap = matplotlib.cm.get_cmap('RdYlGn_r')
            my_norm = matplotlib.colors.Normalize(vmin=min(V), vmax=max(V))
            p1 = plt.bar(range(len(eadf)),eadf[Field],align='center',color=my_cmap(my_norm(V)))
            plt.xticks(range(len(df)),df.index,rotation=90)
            p2, = plt.plot(range(len(df)),df[Field],'-o',color='green')
            plt.xlabel(Field)
            #plt.xticks(rotation=90)
            plt.title('{} - {} - {} - {}'.format(r.District,r.StateLocal,r.UrbanRural,r.Dis_Label))
            plt.grid()
            plt.gca().set_yticklabels(['{:,.2%}'.format(x) for x in plt.gca().get_yticks()])
            plt.legend([p2,p1],['Statewide Crashes ({})'.format(Crash_DF.shape[0]),'Site-Specific Crashes ({})'.format(eadf.shape[0])],loc=2,fancybox=True,framealpha=0.5,prop={'size': 9})
            plt.tight_layout()
            plt.savefig(png_out,transparent=False,dpi=1200, bbox_inches='tight', pad_inches=0)
            plt.close()
    def SHSP_TimeTrend_Contour(DF,PNGName,Title):
        import warnings
        warnings.filterwarnings('ignore')
        DF['Time'] = [datetime.time(datetime(2000,1,1,d.hour,0)).strftime('%I:%M %p') for d in DF.Date]
        TimeOrder = [datetime.time(datetime(2000,1,1,d,0)).strftime('%I:%M %p') for d in range(0,24)]
        TimeOrder.reverse()
        DF['DayName'] = [d.weekday_name for d in DF.Date]
        DayOrder = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        DF['Month']  = [d.strftime('%b') for d in DF.Date]
        MonthOrder = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        if 1<2:
            df0 = pd.DataFrame(DF.groupby(['Month','DayName','Time'])['KAB'].aggregate(sum))
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
        
            plt.figure(figsize=(13, 7), dpi=300, facecolor='w', edgecolor='k')
            ax1 = plt.subplot(211)
        
            df1 = df[MonthOrder[0:6]]
            #pl1 = plt.contourf(df1, cmap=plt.cm.Reds,corner_mask=True ,alpha=1)
            pl1 = plt.imshow(df1, cmap=plt.cm.Reds,alpha=1,aspect='auto')
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
            #pl2 = plt.contourf(df1, cmap=plt.cm.Reds,corner_mask=True ,alpha=1)
            pl2 = plt.imshow(df1, cmap=plt.cm.Reds,alpha=1,aspect='auto')
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
            plt.suptitle(Title,y=0.99)
            #plt.tight_layout()
            plt.savefig(PNGName,transparent=False,dpi=1200, bbox_inches='tight', pad_inches=0)
            plt.close()

    # Defining Parameteres
    print(strftime("%Y-%m-%d %H:%M:%S"))
    Years = range(2012,2017)
    MaxOpenProcesses = 15
    Project_DIR  = r'\\CHCFPP01\Proj\ILDOT\650511SAFETYPROGRAM\4_WorkData\WO00_OtherStates\NewMexico\3_WorkData\7_NetworkScreening'
    ReceivedDir  = Project_DIR + '\\2.Received_Data'
    Project_GDB  = Project_DIR + '\\5.NM_NS_GDB.gdb'
    PythonDir   = Project_DIR + '\\6.Python_Notebook'
    DeliverableDir = Project_DIR + '\\8.Deliverable'

    Src_Loc  = ReceivedDir + '\\crash_asof_11jun2018.csv'
    Src_Unit = ReceivedDir + '\\vehicle_asof_11jun2018.csv'
    Src_Occ  = ReceivedDir + '\\occupant_asof_11jun2018.csv'

    Src_Ped_Loc  = ReceivedDir + '\\Ped_2017_KAB\\crashkabped.csv'
    Src_Ped_Unit = ReceivedDir + '\\Ped_2017_KAB\\vehiclekabped.csv'
    Src_Ped_Occ  = ReceivedDir + '\\Ped_2017_KAB\\occkabped.csv'

    HPMS105 = {year:ReceivedDir + '\\v105\\jg_request.gdb\\HPMS{}Data'.format(year) for year in Years}
    HPMS10  = {year:ReceivedDir + '\\v10\\jg_request.gdb\\HPMS{}Data'.format(year) for year in Years}

    FOU_2017_105 = ReceivedDir + '\\v105\\jg_request.gdb\\HPMS2017Ownership_Urban_FuncSys'
    FOU_2017_10  = ReceivedDir + '\\v10\\jg_request.gdb\\HPMS2017Ownership_Urban_FuncSys'

    FHWA_HPMS     = {year:ReceivedDir + '\\FHWA_HPMS\\newmexico{}\\NewMexico{}.shp'.format(year,year) for year in Years}
    MS2_HPMS_2017 = {year:ReceivedDir + '\\NM_HPMS_N2017_A{}.csv'.format(year) for year in Years}

    Routes  = {year:Project_GDB + '\\Routes_{}'.format(year) for year in Years}
    AttTabs = {year:Project_GDB + '\\SegAtt_{}'.format(year) for year in Years}
    Segs    = {year:Project_GDB + '\\Seg_{}'.format(year) for year in Years}
    CrashData = {year:Project_GDB + '\\Crash_{}'.format(year) for year in range(2012,2018)}


    # Reading Source Crashes
    print(strftime("%Y-%m-%d %H:%M:%S"))

    Crash_DF = common.FCtoDF(Project_GDB + '\\NM_Crash_KAB_12_16',readGeometry=True)
    Crash_DF.index = Crash_DF.CID

    Loc_DF = pd.read_csv(Src_Loc,low_memory=False)
    Loc_DF['CID'] = ['{}_{}'.format(y,u) for y,u in zip(Loc_DF.year,Loc_DF.UCRnumber)]
    Loc_DF.index = Loc_DF.CID
    Loc_DF = Loc_DF.sort_index()

    F = ['CrashDirection',
    'Astreet',
    'Bstreet',
    'Landmark',
    'DirectionFromLandmark',
    'Measurement',
    'MeasurementUnit',
    'Class',
    'Analysis',
    'CrashOccurrence',
    'HitRun',
    'Light',
    'Weather',
    'RoadCharacter',
    'RoadGrade',
    'nVeh',
    'TopCFacc',
    'Alcinv',
    'Druginv',
    'MCinv',
    'PECinv',
    'TRKinv',
    'HZinv']
    Loc_DF.index = Loc_DF.CID
    for c in F:
        Crash_DF[c] = Loc_DF[c].loc[Crash_DF.index]
    print(Crash_DF.shape)

    Unit_DF = pd.read_csv(Src_Unit,low_memory=False)
    Unit_DF['CUID'] = ['{}_{}_{}'.format(y,u,v) for y,u,v in zip(Unit_DF.year, Unit_DF.UCRnumber,Unit_DF.VehNo)]
    Unit_DF['CID'] = ['{}_{}'.format(y,u) for y,u in zip(Unit_DF.year, Unit_DF.UCRnumber)]
    #Unit_DF.index = pd.MultiIndex.from_tuples([('{}_{}'.format(y,u),v) for y,u,v in zip(Unit_DF.year, Unit_DF.UCRnumber,Unit_DF.VehNo)],names=['CID','Unit'])
    Unit_DF.index = Unit_DF.CID
    Unit_DF = Unit_DF.sort_index()
    Unit_DF = Unit_DF[Unit_DF.CID.isin(Crash_DF.CID)]
    Unit_DF['Shape'] = Crash_DF.Shape.loc[Unit_DF.index]
    Unit_DF['Date'] = Crash_DF.Date.loc[Unit_DF.index]
    F = ['VehNo','Date', 'Passengers', 'DALC', 'DRUG', 'DRESID', 'TopCFcar', 'TypeV', 'Belt', 'Helmet', 'VehDirection', 'StreetOn', 'PostedSpeed', 'SafeSpeed', 'LeftScene', 'DrSeatPos', 'DrAge', 'DrSex', 'DrInjuryCode', 'DrOPCode', 'DrOPProperlyUsed', 'DrAirbagDeployed', 'DrEjected', 'DrEMSNum', 'DrMedTrans', 'DLState', 'DLType', 'DLRestrictions', 'DLExpires', 'DLEndorsements', 'DLStatus', 'VeYear', 'VeMake', 'VeColor', 'VeBodystyle', 'VeCargoBody', 'VeUse1', 'VeUse2', 'VeLicPlateRegYr', 'VeLicPlateState', 'VeTowed', 'VeTowedDisabled', 'VeDamageSeverity', 'VeDamageExtent', 'VeDamageAll', 'HazmatName', 'HazmatPlacard', 'HazmatReleased', 'RoadConditionsVe', 'RoadSurfaceVe', 'TrafficControlDevice', 'RoadDesignLanes', 'RoadDesignDivider', 'RoadDesign', 'SequenceEvent1', 'SequenceEvent2', 'SequenceEvent3', 'SequenceEvent4', 'vVehNo', 'vViolation', 'vAction', 'TraCS', 'CUID', 'CID', 'Shape']
    Unit_DF = Unit_DF[F]
    print(Unit_DF.shape)


    OL = ['CUID','PPLNo', 'OccNo', 'SeatPos', 'Age', 'Sex', 'Injury', 'OPCode', 'OPProperlyUsed', 'AirbagDeployed', 'Ejected', 'MedTrans', 'DAparked', 'Belt', 'Helmet']
    Occ_DF = pd.read_csv(Src_Occ,low_memory=False)
    Occ_DF['CID'] = ['{}_{}'.format(y,u) for y,u in zip(Occ_DF.year, Occ_DF.UCRnumber)]
    Occ_DF['CUID'] = ['{}_{}_{}'.format(y,u,v) for y,u,v,p in zip(Occ_DF.year, Occ_DF.UCRnumber,Occ_DF.VehNo,Occ_DF.PPLNo)]
    #Occ_DF.index = pd.MultiIndex.from_tuples([('{}_{}'.format(y,u),v,p) for y,u,v,p in zip(Occ_DF.year, Occ_DF.UCRnumber,Occ_DF.VehNo,Occ_DF.PPLNo)],names=['CID','Unit','Person'])
    Occ_DF.index = Occ_DF.CID
    Occ_DF = Occ_DF[Occ_DF.CID.isin(Crash_DF.CID)]
    Occ_DF = Occ_DF.sort_index()
    Occ_DF['Shape'] = Crash_DF.Shape.loc[Occ_DF.index]
    Occ_DF['Date'] = Crash_DF.Date.loc[Occ_DF.index]
    F = ['VehNo','Date', 'PPLNo', 'OccNo', 'SeatPos', 'Age', 'Sex', 'Injury', 'OPCode', 'OPProperlyUsed', 'AirbagDeployed', 'Ejected', 'MedTrans', 'DAparked', 'Belt', 'Helmet', 'CID', 'CUID', 'Shape']
    Occ_DF = Occ_DF[F]
    print(Occ_DF.shape)
    print(strftime("%Y-%m-%d %H:%M:%S"))

    # Translate and Add Additional Fields to Crash Data
    print(strftime("%Y-%m-%d %H:%M:%S"))
    Crash_DF['X'] = [s.firstPoint.X for s in Crash_DF.Shape]
    Crash_DF['Y'] = [s.firstPoint.Y for s in Crash_DF.Shape]
    idx = Crash_DF[(~pd.isnull(Crash_DF.X)) & (~pd.isnull(Crash_DF.Y))].index
    Crash_DF.loc[idx,'Point'] = [arcpy.PointGeometry(arcpy.Point(x,y),NAD83_NM).projectAs(common.WGS1984) for x,y in zip(list(Crash_DF.loc[idx,'X']),list(Crash_DF.loc[idx,'Y']))]
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
    Crash_DF.loc[idx,'LAT'] = [GetLAT(p) for p in Crash_DF.Point.loc[idx]]
    Crash_DF.loc[idx,'LON'] = [GetLON(p) for p in Crash_DF.Point.loc[idx]]
        
    Crash_DF['SUN_ANG'] = [il.SunAngle(lt,ln,dt) for lt,ln,dt in zip(list(Crash_DF.LAT),list(Crash_DF.LON),list(Crash_DF.Date))]

    def DayNight(d,s):
        if s<-6:
            return('Night')
        if s>0:
            return('Day')
        if s>=-6 and s <=0:
            if d.hour<12:
                return('Dawn')
            else:
                return('Dusk')
        return('Unknown')
    Crash_DF["DayNight"] = [DayNight(d,s) for d,s in zip(Crash_DF.Date,Crash_DF.SUN_ANG)]

    Crash_DF['Time'] = [datetime.time(datetime(2000,1,1,d.hour,0)).strftime('%I:%M %p') for d in Crash_DF.Date]
    TimeOrder = [datetime.time(datetime(2000,1,1,d,0)).strftime('%I:%M %p') for d in range(0,24)]
    Crash_DF['DayName'] = [d.weekday_name for d in Crash_DF.Date]
    DayOrder = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    Crash_DF['Month']  = [d.strftime('%b') for d in Crash_DF.Date]
    MonthOrder = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    Crash_DF['Year'] = [d.year for d in Crash_DF.Date]
    Crash_DF['PedCrashCount'] = [{True:1,False:0}[sum([k,a,b])>0] for k,a,b in zip(Crash_DF.PedK,Crash_DF.PedA,Crash_DF.PedB)]
    Crash_DF['Count'] = 1
    Crash_DF['KAB'] = Crash_DF.Killed + Crash_DF.ClassA + Crash_DF.ClassB
    def LightConv(l):
        if pd.isnull(l):
            return('Unknown')
        else:
            return({1:'DayLight',2:'Dawn',3:'Dusk',4:'Dark - Lighted',5:'Dark - unlighted',6:'Unknown',0:'Unknown',99:'Unknown',98:'Unknown'}[l])
    def WeatherConv(l):
        if pd.isnull(l):
            return('Unknown')
        else:
            return({1:'Clear',2:'Raining',3:'Snowing',4:'Fog',5:'Dust',6:'Wind',7:'Other',8:'Sleet or Hail',99:'Unknown',98:'Unknown',0:'Unknown'}[l])
        
    Crash_DF['Light'] = [LightConv(l) for l in Loc_DF.Light.loc[Crash_DF.index]]
    Crash_DF['Weather'] = [WeatherConv(l) for l in Loc_DF.Weather.loc[Crash_DF.index]]
    print(strftime("%Y-%m-%d %H:%M:%S"))

    Res_DF = pd.read_excel(PythonDir + '\\Aggregated_Sites2.xlsx')

    print(strftime("%Y-%m-%d %H:%M:%S"))
    for i,r in Res_DF.iterrows():
        print(r.Site_ID )
        SHSP_TimeTrend_Contour(Crash_DF.loc[r.All_CIDs],'Site_{}_Contour.png'.format(r.Site_ID),'{} - {} - {} - {}\n({} KAB Crashes)'.format(r.District,r.StateLocal,r.UrbanRural,r.Dis_Label,Crash_DF.loc[r.All_CIDs].shape[0]))
        SHSP_EABarStateLine(Crash_DF,r.All_CIDs,'Time','Site_{}_Time.png'.format(r.Site_ID),Order=TimeOrder,Length=0,r=r)
        SHSP_EABarStateLine(Crash_DF,r.All_CIDs,'DayName','Site_{}_Day.png'.format(r.Site_ID),Order=DayOrder,Length=0,r=r)
        SHSP_EABarStateLine(Crash_DF,r.All_CIDs,'Month','Site_{}_Month.png'.format(r.Site_ID),Order=MonthOrder,Length=0,r=r)
        SHSP_EABarStateLine(Crash_DF,r.All_CIDs,'DayNight','Site_{}_DayNight.png'.format(r.Site_ID),Order=['Dawn','Day','Dusk','Night'],Length=0,r=r)
        #SHSP_EABarStateLine(Crash_DF,r.All_CIDs,'Light','Light.png',Order=[],Length=0,r=r)
        SHSP_EABarStateLine(Crash_DF,r.All_CIDs,'Weather','Site_{}_Weather.png'.format(r.Site_ID),Order=[],Length=0,r=r)
    print(strftime("%Y-%m-%d %H:%M:%S"))