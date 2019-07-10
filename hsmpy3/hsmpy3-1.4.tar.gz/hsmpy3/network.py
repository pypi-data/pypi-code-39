#HSMPY3
# Developed By Mahdi Rajabi mrajabi@clemson.edu
import os
import sys
import hsmpy3.common as common
import hsmpy3.fields_SC as fields_SC
import hsmpy3.fields
import hsmpy3.fields_IL
import datetime
import json
import arcpy
import math
import pandas as pd
import numpy as np
from scipy import optimize
import re
from time import gmtime, strftime
import matplotlib.pyplot as plt

def ExtractIntFromSeg(Segments,Intersections,Buffer,Output):
    #Output should be on a GDB not a shapefile
    SegFields = [f.name for f in arcpy.ListFields(Segments)]

    SelInt = common.CreateOutPath(MainFile=Output,appendix='SelInt',Extension='')
    arcpy.SpatialJoin_analysis(target_features = Intersections, 
                               join_features = Segments, 
                               out_feature_class = SelInt, 
                               join_operation = 'JOIN_ONE_TO_ONE', 
                               join_type = 'KEEP_COMMON', 
                               match_option = 'INTERSECT',
                               search_radius = Buffer)
    arcpy.DeleteField_management(SelInt,[f.name for f in arcpy.ListFields(SelInt) if not  f.required])

    SelIntBuf = common.CreateOutPath(MainFile=Output,appendix='SelIntBuf',Extension='')
    arcpy.Buffer_analysis(in_features = SelInt, 
                          out_feature_class = SelIntBuf, 
                          buffer_distance_or_field = str(Buffer) + ' Feet', 
                          line_side = 'FULL', 
                          line_end_type = 'FLAT')

    F2L = common.CreateOutPath(MainFile = Output,appendix='F2L',Extension='')
    arcpy.FeatureToLine_management (in_features = [Segments,SelIntBuf], 
                                    out_feature_class = F2L,attributes='ATTRIBUTES')
    
    F2LLayer = common.CreateOutLayer('F2LLayer')
    arcpy.MakeFeatureLayer_management(in_features = F2L,out_layer = F2LLayer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = F2LLayer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "BUFF_DIST = 0")

    Seg1F = common.CreateOutPath(MainFile = Output,appendix='Seg1F',Extension='')
    arcpy.CopyFeatures_management(in_features=F2LLayer,out_feature_class=Seg1F)
    arcpy.DeleteField_management(Seg1F,[f.name for f in arcpy.ListFields(Seg1F) if not f.required and not f.name in SegFields])
    
    Selseg = common.CreateOutPath(MainFile=Output,appendix='SelSeg',Extension='')
    arcpy.SpatialJoin_analysis(target_features = Seg1F, 
                               join_features = SelIntBuf, 
                               out_feature_class = Selseg, 
                               join_operation = 'JOIN_ONE_TO_ONE', 
                               join_type = 'KEEP_ALL', 
                               match_option = 'WITHIN')
    
    SPJLayer = common.CreateOutLayer('SPJLayer')
    arcpy.MakeFeatureLayer_management(in_features = Selseg,out_layer = SPJLayer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = SPJLayer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "Join_Count = 0 AND Shape_Length>528")

    arcpy.CopyFeatures_management(in_features=SPJLayer,out_feature_class=Output)
    arcpy.DeleteField_management(Output,[f.name for f in arcpy.ListFields(Output) if not f.required and not f.name in SegFields])

    arcpy.Delete_management(SelInt)    
    arcpy.Delete_management(SelIntBuf)    
    arcpy.Delete_management(F2L)    
    arcpy.Delete_management(F2LLayer)    
    arcpy.Delete_management(Seg1F)    
    arcpy.Delete_management(Selseg)    
    arcpy.Delete_management(SPJLayer)
def ImportRoadwayData_Old(Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance):
    #Output should be on a GDB not a shapefile

    #Step 1: Create a route FC based on the input 
    Sites_Event_Table = common.CreateOutPath(MainFile=Output,appendix='EventTab',Extension='')
    arcpy.LocateFeaturesAlongRoutes_lr(in_features = Input, 
                                       in_routes = Route, 
                                       route_id_field = RouteID, 
                                       radius_or_tolerance = XY_Tolerance, 
                                       out_table = Sites_Event_Table, 
                                       out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                       route_locations = "FIRST", 
                                       distance_field = "DISTANCE", 
                                       zero_length_events = "ZERO", 
                                       in_fields = "FIELDS", 
                                       m_direction_offsetting = "M_DIRECTON")
    Sites_Event_Layer = common.CreateOutLayer('EventLayer')
    arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
                                 route_id_field = RouteID, 
                                 in_table = Sites_Event_Table, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 out_layer = Sites_Event_Layer, 
                                 add_error_field="NO_ERROR_FIELD")
    
    Sites_Routes = common.CreateOutPath(MainFile=Output,appendix='route',Extension='')
    arcpy.CopyFeatures_management(in_features = Sites_Event_Layer,
                                  out_feature_class = Sites_Routes)
    
    IRIS_Diss = common.CreateOutPath(MainFile=Output,appendix='diss',Extension='')
    arcpy.DissolveRouteEvents_lr(in_events = AttTable, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_field = ';'.join(Fields), 
                                 out_table = IRIS_Diss, 
                                 out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_type="DISSOLVE", 
                                 build_index="INDEX")    
    
    Overlay_Event_Table1 = common.CreateOutPath(MainFile=Output,appendix='OverlayTab1',Extension='')
    arcpy.OverlayRouteEvents_lr(in_table = IRIS_Diss, 
                                in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                overlay_table = Sites_Event_Table, 
                                overlay_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                overlay_type = "INTERSECT", 
                                out_table = Overlay_Event_Table1, 
                                out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                zero_length_events = "NO_ZERO", 
                                in_fields = "FIELDS", 
                                build_index="INDEX")    
    
    Overlay_Event_Layer = common.CreateOutLayer('OverlayEventLayer')
    arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
                                 route_id_field = RouteID, 
                                 in_table = Overlay_Event_Table1, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 out_layer = Overlay_Event_Layer, 
                                 offset_field = "", 
                                 add_error_field = "ERROR_FIELD")     
    
    Sites_segs1 = common.CreateOutPath(MainFile=Output,appendix='seg1',Extension='')
    arcpy.CopyFeatures_management(in_features = Overlay_Event_Layer,
                                  out_feature_class = Sites_segs1)


    #Curves_Table = common.CreateOutPath(MainFile=Output,appendix='curves',Extension='')
    #ExtractCurves(inp=Sites_segs1,IDField=RouteID,RMax=5280,RMin=10,DegMin=2,desd=1000,LenMin=1000,out=Curves_Table)

    #Overlay_Event_Table2 = common.CreateOutPath(MainFile=Output,appendix='OverlayTab2',Extension='')
    #arcpy.OverlayRouteEvents_lr(in_table = Overlay_Event_Table1, 
    #                            in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            overlay_table = Curves_Table, 
    #                            overlay_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            overlay_type = "UNION", 
    #                            out_table = Overlay_Event_Table2, 
    #                            out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            zero_length_events = "NO_ZERO", 
    #                            in_fields = "FIELDS", 
    #                            build_index="INDEX") 

    #Overlay_Event_Layer2 = common.CreateOutLayer('OverlayEventLayer2')
    #arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
    #                             route_id_field = RouteID, 
    #                             in_table = Overlay_Event_Table2, 
    #                             in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                             out_layer = Overlay_Event_Layer2, 
    #                             offset_field = "", 
    #                             add_error_field = "ERROR_FIELD") 
    
    Sort = common.CreateOutPath(MainFile=Output,appendix='sort',Extension='')
    arcpy.Sort_management(in_dataset = Sites_segs1,
                          out_dataset = Sort,
                          sort_field = ';'.join([RouteID,BMP,EMP]))
    Final_Layer = common.CreateOutLayer('FinalLayer')
    
    arcpy.MakeFeatureLayer_management(in_features=Sort,out_layer=Final_Layer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = Final_Layer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "Shape_Length > 52")
    
    arcpy.Delete_management(Output)
    arcpy.MultipartToSinglepart_management(in_features=Final_Layer, 
                                           out_feature_class=Output)    
    arcpy.DeleteField_management(Output,'ORIG_FID')
    FL = [f.name for f in arcpy.ListFields(Output) if f.name != arcpy.Describe(Output).OIDFieldName]
    arcpy.DeleteIdentical_management(in_dataset = Output, 
                                     fields = ';'.join(FL), 
                                     xy_tolerance = "", 
                                     z_tolerance = "0")


    arcpy.Delete_management(Sites_Event_Table)
    arcpy.Delete_management(Sites_Event_Layer)
    arcpy.Delete_management(Sites_Routes)
    arcpy.Delete_management(IRIS_Diss)
    arcpy.Delete_management(Overlay_Event_Table1)
    arcpy.Delete_management(Overlay_Event_Layer)
    arcpy.Delete_management(Sites_segs1)
    #arcpy.Delete_management(Curves_Table)
    #arcpy.Delete_management(Overlay_Event_Table2)
    #arcpy.Delete_management(Overlay_Event_Layer2)
    arcpy.Delete_management(Sort)
    arcpy.Delete_management(Final_Layer)
def CreateRouteEventLayer(Sites_Routes,AttTable,RouteID,BMP,EMP,Fields,Output):
    IRIS_Diss = common.CreateOutPath(MainFile=Output,appendix='diss',Extension='')
    arcpy.DissolveRouteEvents_lr( in_events = AttTable, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_field = ';'.join(Fields), 
                                 out_table = IRIS_Diss, 
                                 out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_type="DISSOLVE", 
                                 build_index="INDEX")    
    #arcpy.DissolveRouteEvents_lr(AttTable, 
    #                             ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                             ';'.join(Fields), 
    #                             IRIS_Diss, 
    #                             ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                             "CONCATENATE", 
    #                             "INDEX")    

    Overlay_Event_Layer = common.CreateOutLayer('OverlayEventLayer')
    arcpy.MakeRouteEventLayer_lr(in_routes = Sites_Routes,
                                 route_id_field = RouteID, 
                                 in_table = IRIS_Diss, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 out_layer = Overlay_Event_Layer, 
                                 offset_field = "", 
                                 add_error_field = "ERROR_FIELD") 

    Sort = common.CreateOutPath(MainFile=Output,appendix='sort',Extension='')
    arcpy.Sort_management(in_dataset = Overlay_Event_Layer,
                          out_dataset = Sort,
                          sort_field = ';'.join([RouteID,BMP,EMP]))
    Final_Layer = common.CreateOutLayer('FinalLayer')
    
    arcpy.MakeFeatureLayer_management(in_features=Sort,out_layer=Final_Layer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = Final_Layer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "Shape_Length > 0")
    arcpy.Delete_management(Output)
    arcpy.CopyFeatures_management(in_features=Final_Layer,out_feature_class=Output)

    arcpy.Delete_management(IRIS_Diss)
    arcpy.Delete_management(Overlay_Event_Layer)
    arcpy.Delete_management(Sort)
    arcpy.Delete_management(Final_Layer)
def PrintSegSummary(Input,Title = ''):
    ts = int(str(arcpy.GetCount_management(Input)))
    ml = sum([r.getValue('Shape').length for r in arcpy.SearchCursor(Input)])/5280
    if 'AADT' in [f.name for f in arcpy.ListFields(Input)]:
        aa = sum([r.getValue('AADT') for r in arcpy.SearchCursor(Input)])/max(ts,1)
        print('{}: Total Segments: {}, Mileage: {:0.2f}, Average AADT {:0.2f}'.format(Title,ts,ml,aa)) 
    else:
        print('{}: Total Segments: {}, Mileage: {:0.2f}'.format(Title,ts,ml)) 
def PrintIntSummary(InputPoints,InputTable,Title = ''):
    ts = int(str(arcpy.GetCount_management(InputPoints)))
    tr = int(str(arcpy.GetCount_management(InputTable)))
    if 'AADT' in [f.name for f in arcpy.ListFields(InputTable)]:
        aa = sum([r.getValue('AADT') for r in arcpy.SearchCursor(InputTable)])/max(tr,1)
        print('{}: Total Points: {}, Total Legs: {}, Average AADT {:0.2f}'.format(Title,ts,tr,aa)) 
    else:
        print('{}: Total Points: {}, Total Legs: {}'.format(Title,ts,tr)) 
def ExtractCurves(inp,IDField,DegMin,RMax,RMin,LenMin,desd,out):
    def RemoveOverlap(Curves):
        import pandas as pd
        CDF = pd.DataFrame(columns=['BMP','EMP','Radius','Cen_X','Cen_Y'])
        CDF['BMP'] = [cur[0] for cur in Curves]
        CDF['EMP'] = [cur[1] for cur in Curves]
        CDF['Radius'] = [cur[2] for cur in Curves]
        CDF['Cen_X'] = [cur[3] for cur in Curves]
        CDF['Cen_Y'] = [cur[4] for cur in Curves]    
        for i in range(1,len(CDF)):
            if CDF.loc[i]['BMP']<CDF.loc[i-1]['EMP']:
                ave = (CDF.loc[i]['BMP']+CDF.loc[i-1]['EMP'])/2 
                CDF.loc[i]['BMP'] = ave
                CDF.loc[i-1]['EMP'] = ave
        return(CDF)
    def FindClusters(CD,DegMin):
        flag = False
        j = 0
        R = []
        T = []
        for i in range(len(CD['Radius'])):
            if abs(CD['Radius'][i]) > DegMin:
                T.append(int(math.copysign(1,CD['Radius'][i])))
                if not flag:
                    flag = True
                    j += 1
                else:
                    if CD['Radius'][i]*CD['Radius'][i-1]<=0:
                        j =+ 1
                        flag = True
            else:
                T.append(0)
                if flag:
                    j += 1
                    flag = False
            R.append(j)
        return({'CN':R,'CT':T})
    def FindRadius(Shape,DegMin,MinLen):
        import json
        import pandas as pd
        CD = HorCurvature(Shape)
        CL = FindClusters(CD,DegMin)
        l = json.loads(Shape.JSON)['paths'][0]
        DF = pd.DataFrame()
        DF['X'] = [i[0] for i in l]
        DF['Y'] = [i[1] for i in l]
        DF['Milepost'] = [i[3] for i in l]
        CD = HorCurvature(Shape)
        CL = FindClusters(CD,DegMin)
        DF['Heading Angle'] = CD['Radius']
        DF['Cluster Number'] = CL['CN']
        DF['Cluster Type'] = CL['CT']
        DF['Cluster Type'] = MergeCurves(DF,MinLen)
        Radius = []
        Cen_X = []
        Cen_Y = []
        Points = []
        kr = [-1]
        Curves = []
        for i in range(len(DF)):
            if not i in kr:
                if DF.loc[i]['Cluster Type'] == 0:
                    Cen_X.append(0)
                    Cen_Y.append(0)
                    Radius.append(0)
                    Points.append(str(i))
                else:
                    cl = [[DF.loc[i-1]['X'],DF.loc[i-1]['Y']]]
                    j = i
                    while DF.loc[j]['Cluster Type']==DF.loc[i]['Cluster Type']:
                        cl.append([DF.loc[j]['X'],DF.loc[j]['Y']])
                        j += 1
                    cl.append([DF.loc[j]['X'],DF.loc[j]['Y']])
                    CF = CircleFitting(cl)
                    Curves.append([
                        DF.loc[i-1]['Milepost'],
                        DF.loc[j]['Milepost'],
                        math.copysign(CF['Radius'],DF.loc[i]['Cluster Type']),
                        CF['Center'][0],
                        CF['Center'][1]
                    ])
                    kr = range(i,j)
                    for k in kr:
                            Radius.append(math.copysign(CF['Radius'],DF.loc[i]['Cluster Type']))
                            Cen_X.append(CF['Center'][0])
                            Cen_Y.append(CF['Center'][1])
                            Points.append(';'.join([str(t) for t in range(i-1,j+1)]))
                    
        DF['Radius'] = Radius
        DF['Center_X'] = Cen_X
        DF['Center_Y'] = Cen_Y
        DF['Points'] = Points
        CDF = RemoveOverlap(Curves)
        Res = RemoveSharpTurns(DF)
        DF['Cluster Type'] = Res[0]
        CDF = CDF.loc[[k for k in list(CDF.index) if not k in Res[1]]]
        return([DF,CDF])
    def MergeCurves(DF,MinLen):
        CT = [0]
        for i in range(1,len(DF)-1):
            if DF.loc[i]['Cluster Type'] == 0:
                if DF.loc[i-1]['Cluster Type'] == DF.loc[i+1]['Cluster Type']:
                    if (DF.loc[i+1]['Milepost']-DF.loc[i-1]['Milepost']) * 5280 <MinLen:
                        CT.append(DF.loc[i-1]['Cluster Type'])
                    else:
                        CT.append(DF.loc[i]['Cluster Type'])
                else:
                    CT.append(DF.loc[i]['Cluster Type'])
            else:
                CT.append(DF.loc[i]['Cluster Type'])
        CT.append(0)
        return(CT)
    def AddMidPoints(l,desd):
        pntl = [arcpy.Point(X = l[0][0],Y=l[0][1],Z=0,M=l[0][3])]
        for p in l[1:]:
            curpnt = arcpy.Point(X = p[0],Y=p[1],Z=0,M=p[3])
            curd = arcpy.PointGeometry(pntl[-1]).distanceTo(curpnt)
            if curd <= desd:
                pntl.append(curpnt)
            else:
                n = int(curd/desd)+1
                delta = curd/n
                pl = arcpy.Polyline(arcpy.Array([pntl[-1],curpnt]))
                for j in range(1,n):
                    if j*delta<curd:
                        midpg = pl.positionAlongLine(j*delta)
                        m = float((curpnt.M - pntl[-1].M))/n*j + pntl[-1].M
                        midp = arcpy.Point(midpg.firstPoint.X,midpg.firstPoint.Y,0,m)
                        pntl.append(midp)
                pntl.append(curpnt)
        return(pntl)
    def FindCurves(pl,DegMin,RMax,RMin,LenMin,desd):
        import json
        Curve = []
        pntl = json.loads(pl.JSON)['paths'][0]
        CD = HorCurvature(pl)
        flag = False
        for i in range(len(CD['Radius'])):
            if abs(CD['Radius'][i]) > DegMin:
                if not flag:
                    start = CD['Milepost'][i-1]
                    startSign =  math.copysign(1,CD['Radius'][i])
                    Dis = 0
                    flag = True
                    R = [pntl[i-1],pntl[i]]
                else:
                    if math.copysign(1,CD['Radius'][i])==startSign:
                        Dis = 0
                        endi = i
                        R.append(pntl[i])
                    else:
                        if Dis > 0:
                            end = CD['Milepost'][endi]
                            R = [r for r in R if r[3]<=end]
                            cirD = CircleFitting(R)
                            cirD['Radius'] = math.copysign(cirD['Radius'],CD['Radius'][endi-1])
                            if end<start:
                                print(start,end)
                            if abs(cirD['Radius'])<RMax and abs(cirD['Radius'])>RMin and (end-start)>LenMin:
                                Curve.append([start,end,cirD['Radius'],cirD['Center'][0],cirD['Center'][1]])
                            start = end
                            Dis = 0
                            flag = False
                            i=endi
                            R = []
                        else:
                            end = (CD['Milepost'][i-1] + CD['Milepost'][i])/2.0
                            R.append(pntl[i])
                            cirD = CircleFitting(R)
                            cirD['Radius'] = math.copysign(cirD['Radius'],CD['Radius'][i-1])
                            if end<start:
                                print(start,end)
                            if abs(cirD['Radius'])<RMax and abs(cirD['Radius'])>RMin and (end-start)>LenMin:
                                Curve.append([start,end,cirD['Radius'],cirD['Center'][0],cirD['Center'][1]])
                            start = end
                            Dis = 0
                            flag = True
                            R = [pntl[i-1],pntl[i]]
            else:
                if flag:
                    if Dis == 0:
                        endi = i
                    Dis += (CD['Milepost'][i] - CD['Milepost'][i-1])
                    if Dis>float(desd)/5280.0 or i==len(CD['Milepost'])-1:
                        end = CD['Milepost'][endi]
                        R.append(pntl[i])
                        R = [r for r in R if r[3]<=end]
                        if len(R)>=3:
                            cirD = CircleFitting(R)
                            cirD['Radius'] = math.copysign(cirD['Radius'],CD['Radius'][endi-1])
                            if end<start:
                                print(start,end)
                            if abs(cirD['Radius'])<RMax and abs(cirD['Radius'])>RMin and (end-start)>LenMin:
                                Curve.append([start,end,cirD['Radius'],cirD['Center'][0],cirD['Center'][1]])
                        flag = False
                        R = []
                        i=endi
                    else:
                        R.append(pntl[i])
        return(Curve)
    def CircleFitting(l):
        from scipy import optimize
        import numpy
        def calc_R(xc, yc):
            return numpy.sqrt((x-xc)**2 + (y-yc)**2)
        def f_2(c):
            Ri = calc_R(*c)
            return Ri - Ri.mean()
        x = numpy.array([i[0] for i in l])
        y = numpy.array([i[1] for i in l])
        x_m = sum(x)/max(len(x),1)
        y_m = sum(y)/max(len(y),1)
        center_estimate = x_m, y_m
        center_2, ier = optimize.leastsq(f_2, center_estimate)
        xc_2, yc_2 = center_2
        Ri_2       = calc_R(*center_2)
        R_2        = Ri_2.mean()
        residu_2   = sum((Ri_2 - R_2)**2)
        return({'Radius':R_2,'Center':[xc_2, yc_2]})
    def HorCurvature(Shape):
        import re
        import math
        import arcpy
        from math import acos
        from numpy.linalg import norm
        import numpy
        import json
        Inf = 52800 
        def findangle(p1, p2,p3):
            A = np.array(p1)
            B = np.array(p2)
            C = np.array(p3)
            v1 = B - A
            v2 = C - B
            def unit_vector(vector):
                return vector / np.linalg.norm(vector)
            v1_u = unit_vector(v1)
            v2_u = unit_vector(v2)
            return(np.degrees(np.arctan2(v2_u[1], v2_u[0])-np.arctan2(v1_u[1], v1_u[0])))
        def Radius(P1,P2,P3):
            Inf = 52800
            x1 = P1[0];x2 = P2[0];x3 = P3[0]
            y1 = P1[1];y2 = P2[1];y3 = P3[1]
            if y1==y2 and y2==y3:
                R = Inf
            elif y1==y2 and y2!=y3:
                m2 = -(x3-x2)/(y3-y2)
                xm1 = (x1+x2)/2
                ym1 = (y1+y2)/2
                xm2 = (x3+x2)/2
                ym2 = (y3+y2)/2
                xc = xm1
                yc = m2*(xc-xm2)+ym2
                R  = math.sqrt((xc-x1)**2+(yc-y1)**2)
                R = min(R,Inf)
                R = math.copysign(R,m2)
            elif y2==y3 and y1!=y2:
                m1 = -(x2-x1)/(y2-y1)
                xm1 = (x1+x2)/2
                ym1 = (y1+y2)/2
                xm2 = (x3+x2)/2
                ym2 = (y3+y2)/2
                xc = xm2
                yc = m1*(xc-xm1)+ym1
                R  = math.sqrt((xc-x1)**2+(yc-y1)**2)
                R = min(R,Inf)
                R = math.copysign(R,-m1)
            elif y1!=y2 and y3!=y2:
                if y3 == y1:
                    R = Inf
                elif y3!=y1:
                    if (x3-x1)/(y3-y1) == (x2-x1)/(y2-y1):
                        R = Inf
                    else:
                        m1 = -(x2-x1)/(y2-y1)
                        m2 = -(x3-x2)/(y3-y2)
                        xm1 = (x1+x2)/2
                        ym1 = (y1+y2)/2
                        xm2 = (x3+x2)/2
                        ym2 = (y3+y2)/2
                        xc = (ym1-ym2+m2*xm2-m1*xm1)/(m2-m1)
                        yc = m1*(xc-xm1)+ym1
                        R  = math.sqrt((xc-x1)**2+(yc-y1)**2)
                        R = min(R,Inf)
                        R = math.copysign(R,m2-m1)
            return(min(R,Inf))
        def Length(P1,P2):
            return(math.sqrt((P2[0]-P1[0])**2+(P2[1]-P1[1])**2))
        Vertices = json.loads(Shape.JSON)['paths'][0]
        R = [0]
        M = [Vertices[0][3]]
        L = Shape.length
        for i in range(2,len(Vertices)):
            l1 = Length(Vertices[i-2],Vertices[i-1])
            l2 = Length(Vertices[i-1],Vertices[i  ])
            #R.append(Radius(Vertices[i-2],Vertices[i-1],Vertices[i]))
            R.append(findangle(Vertices[i-2],Vertices[i-1],Vertices[i]))
            M.append(Vertices[i-1][3])
        R.append(0)
        M.append(Vertices[-1][3])
        return({'Radius':R,'Milepost':M})
    def progressBar(value, endvalue, bar_length=20):
        percent = float(value) / endvalue
        sys.stdout.write("\r{}%".format(int(round(percent * 100))))
        sys.stdout.flush()
    def RemoveSharpTurns(DF):
        j = -1
        pDict = {}
        rmcurve = []
        ct = []
        for i in range(0,len(DF)):
            Points = DF.loc[i]['Points'].split(';')
            if len(Points)>1 and not DF.loc[i]['Points'] in pDict.keys():
                j +=  1
                pDict.update({DF.loc[i]['Points']:0})
            if len(Points)>=3:
                Points = Points[1:-1]
                b = int(Points[0])
                e = int(Points[len(Points)-1])
                l = DF.loc[e]['Milepost'] - DF.loc[b]['Milepost']
                ha = list(DF.loc[[int(p) for p in Points]]['Heading Angle'])
                ha = abs(sum(ha)/len(ha))
                if l<0.03 and ha>=15:
                    rmcurve.append(j)
                    ct.append(2)
                else:
                    ct.append(DF.loc[i]['Cluster Type'])
            else:
                ct.append(DF.loc[i]['Cluster Type'])
        return([ct,rmcurve])
    #inp = sys.argv[1]
    #IDField = sys.argv[2]
    #desd = sys.argv[3]
    #DegMin = sys.argv[4]
    #RMax= sys.argv[5]
    #RMin= sys.argv[6]
    #LenMin= sys.argv[7]
    #out = sys.argv[3]
    #DegMin=2
    #RMax=5280*3
    #RMin=50
    #LenMin=100/5280
    #desd = 250

    arcpy.CreateTable_management(out_path=os.path.dirname(out),out_name=os.path.basename(out))
    arcpy.AddField_management(out,IDField,'TEXT')
    arcpy.AddField_management(out,'BEG_STA','DOUBLE')
    arcpy.AddField_management(out,'END_STA','DOUBLE')
    arcpy.AddField_management(out,'Radius','DOUBLE')
    arcpy.AddField_management(out,'CurveLen','DOUBLE')
    arcpy.AddField_management(out,'Center_X','DOUBLE')
    arcpy.AddField_management(out,'Center_Y','DOUBLE')
    arcpy.AddField_management(out,'CMF_CH10','DOUBLE')
    arcpy.AddField_management(out,'CMF_CH18','DOUBLE')
    OID = arcpy.Describe(inp).OIDFieldName
    INV = {r.getValue(OID):{'INV':r.getValue(IDField),'Shape':r.getValue('Shape')} for r in arcpy.SearchCursor(inp)}
    IC = arcpy.InsertCursor(out)
    arcpy.SetProgressor("step", "Finding Curves...",0, len(INV),1)
    k = INV.keys()
    k.sort()
    for inv in k:
        leng = 0
        try:
            l = json.loads(INV[inv]['Shape'].JSON)['paths'][0]
            leng = INV[inv]['Shape'].length/5280
        except:
            l = []
        #if not None in [p[3] for p in l]:
        if len(l)>2 and leng>=0.3:
            pntl = AddMidPoints(l,desd) 
            a = arcpy.Array(pntl)
            pl = arcpy.Polyline(a,arcpy.Describe(inp).spatialReference,True,True)
            #Curve = FindCurves(pl,DegMin,RMax,RMin,LenMin,desd)
            Curve = FindRadius(pl,DegMin,LenMin)[1]
            for i,cur in Curve.iterrows():
                R = abs(cur['Radius'])
                L = cur['EMP']-cur['BMP']
                if L<100.0/5280.0:
                    L = 100.0/5280.0
                if R<100:
                    R = 100
                CMF1 = (1.55*L+80.2/R)/(1.55*L)
                if CMF1<1:CMF1 =1
                CMF2 = 1 + 0.0626*(5730.0/R)**2
                if CMF2<1:CMF2 =1
                #if abs(cur['Radius'])<RMax and abs(cur['Radius'])<RMin:
                if min([CMF1,CMF2])>1.001 and L>0.2:
                
                    r = IC.newRow()
                    r.setValue(IDField,INV[inv]['INV'])
                    r.setValue('BEG_STA',cur['BMP'])
                    r.setValue('END_STA',cur['EMP'])
                    r.setValue('Radius',cur['Radius'])
                    r.setValue('CurveLen',cur['EMP']-cur['BMP'])
                    r.setValue('Center_X',cur['Cen_X'])
                    r.setValue('Center_Y',cur['Cen_Y'])
                    r.setValue('CMF_CH10',CMF1)
                    r.setValue('CMF_CH18',CMF2)
                    IC.insertRow(r)
        arcpy.SetProgressorPosition(INV.keys().index(inv))
        progressBar(INV.keys().index(inv),len(INV))
    del IC
def ImportIntAtt(Intersections,TrafficControl,Routes,RouteID,BMP,EMP,AttTable,Fields,Output,OutputTable):
    def FindAngle(O,P):
            import math
            if P[0] == O[0]:
                 if P[1] == O[1]:
                     #arcpy.AddWarning(str(O) + str(P))
                     return 0 #1
                 else:
                     if P[1] > O[1]:
                         return 90  #2
                     if P[1] < O[1]:
                         return 270 #3
            else:
                if P[1] == O[1]:
                    if P[0] > O[0]:
                        return 0 #4
                    else:
                        return 180 #5
                else:
                    if   (P[0] - O[0]) > 0 and (P[1] - O[1]) > 0:
                        return math.degrees(math.atan((P[1] - O[1]) / (P[0] - O[0]))) #6
                    elif (P[0] - O[0]) > 0 and (P[1] - O[1]) < 0:
                        return 360 - math.degrees(math.atan(-(P[1] - O[1]) / (P[0] - O[0]))) #7
                    elif (P[0] - O[0]) < 0 and (P[1] - O[1]) > 0:
                        return 180 - math.degrees(math.atan(-(P[1] - O[1]) / (P[0] - O[0]))) #8
                    elif (P[0] - O[0]) < 0 and (P[1] - O[1]) < 0:
                        return 180 + math.degrees(math.atan((P[1] - O[1]) / (P[0] - O[0])))
    def FindClosestPoint(PolylineList,IntPoint):
            n = len(PolylineList)
            Dist0 = ((PolylineList[0    ][0] - IntPoint[0]) ** 2 + (PolylineList[0    ][1] - IntPoint[1]) ** 2) ** 0.5
            Distn = ((PolylineList[n - 1][0] - IntPoint[0]) ** 2 + (PolylineList[n - 1][1] - IntPoint[1]) ** 2) ** 0.5
            if Dist0 <= Distn:
                return [PolylineList[0  ],PolylineList[1  ]]
            else:
                return [PolylineList[n-1],PolylineList[n-2]]
    
    Buffer = "80 Feet"
    Tolerance = "10 Feet"
    Int = hsmpy3.common.CreateOutPath(MainFile=Output,appendix='Int',Extension='')
    arcpy.Intersect_analysis(
        in_features = Routes,
        out_feature_class = Int, 
        join_attributes = "ALL", 
        cluster_tolerance = "-1 Unknown", 
        output_type = "POINT")

    SPJ = hsmpy3.common.CreateOutPath(MainFile=Output,appendix='SPJ',Extension='')
    arcpy.SpatialJoin_analysis(
        target_features = Int, 
        join_features = Intersections, 
        out_feature_class = SPJ, 
        join_operation = "JOIN_ONE_TO_ONE", 
        join_type = "KEEP_COMMON", 
        match_option = "CLOSEST", 
        search_radius = Buffer, 
        distance_field_name = "")

    arcpy.DeleteIdentical_management(
        in_dataset = SPJ, 
        fields = arcpy.Describe(SPJ).ShapeFieldName, 
        xy_tolerance = "", 
        z_tolerance = "0")

    OrgFields = [f.name for f in arcpy.ListFields(Intersections)]
    arcpy.DeleteField_management(SPJ,[f.name for f in arcpy.ListFields(SPJ) if not f.required and not f.name in OrgFields])

    arcpy.SpatialJoin_analysis(
        target_features = SPJ, 
        join_features = TrafficControl, 
        out_feature_class = Output, 
        join_operation = "JOIN_ONE_TO_ONE", 
        join_type = "KEEP_COMMON", 
        match_option = "CLOSEST", 
        search_radius = Buffer, 
        distance_field_name = "")

    OrgFields.extend(['TRAF_CONT','LEG_COUNT','PeerGroup_CH2M_TJM'])
    arcpy.DeleteField_management(Output,[f.name for f in arcpy.ListFields(Output) if not f.required and not f.name in OrgFields])

    EventTable = hsmpy3.common.CreateOutPath(MainFile=Output,appendix='EventTable',Extension='')
    arcpy.LocateFeaturesAlongRoutes_lr(
        in_features                = Output, 
        in_routes                = Routes, 
        route_id_field            = RouteID, 
        radius_or_tolerance        = Tolerance, 
        out_table                = EventTable, 
        out_event_properties    = " ".join([RouteID, "POINT", "MP"]),
        route_locations            = "ALL", 
        in_fields                = "FIELDS", 
        m_direction_offsetting    = "M_DIRECTON"
        )

    # Milepost Correction
    EMPDict = {r.getValue(RouteID):r.getValue('Shape').lastPoint.M for r in arcpy.SearchCursor(Routes)}
    r = 0 
    uc = arcpy.UpdateCursor(EventTable)
    for r in uc:
        inv = r.getValue(RouteID)
        MP = r.getValue('MP')
        if MP<0:
            r.setValue('MP',0)
            uc.updateRow(r)
        if MP>EMPDict[inv]:
            r.setValue('MP',EMPDict[inv])
            uc.updateRow(r)
    del uc, r

    AllF = [f.name for f in arcpy.ListFields(AttTable)]
    MF = [f for f in Fields if not f in AllF]
    if not MF == []:
        print(str(MF) + ' not found in ' + AttTable)
    IRIS_Diss = hsmpy3.common.CreateOutPath(MainFile=Output,appendix='diss',Extension='')
    arcpy.DissolveRouteEvents_lr(
        in_events = AttTable, 
        in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
        dissolve_field = ';'.join(Fields), 
        out_table = IRIS_Diss, 
        out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
        dissolve_type="DISSOLVE", 
        build_index="INDEX"
        )

    arcpy.OverlayRouteEvents_lr(
        in_table = EventTable , 
        in_event_properties = ' '.join([RouteID,'POINT','MP']), 
        overlay_table = IRIS_Diss, 
        overlay_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
        overlay_type = "INTERSECT", 
        out_table = OutputTable, 
        out_event_properties = ' '.join([RouteID,'POINT','MP']),  
        in_fields = "FIELDS", 
        build_index="INDEX"
        ) 
    
    hsmpy3.common.AddField(Output, [
        fields_SC.intr.AADT_Major,
        fields_SC.intr.AADT_Minor,
        fields_SC.crash.ABuffer,
        fields_SC.crash.BBuffer
        ])

    arcpy.AddField_management(OutputTable,'ApprType','TEXT')
    #arcpy.AddField_management(OutputTable,'ApprDeg','Double')
    Approach = {r.getValue('SiteID'):[] for r in arcpy.SearchCursor(Output)}

    OID = arcpy.Describe(OutputTable).OIDFieldName
    for r in arcpy.SearchCursor(OutputTable):
        k = r.getValue('SiteID')
        if k in Approach.keys():
            Approach[k].append({
                'OID':r.getValue(OID),
                'INV':r.getValue(RouteID),
                'AADT':common.GetIntVal(r,'AADT'),
                'Lanes':common.GetIntVal(r,'LNS',2),
                'Urban':r.getValue('URBAN'),
                'SurfWid':common.GetFloatVal(r,'SURF_WTH',24),
                'MedWid':common.GetFloatVal(r,'MED_WTH')
                })
    for k in Approach.keys():
        AADT = [i['AADT'] for i in Approach[k]]
        INV = [i['INV'] for i in Approach[k]]
        major_i = AADT.index(max(AADT))
        major_inv = INV[major_i]
        for i,appr in enumerate(Approach[k]):
            if appr['AADT'] == max(AADT) or appr['INV']==major_inv:
                Approach[k][i].update({'ApprType':'Major'})
            else:
                Approach[k][i].update({'ApprType':'Minor'})

    UC = arcpy.UpdateCursor(OutputTable)
    for r in UC:
        k = r.getValue('SiteID')
        o = r.getValue(OID)
        Type = ''
        for appr in Approach[k]:
            if appr['OID'] == o:
                Type = appr['ApprType']
        r.setValue('ApprType',Type)

        UC.updateRow(r)
                    
    UC = arcpy.UpdateCursor(Output)
    for r in UC:
        k = r.getValue('SiteID')
        try:r.setValue(fields_SC.intr.AADT_Major['name'],max([appr['AADT'] for appr in Approach[k] if appr['ApprType']=='Major']))
        except:r.setValue(fields_SC.intr.AADT_Major['name'],0)
        try:r.setValue(fields_SC.intr.AADT_Minor['name'],max([appr['AADT'] for appr in Approach[k] if appr['ApprType']=='Minor']))
        except:r.setValue(fields_SC.intr.AADT_Minor['name'],0)
        try:W_Major = max([appr['SurfWid'] + appr['MedWid'] for appr in Approach[k] if appr['ApprType']=='Major'])
        except:W_Major = 24
        try:W_Minor = max([appr['SurfWid'] + appr['MedWid'] for appr in Approach[k] if appr['ApprType']=='Minor'])
        except:W_Minor = 24
        ABuffer = max(1.2 * (W_Major**2+W_Minor**2) ** 0.5,50)
        r.setValue(fields_SC.crash.ABuffer['name'],ABuffer)
        r.setValue(fields_SC.crash.BBuffer['name'],max(ABuffer,250))
        AADT = [i['AADT'] for i in Approach[k]]
        major_i = AADT.index(max(AADT))
        LaneMajor = [i['Lanes'] for i in Approach[k]][0]
        UC.updateRow(r)

    arcpy.Delete_management(Int)
    arcpy.Delete_management(EventTable)
    arcpy.Delete_management(SPJ)
    arcpy.Delete_management(IRIS_Diss)
def CON_ExtractCurves(WDir,HSMPY_PATH,IRIS_Routes,IRIS_Table,Curve_Table,CurveLayer,Overlay_Table,OverlayLayer,Title):
    import sys, os, subprocess

    pyFN = os.path.join(WDir , 'CurveExtract_' + str(Title) + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """print("Curve Extract")
from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
#atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
IRIS_Routes = r"{}"
IRIS_Table = r"{}"
Curve_Table = r"{}"
CurveLayer = r"{}"
Overlay_Table = r"{}"
OverlayLayer = r"{}"

sys.path.append(HSMPY_PATH)
import arcpy
import hsmpy

print(Curve_Table)
hsmpy.network.ExtractCurves(inp=IRIS_Routes,IDField='INVENTORY',DegMin=2,RMax=5280,RMin=10,LenMin=1000,desd=1000, out=Curve_Table)
print()

F = [f.name for f in arcpy.ListFields(Curve_Table) if not f.required and not f.name in ['INVENTORY','BEG_STA','END_STA']]
print(CurveLayer)
hsmpy.network.CreateRouteEventLayer(Sites_Routes=IRIS_Routes,AttTable=Curve_Table,BMP='BEG_STA',EMP='END_STA',RouteID='INVENTORY',Fields=F,Output=CurveLayer)

print(Overlay_Table)
arcpy.OverlayRouteEvents_lr(in_table = IRIS_Table, 
                                in_event_properties = ' '.join(['INVENTORY','LINE','BEG_STA','END_STA']), 
                                overlay_table = Curve_Table, 
                                overlay_event_properties = ' '.join(['INVENTORY','LINE','BEG_STA','END_STA']), 
                                overlay_type = "UNION", 
                                out_table = Overlay_Table, 
                                out_event_properties = ' '.join(['INVENTORY','LINE','BEG_STA','END_STA']), 
                                zero_length_events = "NO_ZERO", 
                                in_fields = "FIELDS", 
                                build_index="INDEX") 

print(OverlayLayer)
F = [f.name for f in arcpy.ListFields(Overlay_Table) if not f.required and not f.name in ['INVENTORY','BEG_STA','END_STA']]
hsmpy.network.CreateRouteEventLayer(Sites_Routes=IRIS_Routes,AttTable=Overlay_Table,BMP='BEG_STA',EMP='END_STA',RouteID='INVENTORY',Fields=F,Output=OverlayLayer)

print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,
           IRIS_Routes,
           IRIS_Table,
           Curve_Table,
           CurveLayer,
           Overlay_Table,
           OverlayLayer)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess  = subprocess.Popen([sys.executable, pyFN],shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)
def CON_ImportRoadwayData(WDir,HSMPY_PATH,Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    SubProcess = []
    PyList = []
    pyFN = os.path.join(WDir , os.path.basename(Output) + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import arcpy
import atexit
atexit.register(input, 'Press Enter to continue...')
sys.path.append(r'{}') #1
import hsmpy
Input = r"{}"
Route = r"{}"
AttTable = r"{}"
Fields = {}
Output = r"{}"
RouteID = "{}"
BMP = "{}"
EMP = "{}"
XY_Tolerance = "{}"
print("Roadway Attributes")
print(Output)
hsmpy.network.ImportRoadwayData(Input,Route,AttTable,Fields,Output,
                                    RouteID,BMP,EMP,XY_Tolerance)
hsmpy.network.PrintSegSummary(Output)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance)
    OutFile.write(pyfile)
    OutFile.close()
    PyList.append(pyFN)
    for py in PyList:
        SubProcess.append(subprocess.Popen(
                [sys.executable, py],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE))  
    return(SubProcess[0])
def CON_ImportRoadwayData_Temporal(WDir,HSMPY_PATH,Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance,Title,INVENTORY_I=''):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_RoadwayAtt.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
#atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Input = r"{}"
Route = {}
AttTable = {}
Fields = {}
Output = {}
RouteID = "{}"
BMP = "{}"
EMP = "{}"
XY_Tolerance = "{}"
INV_I = "{}"
Title = "{}"

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
print("Roadway Attributes")
for year in Output.keys():
    print(Output[year])
    hsmpy3.network.ImportRoadwayData(Input,Route[year],AttTable[year],Fields,Output[year],
                                    RouteID,BMP,EMP,XY_Tolerance,INV_I)
    hsmpy3.network.PrintSegSummary(Output[year],Title+'_'+str(year))
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance,INVENTORY_I,Title)
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
def CON_ImportIntData_Temporal(WDir,HSMPY_PATH,Input,TrafficControl,Routes,RouteID,BMP,EMP,AttTable,Fields,Output,OutpuTable,Title):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'HSIP_' + str(Title) + '_IntAtt.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
#atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Input = r"{}"
TrafficControl = {}
Routes = {}
RouteID = "{}"
BMP = "{}"
EMP = "{}"
AttTable = {}
Fields = {}
Output = {}
OutputTable = {}

print("Intersection Attributes")

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
for year in Output.keys():
    print(Output[year])
    hsmpy3.network.ImportIntAtt(Input,TrafficControl[year],Routes[year],RouteID,BMP,EMP,AttTable[year],Fields,Output[year],OutputTable[year])
    hsmpy3.network.PrintIntSummary(Output[year],OutputTable[year],year)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Input,TrafficControl,Routes,RouteID,BMP,EMP,AttTable,Fields,Output,OutpuTable)
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
def CON_ExtractIntFromSeg(WDir,HSMPY_PATH,Segments,Intersections,Buffer,Output,Title=''):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'ExtractIntBuff_' + str(Title) + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
#atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Segments = r"{}"
Intersections = r"{}"
Buffer = "{}"
Output = r"{}"

print("Extract Intersection buffer from Segments")

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
hsmpy3.network.ExtractIntFromSeg(Segments,Intersections,Buffer,Output)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Segments,Intersections,Buffer,Output)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN])
                #shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)

def ImportRoadwayData_old1(Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance):
    #Output should be on a GDB not a shapefile

    #Step 1: Create a route FC based on the input 
    RID_List = list(set([r.getValue(RouteID) for r in arcpy.SearchCursor(Input)]))
    Input_Layer = common.CreateOutLayer('InputLayer'+str(np.random.normal()))
    Route_Layer = common.CreateOutLayer('RouteLayer'+str(np.random.normal()))
    arcpy.MakeFeatureLayer_management(Route,Route_Layer)
    arcpy.MakeFeatureLayer_management(Input,Input_Layer)
    Sites_Event_Table = common.CreateOutPath(MainFile=Output,appendix='EventTab',Extension='')
    for rid in RID_List:
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = Route_Layer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = RouteID + " = '" + rid + "'")
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = Input_Layer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = RouteID + " = '" + rid + "'")
        Sites_Event_Table_T = common.CreateOutPath(MainFile=Output,appendix='EventTab_T',Extension='')
        arcpy.LocateFeaturesAlongRoutes_lr(in_features = Input, 
                                       in_routes = Route, 
                                       route_id_field = RouteID, 
                                       radius_or_tolerance = XY_Tolerance, 
                                       out_table = Sites_Event_Table, 
                                       out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                       route_locations = "ALL", 
                                       distance_field = "DISTANCE", 
                                       zero_length_events = "ZERO", 
                                       in_fields = "FIELDS", 
                                       m_direction_offsetting = "M_DIRECTON")
        if RID_List.index(rid)>0:
            arcpy.Merge_management(inputs=abs,output=o)
        arcpy.CopyRows_management()
    arcpy.Delete_management(Input_Layer)
    arcpy.Delete_management(Route_Layer)
    Sites_Event_Layer = common.CreateOutLayer('EventLayer')
    arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
                                 route_id_field = RouteID, 
                                 in_table = Sites_Event_Table, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 out_layer = Sites_Event_Layer, 
                                 add_error_field="NO_ERROR_FIELD")
    
    Sites_Routes = common.CreateOutPath(MainFile=Output,appendix='route',Extension='')
    arcpy.CopyFeatures_management(in_features = Sites_Event_Layer,
                                  out_feature_class = Sites_Routes)
    
    IRIS_Diss = common.CreateOutPath(MainFile=Output,appendix='diss',Extension='')
    arcpy.DissolveRouteEvents_lr(in_events = AttTable, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_field = ';'.join(Fields), 
                                 out_table = IRIS_Diss, 
                                 out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_type="DISSOLVE", 
                                 build_index="INDEX")    
    
    Overlay_Event_Table1 = common.CreateOutPath(MainFile=Output,appendix='OverlayTab1',Extension='')
    arcpy.OverlayRouteEvents_lr(in_table = IRIS_Diss, 
                                in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                overlay_table = Sites_Event_Table, 
                                overlay_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                overlay_type = "INTERSECT", 
                                out_table = Overlay_Event_Table1, 
                                out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                zero_length_events = "NO_ZERO", 
                                in_fields = "FIELDS", 
                                build_index="INDEX")    
    
    Overlay_Event_Layer = common.CreateOutLayer('OverlayEventLayer')
    arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
                                 route_id_field = RouteID, 
                                 in_table = Overlay_Event_Table1, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 out_layer = Overlay_Event_Layer, 
                                 offset_field = "", 
                                 add_error_field = "ERROR_FIELD")     
    
    Sites_segs1 = common.CreateOutPath(MainFile=Output,appendix='seg1',Extension='')
    arcpy.CopyFeatures_management(in_features = Overlay_Event_Layer,
                                  out_feature_class = Sites_segs1)


    #Curves_Table = common.CreateOutPath(MainFile=Output,appendix='curves',Extension='')
    #ExtractCurves(inp=Sites_segs1,IDField=RouteID,RMax=5280,RMin=10,DegMin=2,desd=1000,LenMin=1000,out=Curves_Table)

    #Overlay_Event_Table2 = common.CreateOutPath(MainFile=Output,appendix='OverlayTab2',Extension='')
    #arcpy.OverlayRouteEvents_lr(in_table = Overlay_Event_Table1, 
    #                            in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            overlay_table = Curves_Table, 
    #                            overlay_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            overlay_type = "UNION", 
    #                            out_table = Overlay_Event_Table2, 
    #                            out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            zero_length_events = "NO_ZERO", 
    #                            in_fields = "FIELDS", 
    #                            build_index="INDEX") 

    #Overlay_Event_Layer2 = common.CreateOutLayer('OverlayEventLayer2')
    #arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
    #                             route_id_field = RouteID, 
    #                             in_table = Overlay_Event_Table2, 
    #                             in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                             out_layer = Overlay_Event_Layer2, 
    #                             offset_field = "", 
    #                             add_error_field = "ERROR_FIELD") 
    
    Sort = common.CreateOutPath(MainFile=Output,appendix='sort',Extension='')
    arcpy.Sort_management(in_dataset = Sites_segs1,
                          out_dataset = Sort,
                          sort_field = ';'.join([RouteID,BMP,EMP]))
    Final_Layer = common.CreateOutLayer('FinalLayer')
    
    arcpy.MakeFeatureLayer_management(in_features=Sort,out_layer=Final_Layer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = Final_Layer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "Shape_Length > 52")
    
    arcpy.Delete_management(Output)
    arcpy.MultipartToSinglepart_management(in_features=Final_Layer, 
                                           out_feature_class=Output)    
    arcpy.DeleteField_management(Output,'ORIG_FID')
    FL = [f.name for f in arcpy.ListFields(Output) if f.name != arcpy.Describe(Output).OIDFieldName]
    arcpy.DeleteIdentical_management(in_dataset = Output, 
                                     fields = ';'.join(FL), 
                                     xy_tolerance = "", 
                                     z_tolerance = "0")


    arcpy.Delete_management(Sites_Event_Table)
    arcpy.Delete_management(Sites_Event_Layer)
    arcpy.Delete_management(Sites_Routes)
    arcpy.Delete_management(IRIS_Diss)
    arcpy.Delete_management(Overlay_Event_Table1)
    arcpy.Delete_management(Overlay_Event_Layer)
    arcpy.Delete_management(Sites_segs1)
    #arcpy.Delete_management(Curves_Table)
    #arcpy.Delete_management(Overlay_Event_Table2)
    #arcpy.Delete_management(Overlay_Event_Layer2)
    arcpy.Delete_management(Sort)
    arcpy.Delete_management(Final_Layer)
def ImportRoadwayData(Input,Route,AttTable,Fields,Output,RouteID,BMP,EMP,XY_Tolerance,RouteID_I=''):
    #Output should be on a GDB not a shapefile

    #Step 1: Create a route FC based on the input 
    Sites_Event_Table = common.CreateOutPath(MainFile=Output,appendix='EventTab',Extension='')
    if RouteID_I=='':
        arcpy.LocateFeaturesAlongRoutes_lr(in_features = Input, 
                                       in_routes = Route, 
                                       route_id_field = RouteID, 
                                       radius_or_tolerance = XY_Tolerance, 
                                       out_table = Sites_Event_Table, 
                                       out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                       route_locations = "FIRST", 
                                       distance_field = "DISTANCE", 
                                       zero_length_events = "ZERO", 
                                       in_fields = "FIELDS", 
                                       m_direction_offsetting = "M_DIRECTON")
    else:
        arcpy.LocateFeaturesAlongRoutes_lr(in_features = Input, 
                                       in_routes = Route, 
                                       route_id_field = RouteID, 
                                       radius_or_tolerance = XY_Tolerance, 
                                       out_table = Sites_Event_Table, 
                                       out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                       route_locations = "ALL", 
                                       distance_field = "DISTANCE", 
                                       zero_length_events = "ZERO", 
                                       in_fields = "FIELDS", 
                                       m_direction_offsetting = "M_DIRECTON")
        Sites_Event_Table_Layer = common.CreateOutLayer('EventTableLayer')
        #arcpy.MakeFeatureLayer_management(Sites_Event_Table,Sites_Event_Table_Layer)
        arcpy.MakeTableView_management (in_table=Sites_Event_Table, out_view=Sites_Event_Table_Layer)
        arcpy.SelectLayerByAttribute_management(in_layer_or_view = Sites_Event_Table_Layer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = RouteID + " = " + RouteID_I )
        Sites_Event_Table = Sites_Event_Table_Layer
    Sites_Event_Layer = common.CreateOutLayer('EventLayer')
    arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
                                 route_id_field = RouteID, 
                                 in_table = Sites_Event_Table, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 out_layer = Sites_Event_Layer, 
                                 add_error_field="NO_ERROR_FIELD")
    
    Sites_Routes = common.CreateOutPath(MainFile=Output,appendix='route',Extension='')
    arcpy.CopyFeatures_management(in_features = Sites_Event_Layer,
                                  out_feature_class = Sites_Routes)
    
    IRIS_Diss = common.CreateOutPath(MainFile=Output,appendix='diss',Extension='')
    arcpy.DissolveRouteEvents_lr(in_events = AttTable, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_field = ';'.join(Fields), 
                                 out_table = IRIS_Diss, 
                                 out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 dissolve_type="DISSOLVE", 
                                 build_index="INDEX")    
    
    Overlay_Event_Table1 = common.CreateOutPath(MainFile=Output,appendix='OverlayTab1',Extension='')
    arcpy.OverlayRouteEvents_lr(in_table = IRIS_Diss, 
                                in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                overlay_table = Sites_Event_Table, 
                                overlay_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                overlay_type = "INTERSECT", 
                                out_table = Overlay_Event_Table1, 
                                out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                zero_length_events = "NO_ZERO", 
                                in_fields = "FIELDS", 
                                build_index="INDEX")    
    
    Overlay_Event_Layer = common.CreateOutLayer('OverlayEventLayer')
    arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
                                 route_id_field = RouteID, 
                                 in_table = Overlay_Event_Table1, 
                                 in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
                                 out_layer = Overlay_Event_Layer, 
                                 offset_field = "", 
                                 add_error_field = "ERROR_FIELD")     
    
    Sites_segs1 = common.CreateOutPath(MainFile=Output,appendix='seg1',Extension='')
    arcpy.CopyFeatures_management(in_features = Overlay_Event_Layer,
                                  out_feature_class = Sites_segs1)


    #Curves_Table = common.CreateOutPath(MainFile=Output,appendix='curves',Extension='')
    #ExtractCurves(inp=Sites_segs1,IDField=RouteID,RMax=5280,RMin=10,DegMin=2,desd=1000,LenMin=1000,out=Curves_Table)

    #Overlay_Event_Table2 = common.CreateOutPath(MainFile=Output,appendix='OverlayTab2',Extension='')
    #arcpy.OverlayRouteEvents_lr(in_table = Overlay_Event_Table1, 
    #                            in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            overlay_table = Curves_Table, 
    #                            overlay_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            overlay_type = "UNION", 
    #                            out_table = Overlay_Event_Table2, 
    #                            out_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                            zero_length_events = "NO_ZERO", 
    #                            in_fields = "FIELDS", 
    #                            build_index="INDEX") 

    #Overlay_Event_Layer2 = common.CreateOutLayer('OverlayEventLayer2')
    #arcpy.MakeRouteEventLayer_lr(in_routes = Route, 
    #                             route_id_field = RouteID, 
    #                             in_table = Overlay_Event_Table2, 
    #                             in_event_properties = ' '.join([RouteID,'LINE',BMP,EMP]), 
    #                             out_layer = Overlay_Event_Layer2, 
    #                             offset_field = "", 
    #                             add_error_field = "ERROR_FIELD") 
    
    Sort = common.CreateOutPath(MainFile=Output,appendix='sort',Extension='')
    arcpy.Sort_management(in_dataset = Sites_segs1,
                          out_dataset = Sort,
                          sort_field = ';'.join([RouteID,BMP,EMP]))
    Final_Layer = common.CreateOutLayer('FinalLayer')
    
    arcpy.MakeFeatureLayer_management(in_features=Sort,out_layer=Final_Layer)
    arcpy.SelectLayerByAttribute_management(in_layer_or_view = Final_Layer,
                                            selection_type = 'NEW_SELECTION',
                                            where_clause = "Shape_Length > 52")
    
    arcpy.Delete_management(Output)
    arcpy.MultipartToSinglepart_management(in_features=Final_Layer, 
                                           out_feature_class=Output)    
    arcpy.DeleteField_management(Output,'ORIG_FID')
    FL = [f.name for f in arcpy.ListFields(Output) if f.name != arcpy.Describe(Output).OIDFieldName]
    arcpy.DeleteIdentical_management(in_dataset = Output, 
                                     fields = ';'.join(FL), 
                                     xy_tolerance = "", 
                                     z_tolerance = "0")


    arcpy.Delete_management(Sites_Event_Table)
    arcpy.Delete_management(Sites_Event_Layer)
    arcpy.Delete_management(Sites_Routes)
    arcpy.Delete_management(IRIS_Diss)
    arcpy.Delete_management(Overlay_Event_Table1)
    arcpy.Delete_management(Overlay_Event_Layer)
    arcpy.Delete_management(Sites_segs1)
    #arcpy.Delete_management(Curves_Table)
    #arcpy.Delete_management(Overlay_Event_Table2)
    #arcpy.Delete_management(Overlay_Event_Layer2)
    arcpy.Delete_management(Sort)
    arcpy.Delete_management(Final_Layer)


def PolylineToDF(pl):
    df = pd.DataFrame(columns=['PartNumber','BMP','EMP','Diff','Mileage','Shape'])
    for i,prt in enumerate(pl):
        M = [pnt.M for pnt in prt]
        df.loc[i] = [i,M[0],M[-1],M[-1]-M[0]-arcpy.Polyline(prt).length/5280,arcpy.Polyline(prt).length/5280,prt]
    return(df)
def UnsplitParts(df,Tolerance,SpatRef):
    df.index = np.arange(0, len(df) )
    df['FP'] = [s[0] for s in df.Shape]
    df['LP'] = [s[-1] for s in df.Shape]
    df = df.sort_values('BMP')
    df['Spread'] = -1
    df['Continuous'] = 0
    for i,r in df.iterrows():
        if i==df.shape[0]-1:
            continue
        if r.EMP==df.loc[i+1]['BMP']:
            d = hsmpy3.common.Distance(x1=r.LP.X,y1=r.LP.Y,x2=df.loc[i+1]['FP'].X,y2=df.loc[i+1]['FP'].Y)
            df.set_value(i,'Spread',d)
            if d<Tolerance:
                df.set_value(i,'Continuous',1)
                #mp = arcpy.Multipoint(arcpy.Array([r.LP,df.loc[i+1]['FP']])).centeroid
    df['MergeID'] = -1
    m = 1
    for i,r in df.iterrows():
        df.set_value(i,'MergeID',m)
        if r.Continuous==0:
            m += 1
    mdf = pd.DataFrame(columns=['BMP','EMP','Shape'])
    ml = list(set(df.MergeID))
    ml.sort()
    for m in ml:
        rdf = df[df.MergeID==m]
        pntL = []
        rdf.index = range(1,rdf.shape[0]+1)
        for i,r in rdf.iterrows():
            if i==1 and rdf.shape[0]==1:
                pntL.extend([pnt for pnt in r.Shape])
            elif i==1 and rdf.shape[0]>1:
                pntL.extend([pnt for pnt in r.Shape][:-1])
            elif i == rdf.shape[0] and rdf.shape[0]>1:
                pntL.extend([pnt for pnt in r.Shape])
            else:
                pntL.extend([pnt for pnt in r.Shape][:-1])

        pl = arcpy.Polyline(arcpy.Array(pntL),SpatRef,False,True)
        M = [pnt.M for pnt in pntL]
        mdf.loc[m] = [M[0],M[-1],arcpy.Array(pntL)]
    a = arcpy.Array(list(mdf.Shape))
    return(arcpy.Polyline(a,SpatRef,True,True))
def MergeOverlappingParts(df):
    df.index = np.arange(0, len(df) )
    df['FP'] = [s.firstPoint for s in df.Shape]
    df['LP'] = [s.lastPoint for s in df.Shape]
    df = df.sort_values('BMP')
    df['Overlapping'] = -1
    for i,r in df.iterrows():
        if i==df.shape[0]-1:
            continue
        if r.EMP>df.loc[i+1]['BMP']:
            ip = r.Shape.intersect(df.loc[i+1]['Shape'],2)
            df.set_value(i,'Overlapping',ip.length)
    df['MergeID'] = -1
    m = 1
    for i,r in df.iterrows():
        df.set_value(i,'MergeID',m)
        if r.Overlapping<=0:
            m += 1
    mdf = pd.DataFrame(columns=['BMP','EMP','Shape'])
    ml = list(set(df.MergeID))
    ml.sort()
    for m in ml:
        rdf = df[df.MergeID==m]
        plL = list(rdf.Shape)
        upl = plL[0]
        for pl in plL[1:]:
            upl = upl.union(pl)
        #prt = UnionPrts([s[0] for s in rdf.Shape])
        prt = upl[0]
        M = [pnt.M for pnt in prt]
        mdf.loc[m] = [M[0],M[-1],prt]
    return(mdf)
def PlotPolylines(List,anotate = False):
    size = 25
    plt.figure(figsize=(size,size))
    for l in List:
        x = [i.X for i in l]
        y = [i.Y for i in l]
        plt.plot(x, y,'-')
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off') # labels along the bottom edge are off
    plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        right='off',         # ticks along the top edge are off
        labelleft='off') # labels along the bottom edge are off
    if anotate:
        for l in List:    
            x = [i.X for i in l]
            y = [i.Y for i in l]
            for i in range(len(l)):
                plt.annotate(str(i),(x[i],y[i]))    
    for l in List:    
        x = list(l)[0].X
        y = list(l)[0].Y
        m = list(l)[0].M
        plt.annotate(m,(x,y))    
        x = list(l)[-1].X
        y = list(l)[-1].Y
        m = list(l)[-1].M
        plt.annotate(m,(x,y))    

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
def ParttoDF(prt):
    df = pd.DataFrame(columns=['ID','X','Y','Z','M'])
    for i,pnt in enumerate(prt):
        df.loc[i] = [i,pnt.X,pnt.Y,pnt.Z,pnt.M]
    return(df)
def CreateRoutes(Input,RID,BMP,EMP,SpatRef,Tolerance,Output):
    print('[{}] {} to pandas:'.format(strftime("%Y-%m-%d %H:%M:%S"),os.path.basename(Input)))
    df  = common.FCtoDF(Input,readGeometry=True,selectedFields=[RID,BMP,EMP])
    df = df.rename(columns = {RID:'RID',BMP:'BMP',EMP:'EMP'})
    df['EMP'] = df.EMP.astype(float)
    df['BMP'] = df.BMP.astype(float)
    df['RID'] = df.RID.astype(str)
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape[0]))

    print('[{}] droping duplicates:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    s1 = df.shape[0]
    df = df.drop_duplicates(subset=['RID','BMP','EMP'])
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),s1-df.shape[0]))

    print('[{}] droping zero length:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    shape = arcpy.Describe(Input).shapeFieldName
    df['ShapeLength'] = [s.length for s in df[shape]]
    s1 = df.shape[0]
    df = df[df.ShapeLength>0]
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),s1-df.shape[0]))

    print('[{}] droping overlaps:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    s1 = df.shape[0]
    df['Diff'] = df.EMP - df.BMP
    df['FlagForRemove'] = 0
    df = df.sort_values(by=['RID','Diff'],ascending=[True,False])
    vdf = pd.DataFrame(df.RID.value_counts())
    vdf = vdf[vdf.RID>1]
    ridL = list(vdf.index)
    for rid in ridL:
        rdf = df[df.RID==rid]
        for j,k in rdf.iterrows():
            zdf = rdf[(rdf.BMP<=k.BMP) & (rdf.EMP>=k.EMP)]
            if zdf.shape[0]>1:
                df.set_value(j,'FlagForRemove',1)
    df = df[df.FlagForRemove==0]
    df = df[['RID','BMP','EMP','Shape']]
    df = df.sort_values(['RID','BMP'])
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),s1-df.shape[0]))

    print('[{}] create feature class:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    IC = common.CreateOutPath(os.path.dirname(Output) + '\\CR_ic',strftime("%Y%m%d_%H%M%S"),'')
    arcpy.management.CreateFeatureclass(out_name = os.path.basename(IC),
                                        out_path = os.path.dirname(IC),
                                        spatial_reference=SpatRef,
                                        geometry_type='Polyline',
                                        has_m='ENABLED',
                                        has_z='DISABLED')
    arcpy.AddField_management(IC,'RID','Text')
    arcpy.AddField_management(IC,'BMP','Double')
    arcpy.AddField_management(IC,'EMP','Double')
    ic = arcpy.InsertCursor(IC)
    for i,r in df.iterrows():
                Pl =  r.Shape
                row = ic.newRow()
                row.setValue('RID',int(i))
                row.setValue('BMP',float(r.BMP))
                row.setValue('EMP',float(r.EMP))
                row.shape = Pl
                ic.insertRow(row)
    del ic
    del row
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.management.GetCount(IC))))

    print('[{}] create routes:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    R = hsmpy3.common.CreateOutPath(os.path.dirname(Output) + '\\CR_route',strftime("%Y%m%d_%H%M%S"),'')
    arcpy.lr.CreateRoutes(
        in_line_features    = IC,
        route_id_field      = 'RID',
        out_feature_class   = R,
        measure_source      = "TWO_FIELDS", 
        from_measure_field  = 'BMP', 
        to_measure_field    = 'EMP', 
        measure_factor      = "1", 
        measure_offset      = "0", 
        build_index         = "INDEX"
    )
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),int(str(arcpy.management.GetCount(R)))))

    print('[{}] generalize'.format(strftime("%Y-%m-%d %H:%M:%S")))
    arcpy.Generalize_edit (in_features =R, tolerance = "0.001 Feet")

    print('[{}] multi to single part:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    #RSP = hsmpy3.common.CreateOutPath(os.path.dirname(Output) + '\\CR_route_mp2sp',strftime("%Y%m%d_%H%M%S"),'')
    #arcpy.management.MultipartToSinglepart(in_features=R,out_feature_class=RSP)
    RSP = R
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.management.GetCount(RSP))))

    print('[{}] fc to pandas:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    rdf = hsmpy3.common.FCtoDF(RSP,readGeometry=True,selectedFields=['RID'])
    rdf['RShape'] = rdf[arcpy.Describe(RSP).shapeFieldName]
    rdf['RID'] = rdf.RID.astype(int)
    rdf = rdf.sort_values('RID')
    rdf.index = list(rdf.RID)
    rdf = rdf[['RShape']]
    df = pd.concat([rdf,df[['RID']]],axis=1)
    df['BMP'] = [pl.firstPoint.M for pl in list(df.RShape)]
    df['EMP'] = [pl.lastPoint.M for pl in list(df.RShape)]
    df = df.sort_values(['RID','BMP','EMP'])
    df.columns = ['Shape','RID','BMP','EMP']
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),rdf.shape[0]))

    print('[{}] unsplit & merge overlaps:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    vdf = pd.DataFrame(df.RID.value_counts())
    RIDs = list(vdf[vdf.RID==1].index)
    RIDm = list(vdf[vdf.RID>1].index)
    fdf = pd.DataFrame(columns=['Shape'])
    sdf = df[df.RID.isin(RIDs)].copy(deep=True)
    sdf.index = sdf['RID']
    fdf['Shape'] = sdf.loc[RIDs,'Shape']
    fdf.index = RIDs
    for rid in RIDm:
        rdf = df[df.RID==rid].copy(deep=True)
        rdf = MergeOverlappingParts(rdf) 
        pl = UnsplitParts(rdf,Tolerance,SpatRef)
        fdf.set_value(rid,'Shape',pl) 
    fdf = fdf.sort_index()
    fdf['BMP'] = [s.firstPoint.M for s in fdf.Shape]
    fdf['EMP'] = [s.lastPoint.M for s in fdf.Shape]
    fdf['partCount'] = [s.partCount for s in fdf.Shape]
    fdf['ShapeLength'] = [s.length for s in fdf.Shape]
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),fdf.shape[0]))

    print('[{}] create feature class:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    try:
        arcpy.management.Delete(Output)
    except:pass
    arcpy.management.CreateFeatureclass(out_name = os.path.basename(Output),
                                        out_path = os.path.dirname(Output),
                                        spatial_reference=SpatRef,
                                        geometry_type='Polyline',
                                        has_m='ENABLED',
                                        has_z='DISABLED')
    arcpy.AddField_management(Output,RID,'Text')
    arcpy.AddField_management(Output,BMP,'Double')
    arcpy.AddField_management(Output,EMP,'Double')
    arcpy.AddField_management(Output,'partCount','Long')
    ic = arcpy.InsertCursor(Output)
    for i,r in fdf.iterrows():
                Pl =  r.Shape
                row = ic.newRow()
                row.setValue(RID,i)
                row.setValue(BMP,float(r.BMP))
                row.setValue(EMP,float(r.EMP))
                row.setValue('partCount',int(r.partCount))
                row.shape = Pl
                ic.insertRow(row)
    del ic
    del row
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),str(arcpy.management.GetCount(Output))))
    arcpy.management.Delete(R)
    arcpy.management.Delete(IC)

    return(Output)
def CON_CreateRoutes(WDir,HSMPY_PATH,Input,RID,BMP,EMP,SpatRef,Tolerance,Output,Title=''):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'CreateRoutes_' + str(Title) + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Input = r"{}"
RID = "{}"
BMP = "{}"
EMP = "{}"
SpatRef = {}
Tolerance = {}
Output = r"{}"

print("Create Routes")

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
hsmpy3.network.CreateRoutes(Input,RID,BMP,EMP,arcpy.arcpy.SpatialReference(SpatRef),Tolerance,Output)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Input,RID,BMP,EMP,SpatRef,Tolerance,Output)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)

def CreateIntPoints(Routes,Project_GDB,BridgeDF,SignalsDF,IntFC_Out,AppCSV_Out):
    RouteID = "ROUTE_ID"
    BEG_STA = 'BEG_POINT'
    END_STA = 'END_POINT'

    #print('[{}] Extend Line:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    #Tolerance = "15 Feet"
    #EL = hsmpy3.common.CreateOutPath(Project_GDB + '\\' + os.path.basename(Routes),'EL','')
    #arcpy.management.CopyFeatures(Routes,EL)
    #arcpy.ExtendLine_edit(EL, Tolerance, "FEATURE")

    print('[{}] Feature to Line:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Tolerance = "5 Feet"
    F2L = hsmpy3.common.CreateOutPath(Project_GDB + '\\' + os.path.basename(Routes),'F2L','')
    arcpy.management.FeatureToLine(in_features=Routes,out_feature_class=F2L,attributes="ATTRIBUTES",cluster_tolerance=Tolerance)

    print('[{}] Intersect:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Int_M = common.CreateOutPath(Project_GDB + '\\' + os.path.basename(Routes),'Int_M','')
    arcpy.analysis.Intersect(
        in_features=Routes,
        out_feature_class=Int_M,
        join_attributes='ALL',
        output_type='POINT',
        cluster_tolerance=Tolerance
    )
    print('[{}] MultiPart To SinglePart:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Int = common.CreateOutPath(Project_GDB + '\\' + os.path.basename(Routes),'Int','')
    arcpy.management.MultipartToSinglepart(in_features=Int_M,out_feature_class=Int)
    print('[{}] Delete Identical:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    arcpy.DeleteIdentical_management(in_dataset=Int,fields='Shape')
    print('[{}] Delete Field:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    arcpy.management.DeleteField(Int,[f.name for f in arcpy.ListFields(Int) if not f.required])
    print('[{}] Add XY:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    arcpy.management.AddXY(Int)

    print('[{}] Spatial Join F2L:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    IntAppSPJ = hsmpy3.common.CreateOutPath(Project_GDB + '\\' + os.path.basename(Routes),'IntAppSPJ','')
    arcpy.SpatialJoin_analysis(
            target_features = Int, 
            join_features = F2L, 
            out_feature_class = IntAppSPJ, 
            join_operation = "JOIN_ONE_TO_MANY", 
            join_type = "KEEP_ALL", 
            match_option = "INTERSECT", 
            search_radius = Tolerance, 
            distance_field_name = "Dist_F2L")

    #print('[{}] {} to pandas:'.format(strftime("%Y-%m-%d %H:%M:%S"),os.path.basename(Routes)))
    #Routes_DF = common.FCtoDF(Routes,True)
    #print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),Routes_DF.shape[0]))
    print('[{}] F2L to pandas:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    F2L_DF = hsmpy3.common.FCtoDF(F2L,True,['Shape'])
    print('[{}] - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),F2L_DF.shape[0]))

    print('[{}] Int_App DataFrame:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Bridge_Tolerance = 50
    Signal_Tolerance = 150
    App_DF = common.FCtoDF(IntAppSPJ,False,['TARGET_FID','POINT_X','POINT_Y','ROUTE_ID','JOIN_FID'])
    App_DF.columns = ['Int_ID','JOIN_FID','X','Y','RID']
    
    print('[{}] First Filter:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    App_DF = App_DF[[rid.split('-')[0]!='I' for rid in App_DF.RID]]
    def All_App(RIDList): return(len(list(set(['-'.join(s.split('-')[0:2]) for s in RIDList]))))
    def All_App_i(RIDList): return(list(set([s.split('-')[0] for s in RIDList])))
    df = pd.concat([App_DF.groupby('Int_ID')['RID'].aggregate([All_App_i]),App_DF.groupby('Int_ID')['RID'].aggregate([All_App])],axis=1)
    df = df[[(i!=['IX'] and a>1) for i,a in zip(df.All_App_i,df.All_App)]]
    App_DF = App_DF[App_DF.Int_ID.isin(list(df.index))]

    print('[{}] Second Filter:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    App_DF['Shape'] = list(F2L_DF.loc[App_DF.JOIN_FID]['Shape'])
    del F2L_DF
    App_DF['P1P2'] = [FindClosestPoint([[p.X,p.Y,p.M] for p in list(s)[0]],[x,y]) for s,x,y in zip(App_DF.Shape,App_DF.X,App_DF.Y)]
    App_DF['MP'] = [p1p2[0][2] for p1p2 in App_DF.P1P2]
    App_DF['OnBridge'] = [len(BridgeDF[(BridgeDF.RID==RID)   & ((BridgeDF.BMP-Bridge_Tolerance/5280.0)<=MP)  & ((BridgeDF.EMP+Bridge_Tolerance/5280.0)>=MP)])>0  for RID,MP in zip(App_DF.RID,App_DF.MP)]
    App_DF = App_DF[~App_DF.OnBridge]
    App_DF['Direction'] = [FindDirection(p1p2[0],p1p2[1]) for p1p2 in App_DF.P1P2]
    App_DF['Deg'] = [FindAngle(p1p2[0],p1p2[1]) for p1p2 in App_DF.P1P2]
    App_DF['HasSignal'] = [len(SignalsDF[(SignalsDF.RID==RID) & ((SignalsDF.MP-Signal_Tolerance/5280.0)<=MP) & ((SignalsDF.MP+Signal_Tolerance/5280.0)>=MP)])>0 for RID,MP in zip(App_DF.RID,App_DF.MP)]
    def PopDeg(L):return(len(PopCloseDeg(L,8)))
    df = App_DF.groupby('Int_ID')['Deg'].aggregate([PopDeg])
    df = df[df.PopDeg>2]
    App_DF = App_DF[App_DF.Int_ID.isin(list(df.index))]
    App_DF = App_DF.sort_values(by=['RID','MP','Direction'])
    App_DF['Length'] = [s.length for s in App_DF.Shape]
    App_DF = App_DF.drop(['P1P2', 'OnBridge'],axis=1)

    print('[{}] Merging Close Points:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    Cluster_Tolerance = 100  # Feet
    def Set(L):return(list(set(L)))
    df = pd.DataFrame(App_DF.groupby('JOIN_FID')['Int_ID','Length'].aggregate([Set]))
    df = df[[l[0]<Cluster_Tolerance for l in df[('Length','Set')]]]
    L2 = list(df[('Int_ID','Set')])
    L3 = list(set([y for x in L2 for y in x]))
    Cluster_Dict1 = [[int_id] for int_id in list(set(App_DF.Int_ID)) if not int_id in L3]
    Cluster_Dict1.extend(L2)
    Cluster_List = FindClusters(Cluster_Dict1)
    del L2,L3, Cluster_Dict1
    df = pd.DataFrame(columns=['Int_ID','ClusterNum'])
    df['Int_ID'] = list(set(App_DF.Int_ID))
    df.index = df.Int_ID
    df['ClusterNum'] = 0
    cnum = 0
    for i in Cluster_List:
        cnum += 1
        for j in i:
            df.set_value(j,'ClusterNum',cnum)
    App_DF['ClusterNum'] = list(df.loc[list(App_DF.Int_ID)]['ClusterNum'])
    del Cluster_List
    App_DF['XY'] = ['{}_{}'.format(x,y) for x,y in zip(App_DF.X,App_DF.Y)]
    def Centroid(L):
        XY = []
        for l in L:
            xy = l.split('_')
            XY.append([float(xy[0]),float(xy[1])])
        mpnt = arcpy.Multipoint(arcpy.Array([arcpy.Point(X=xy[0],Y=xy[1]) for xy in XY]))
        return([mpnt.centroid.X,mpnt.centroid.Y])
    df = pd.DataFrame(App_DF.groupby('ClusterNum')['XY'].aggregate(Centroid))
    df['C_X'] = [xy[0] for xy in df.XY]
    df['C_Y'] = [xy[1] for xy in df.XY]
    App_DF['C_X'] = list(df.loc[list(App_DF.ClusterNum)]['C_X'])
    App_DF['C_Y'] = list(df.loc[list(App_DF.ClusterNum)]['C_Y'])
    App_DF = App_DF.drop(['XY'],axis=1)

    print('[{}] Finding Number of Legs:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    def ExcludeMDir(RIDList):
        RIDList = list(set(RIDList))
        exclude = []
        for rid in RIDList:
            if rid.split('-')[2]=='M':
                if OppositeDirID(rid) in RIDList:
                    exclude.append(rid)
        return(exclude)
    df = pd.DataFrame(App_DF.groupby('ClusterNum')['RID'].aggregate(ExcludeMDir))
    App_DF['ExcludeRID'] = list(df.loc[list(App_DF.ClusterNum)]['RID'])
    App_DF['ExcForLegCount'] = [(rid in exL or l<Cluster_Tolerance) for exL,l,rid in zip(App_DF.ExcludeRID,App_DF.Length,App_DF.RID)]
    App_DF = App_DF.drop(['ExcludeRID'],axis=1)
    def Legs(L):return(len(PopCloseDeg(L,8)))
    df = pd.DataFrame(App_DF[~App_DF.ExcForLegCount].groupby('ClusterNum')['Deg'].aggregate(Legs))
    App_DF['Legs'] = list(df.loc[list(App_DF.ClusterNum)]['Deg'])
    App_DF = App_DF[App_DF.Legs>2]
    def Signal(L):return(True in list(L))
    df = pd.DataFrame(App_DF[~App_DF.ExcForLegCount].groupby('ClusterNum')['HasSignal'].aggregate(Signal))
    App_DF['Signal'] = list(df.loc[list(App_DF.ClusterNum)]['HasSignal'])

    print('[{}] Export the Results:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    App_DF = App_DF.sort_values(['ClusterNum','Int_ID','RID','Deg'])
    App_DF = App_DF[['ClusterNum', 'C_X', 'C_Y','Legs','Signal','Int_ID', 'X', 'Y', 'JOIN_FID', 'RID', 'MP', 'Direction', 'Deg', 'HasSignal', 'Length', 'Shape','ExcForLegCount']]
    App_DF.to_csv(AppCSV_Out)
    
    def FirstItem(L):return(list(L)[0])
    Int_DF = App_DF.groupby('ClusterNum')['Signal','Legs','C_X','C_Y'].aggregate(FirstItem)
    df = pd.DataFrame(App_DF.groupby('ClusterNum')['RID'].aggregate(Set))
    Int_DF['RIDList'] = list(df.loc[list(Int_DF.index)]['RID'])
    Int_DF.to_csv('Int_DF.csv')
    DF2FC = IntFC_Out
    arcpy.management.CreateFeatureclass(out_name=os.path.basename(DF2FC),
                                        out_path=Project_GDB,geometry_type='POINT',spatial_reference=hsmpy3.nm.NAD83_NM)
    arcpy.management.AddField(DF2FC,'Int_ID','LONG')
    arcpy.management.AddField(DF2FC,'Signal','Short')
    arcpy.management.AddField(DF2FC,'Legs'     ,'Short')
    arcpy.management.AddField(DF2FC,'RIDList'   ,'Text',800)

    ic = arcpy.InsertCursor(DF2FC)
    for i,r in Int_DF.iterrows():
            row = ic.newRow()
            row.setValue('Int_ID',int(i))
            row.setValue('Signal',{True:1,False:0}[r.Signal])
            row.setValue('Legs',int(r.Legs))
            row.setValue('RIDList',';'.join([rid for rid in r.RIDList])[:100])
            p = arcpy.PointGeometry(arcpy.Point(X=r.C_X,Y=r.C_Y),hsmpy3.nm.NAD83_NM)
            row.shape =  p
            ic.insertRow(row)
    del ic
    del row
def FindClusters(Cluster_Dict):
    df = pd.DataFrame(columns=range(0,6))
    for c in df.columns:
        df[c]=[0 for i in range(len(Cluster_Dict))]
    df
    for i,l in enumerate(Cluster_Dict):
        l = list(set(l))
        l.sort()
        for j,k in enumerate(l):
            df.set_value(i,j,k)
    df = df.sort_values([0,1,2,3,4,5])
    df = df.drop_duplicates(subset=[0,1,2,3,4,5])
    df['Len']  = [len([r[c] for c in df.columns if r[c]>0]) for i,r in df.iterrows()]
    df = df.sort_values(['Len',0,1,2,3,4,5])
    df1 = df[df.Len==1]
    df2 = df[df.Len==2]
    df2 = df2.sort_values([0])
    df3 = df[df.Len==3]
    df3 = df3.sort_values([0])
    df4 = df[df.Len==4]
    df4 = df4.sort_values([0])
    df5 = df[df.Len==5]
    df5 = df5.sort_values([0])
    df6 = df[df.Len==6]
    df6 = df6.sort_values([0])

    df3['MergeID'] = 0
    for i,r in df3.iterrows():
        rdf3 = df3[(df3[0]==r[0]) | (df3[0]==r[1]) | (df3[0]==r[2]) | 
                   (df3[1]==r[0]) | (df3[1]==r[1]) | (df3[1]==r[2]) | 
                   (df3[2]==r[0]) | (df3[2]==r[1]) | (df3[2]==r[2])]
        if len(rdf3)>0:
            merge = max(df3.MergeID) + 1
            for j in list(rdf3.index):
                if df3.loc[j]['MergeID'] == 0:
                    df3.set_value(j,'MergeID',merge)
    df3 = df3.sort_values('MergeID')
    df4['MergeID'] = 0
    for i,r in df4.iterrows():
        rdf4 = df4[(df4[0]==r[0]) | (df4[0]==r[1]) | (df4[0]==r[2]) | (df4[0]==r[3]) |
                   (df4[1]==r[0]) | (df4[1]==r[1]) | (df4[1]==r[2]) | (df4[1]==r[3]) |
                   (df4[2]==r[0]) | (df4[2]==r[1]) | (df4[2]==r[2]) | (df4[2]==r[3]) |
                   (df4[3]==r[0]) | (df4[3]==r[1]) | (df4[3]==r[2]) | (df4[3]==r[3])]
        if len(rdf4)>0:
            merge = max(df4.MergeID) + 1
            for j in list(rdf4.index):
                if df4.loc[j]['MergeID'] == 0:
                    df4.set_value(j,'MergeID',merge)
    df4 = df4.sort_values('MergeID') 

    df5['MergeID'] = 0
    for i,r in df5.iterrows():
        rdf5 = df5[(df5[0]==r[0]) | (df5[0]==r[1]) | (df5[0]==r[2]) | (df5[0]==r[3]) | (df5[0]==r[4])]
        if len(rdf5)>0:
            merge = max(df5.MergeID) + 1
            for j in list(rdf5.index):
                if df5.loc[j]['MergeID'] == 0:
                    df5.set_value(j,'MergeID',merge)
    df5 = df5.sort_values('MergeID') 

    df6['MergeID']  = 1

    l1 = [[i] for i in df1[0]]
    l2 = [[i,j] for i,j in zip(df2[0],df2[1])]
    l3 = []
    for i in list(set(df3.MergeID)):
        rdf3 = df3[df3.MergeID==i]
        l = []
        for j,r in rdf3.iterrows():
            l.extend([r[0],r[1],r[2]])
        l = list(set(l))
        l.sort()
        l3.append(l)
    l4 = []
    for i in list(set(df4.MergeID)):
        rdf4 = df4[df4.MergeID==i]
        l = []
        for j,r in rdf4.iterrows():
            l.extend([r[0],r[1],r[2],r[3]])
        l = list(set(l))
        l.sort()
        l4.append(l)
    l5 = []
    for i in list(set(df5.MergeID)):
        rdf5 = df5[df5.MergeID==i]
        l = []
        for j,r in rdf5.iterrows():
            l.extend([r[0],r[1],r[2],r[3],r[4]])
        l = list(set(l))
        l.sort()
        l5.append(l)
    l6 = []
    for i in list(set(df6.MergeID)):
        rdf6 = df6[df6.MergeID==i]
        l = []
        for j,r in rdf6.iterrows():
            l.extend([r[0],r[1],r[2],r[3],r[4],r[5]])
        l = list(set(l))
        l.sort()
        l6.append(l)
    l2.extend(l3)
    l2.extend(l4)
    l2.extend(l5)
    l2.extend(l6)

    Cluster_Dict = l2
    fl = []
    s = []
    for i in range(len(Cluster_Dict)):
        f = [k for k in Cluster_Dict[i]]
        for j in range(i+1,len(Cluster_Dict)):
            d = [k for k in Cluster_Dict[j] if not k in s]
            if len(d)>0:
                if True in [(k in d) for k in Cluster_Dict[i]]:
                    f.extend(Cluster_Dict[j])
                    f = list(set(f))
        if not True in [(k in s) for k in f]:
                fl.append(f)
                s.extend(f)
    Cluster_List = fl
    Cluster_List.extend(l1)
    return(Cluster_List)
def FindAngle(O,P):
        import math
        if P[0] == O[0]:
             if P[1] == O[1]:
                 #arcpy.AddWarning(str(O) + str(P))
                 return(0) #1
             else:
                 if P[1] > O[1]:
                     return(90)  #2
                 if P[1] < O[1]:
                     return(270) #3
        else:
            if P[1] == O[1]:
                if P[0] > O[0]:
                    return 0 #4
                else:
                    return 180 #5
            else:
                if   (P[0] - O[0]) > 0 and (P[1] - O[1]) > 0:
                    return math.degrees(math.atan((P[1] - O[1]) / (P[0] - O[0]))) #6
                elif (P[0] - O[0]) > 0 and (P[1] - O[1]) < 0:
                    return 360 - math.degrees(math.atan(-(P[1] - O[1]) / (P[0] - O[0]))) #7
                elif (P[0] - O[0]) < 0 and (P[1] - O[1]) > 0:
                    return 180 - math.degrees(math.atan(-(P[1] - O[1]) / (P[0] - O[0]))) #8
                elif (P[0] - O[0]) < 0 and (P[1] - O[1]) < 0:
                    return 180 + math.degrees(math.atan((P[1] - O[1]) / (P[0] - O[0])))
def FindClosestPoint(PolylineList,IntPoint):
            n = len(PolylineList)
            Dist0 = ((PolylineList[0    ][0] - IntPoint[0]) ** 2 + (PolylineList[0    ][1] - IntPoint[1]) ** 2) ** 0.5
            Distn = ((PolylineList[n - 1][0] - IntPoint[0]) ** 2 + (PolylineList[n - 1][1] - IntPoint[1]) ** 2) ** 0.5
            if Dist0 <= Distn:
                return [PolylineList[0  ],PolylineList[1  ]]
            else:
                return [PolylineList[n-1],PolylineList[n-2]]
def PopCloseDeg(DegList,Eps):
    out = []
    for i,deg in enumerate(DegList):
        flag = False
        for odeg in out:
            if abs(deg-odeg)<=Eps or abs(deg-odeg)>=(360-Eps):
                flag = True
        if not flag:
            out.append(deg)
    return(out)
def OppositeDirID(InpID):
    out = InpID[:-2]
    ext = InpID[-1]
    if ext == 'P':
        return('{}-M'.format(out))
    if ext == 'M':
        return('{}-P'.format(out))
def FindDirection(O,P):
    direction = 'in' # approaching intersection w increasing milepost
    if P[2]-O[2]>0:
        direction = 'out'
    return(direction)
def CON_CreateIntPoints(WDir,HSMPY_PATH,Routes,Project_GDB,BridgeXLSX,SignalsXLSX,IntFC_Out,AppCSV_Out,Title=''):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'CreateIntPoints_' + str(Title) + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
import pandas as pd
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
Routes = r"{}"
Project_GDB = r"{}"
BridgeXLSX = r"{}"
SignalsXLSX = r"{}"
IntFC_Out = r'{}'
AppCSV_Out = r'{}'

print("Create Intersection Points")

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
hsmpy3.network.CreateIntPoints(Routes,Project_GDB,pd.read_excel(BridgeXLSX),pd.read_excel(SignalsXLSX),IntFC_Out,AppCSV_Out)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,Routes,Project_GDB,BridgeXLSX,SignalsXLSX,IntFC_Out,AppCSV_Out)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)


def DissolveDF(DF,RID,BMP,EMP,STIM,ETIM,DissFields):
    print('[{}] dissolving by milepost: {}'.format(strftime("%Y-%m-%d %H:%M:%S"),DissFields))
    print('[{}] sorting and indexing:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    F1 = [RID,STIM,ETIM,BMP,EMP]
    F2 = DissFields
    df = DF[F1+F2]
    df.index = range(0,df.shape[0])
    df = df.sort_values(by=[RID,STIM])
    df = df.fillna(-1)
    print('[{}]  - {}:'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape))
    print('[{}] grouping intervals:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    idx = df.groupby([RID,STIM,ETIM] + F2)[BMP].shift(-1) != df[EMP]
    df['EMP2'] = df.loc[idx, EMP]
    df['EMP2'] = df.groupby([RID,STIM,ETIM] + F2)['EMP2'].fillna(method='backfill')
    df['EMP2'] = df['EMP2'].fillna(df[EMP]) 
    print('[{}] aggregating groups:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    sdf = df.groupby([RID,STIM,ETIM] + F2 + ['EMP2'], as_index=False).agg({BMP: 'first', EMP: 'last'}).drop(['EMP2'], axis=1)
    print('[{}]  - {}:'.format(strftime("%Y-%m-%d %H:%M:%S"),sdf.shape))

    print('[{}] dissolving by time:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    print('[{}] sorting and indexing:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    df = sdf
    df.index = range(0,df.shape[0])
    df = df.sort_values(by=[RID,BMP])
    print('[{}] grouping intervals:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    idx = df.groupby([RID,BMP,EMP] + F2)[STIM].shift(-1) != df[ETIM]
    df['EMP2'] = df.loc[idx, ETIM]
    df['EMP2'] = df.groupby([RID,BMP,EMP] + F2)['EMP2'].fillna(method='backfill')
    df['EMP2'] = df['EMP2'].fillna(df[ETIM]) 
    print('[{}] aggregating groups:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    sdf = df.groupby([RID,BMP,EMP] + F2 + ['EMP2'], as_index=False).agg({STIM: 'first', ETIM: 'last'}).drop(['EMP2'], axis=1)
    print('[{}]  - {}:'.format(strftime("%Y-%m-%d %H:%M:%S"),sdf.shape))
    print('[{}] sorting the output:'.format(strftime("%Y-%m-%d %H:%M:%S")))
    sdf = sdf.replace(-1,np.NaN)
    sdf = sdf[F1+F2].sort_values(F1)
    print('[{}] done!'.format(strftime("%Y-%m-%d %H:%M:%S")))
    return(sdf)


def ImportIntAtt_New(Intersections, TrafficControl, Routes, RouteID, BMP, EMP, AttTable, Fields, Output, OutputTable):
    def FindAngle(O, P):
        import math
        if P[0] == O[0]:
            if P[1] == O[1]:
                # arcpy.AddWarning(str(O) + str(P))
                return 0  # 1
            else:
                if P[1] > O[1]:
                    return 90  # 2
                if P[1] < O[1]:
                    return 270  # 3
        else:
            if P[1] == O[1]:
                if P[0] > O[0]:
                    return 0  # 4
                else:
                    return 180  # 5
            else:
                if (P[0] - O[0]) > 0 and (P[1] - O[1]) > 0:
                    return math.degrees(math.atan((P[1] - O[1]) / (P[0] - O[0])))  # 6
                elif (P[0] - O[0]) > 0 and (P[1] - O[1]) < 0:
                    return 360 - math.degrees(math.atan(-(P[1] - O[1]) / (P[0] - O[0])))  # 7
                elif (P[0] - O[0]) < 0 and (P[1] - O[1]) > 0:
                    return 180 - math.degrees(math.atan(-(P[1] - O[1]) / (P[0] - O[0])))  # 8
                elif (P[0] - O[0]) < 0 and (P[1] - O[1]) < 0:
                    return 180 + math.degrees(math.atan((P[1] - O[1]) / (P[0] - O[0])))

    def FindClosestPoint(PolylineList, IntPoint):
        n = len(PolylineList)
        Dist0 = ((PolylineList[0][0] - IntPoint[0]) ** 2 + (PolylineList[0][1] - IntPoint[1]) ** 2) ** 0.5
        Distn = ((PolylineList[n - 1][0] - IntPoint[0]) ** 2 + (PolylineList[n - 1][1] - IntPoint[1]) ** 2) ** 0.5
        if Dist0 <= Distn:
            return [PolylineList[0], PolylineList[1]]
        else:
            return [PolylineList[n - 1], PolylineList[n - 2]]

    Buffer = "80 Feet"
    Tolerance = "10 Feet"
    Int = hsmpy3.common.CreateOutPath(MainFile=Output, appendix='Int', Extension='')
    arcpy.Intersect_analysis(
        in_features=Routes,
        out_feature_class=Int,
        join_attributes="ALL",
        cluster_tolerance="-1 Unknown",
        output_type="POINT")

    SPJ = hsmpy3.common.CreateOutPath(MainFile=Output, appendix='SPJ', Extension='')
    arcpy.SpatialJoin_analysis(
        target_features=Int,
        join_features=Intersections,
        out_feature_class=SPJ,
        join_operation="JOIN_ONE_TO_ONE",
        join_type="KEEP_COMMON",
        match_option="CLOSEST",
        search_radius=Buffer,
        distance_field_name="")

    arcpy.DeleteIdentical_management(
        in_dataset=SPJ,
        fields=arcpy.Describe(SPJ).ShapeFieldName,
        xy_tolerance="",
        z_tolerance="0")

    OrgFields = [f.name for f in arcpy.ListFields(Intersections)]
    arcpy.DeleteField_management(SPJ,
                                 [f.name for f in arcpy.ListFields(SPJ) if not f.required and not f.name in OrgFields])

    arcpy.SpatialJoin_analysis(
        target_features=SPJ,
        join_features=TrafficControl,
        out_feature_class=Output,
        join_operation="JOIN_ONE_TO_ONE",
        join_type="KEEP_COMMON",
        match_option="CLOSEST",
        search_radius=Buffer,
        distance_field_name="")

    OrgFields.extend(['TRAF_CONT', 'LEG_COUNT', 'PeerGroupText_CH2M_Updated_PGs_TCTs'])
    arcpy.DeleteField_management(Output, [f.name for f in arcpy.ListFields(Output) if
                                          not f.required and not f.name in OrgFields])

    EventTable = hsmpy3.common.CreateOutPath(MainFile=Output, appendix='EventTable', Extension='')
    arcpy.LocateFeaturesAlongRoutes_lr(
        in_features=Output,
        in_routes=Routes,
        route_id_field=RouteID,
        radius_or_tolerance=Tolerance,
        out_table=EventTable,
        out_event_properties=" ".join([RouteID, "POINT", "MP"]),
        route_locations="ALL",
        in_fields="FIELDS",
        m_direction_offsetting="M_DIRECTON"
    )

    # Milepost Correction
    EMPDict = {r.getValue(RouteID): r.getValue('Shape').lastPoint.M for r in arcpy.SearchCursor(Routes)}
    r = 0
    uc = arcpy.UpdateCursor(EventTable)
    for r in uc:
        inv = r.getValue(RouteID)
        MP = r.getValue('MP')
        if MP < 0:
            r.setValue('MP', 0)
            uc.updateRow(r)
        if MP > EMPDict[inv]:
            r.setValue('MP', EMPDict[inv])
            uc.updateRow(r)
    del uc, r

    AllF = [f.name for f in arcpy.ListFields(AttTable)]
    MF = [f for f in Fields if not f in AllF]
    if not MF == []:
        print(str(MF) + ' not found in ' + AttTable)
    IRIS_Diss = hsmpy3.common.CreateOutPath(MainFile=Output, appendix='diss', Extension='')
    arcpy.DissolveRouteEvents_lr(
        in_events=AttTable,
        in_event_properties=' '.join([RouteID, 'LINE', BMP, EMP]),
        dissolve_field=';'.join(Fields),
        out_table=IRIS_Diss,
        out_event_properties=' '.join([RouteID, 'LINE', BMP, EMP]),
        dissolve_type="DISSOLVE",
        build_index="INDEX"
    )

    arcpy.OverlayRouteEvents_lr(
        in_table=EventTable,
        in_event_properties=' '.join([RouteID, 'POINT', 'MP']),
        overlay_table=IRIS_Diss,
        overlay_event_properties=' '.join([RouteID, 'LINE', BMP, EMP]),
        overlay_type="INTERSECT",
        out_table=OutputTable,
        out_event_properties=' '.join([RouteID, 'POINT', 'MP']),
        in_fields="FIELDS",
        build_index="INDEX"
    )

    hsmpy3.common.AddField(Output, [
        fields_SC.intr.AADT_Major,
        fields_SC.intr.AADT_Minor,
        fields_SC.crash.ABuffer,
        fields_SC.crash.BBuffer
    ])

    arcpy.AddField_management(OutputTable, 'ApprType', 'TEXT')
    # arcpy.AddField_management(OutputTable,'ApprDeg','Double')
    Approach = {r.getValue('SiteID'): [] for r in arcpy.SearchCursor(Output)}

    OID = arcpy.Describe(OutputTable).OIDFieldName
    for r in arcpy.SearchCursor(OutputTable):
        k = r.getValue('SiteID')
        if k in Approach.keys():
            Approach[k].append({
                'OID': r.getValue(OID),
                'INV': r.getValue(RouteID),
                'AADT': common.GetIntVal(r, 'AADT'),
                'Lanes': common.GetIntVal(r, 'LANES', 2),
                'Urban': r.getValue('URBAN'),
                'SurfWid': common.GetFloatVal(r, 'SURF_WTH', 24),
                'MedWid': common.GetFloatVal(r, 'MED_WTH')
            })
    for k in Approach.keys():
        AADT = [i['AADT'] for i in Approach[k]]
        INV = [i['INV'] for i in Approach[k]]
        major_i = AADT.index(max(AADT))
        major_inv = INV[major_i]
        for i, appr in enumerate(Approach[k]):
            if appr['AADT'] == max(AADT) or appr['INV'] == major_inv:
                Approach[k][i].update({'ApprType': 'Major'})
            else:
                Approach[k][i].update({'ApprType': 'Minor'})

    UC = arcpy.UpdateCursor(OutputTable)
    for r in UC:
        k = r.getValue('SiteID')
        o = r.getValue(OID)
        Type = ''
        for appr in Approach[k]:
            if appr['OID'] == o:
                Type = appr['ApprType']
        r.setValue('ApprType', Type)

        UC.updateRow(r)

    UC = arcpy.UpdateCursor(Output)
    for r in UC:
        k = r.getValue('SiteID')
        try:
            r.setValue(fields_SC.intr.AADT_Major['name'],
                       max([appr['AADT'] for appr in Approach[k] if appr['ApprType'] == 'Major']))
        except:
            r.setValue(fields_SC.intr.AADT_Major['name'], 0)
        try:
            r.setValue(fields_SC.intr.AADT_Minor['name'],
                       max([appr['AADT'] for appr in Approach[k] if appr['ApprType'] == 'Minor']))
        except:
            r.setValue(fields_SC.intr.AADT_Minor['name'], 0)
        try:
            W_Major = max([appr['SurfWid'] + appr['MedWid'] for appr in Approach[k] if appr['ApprType'] == 'Major'])
        except:
            W_Major = 24
        try:
            W_Minor = max([appr['SurfWid'] + appr['MedWid'] for appr in Approach[k] if appr['ApprType'] == 'Minor'])
        except:
            W_Minor = 24
        ABuffer = max(1.2 * (W_Major ** 2 + W_Minor ** 2) ** 0.5, 50)
        r.setValue(fields_SC.crash.ABuffer['name'], ABuffer)
        r.setValue(fields_SC.crash.BBuffer['name'], max(ABuffer, 250))
        AADT = [i['AADT'] for i in Approach[k]]
        major_i = AADT.index(max(AADT))
        LaneMajor = [i['Lanes'] for i in Approach[k]][0]
        UC.updateRow(r)

    arcpy.Delete_management(Int)
    arcpy.Delete_management(EventTable)
    arcpy.Delete_management(SPJ)
    arcpy.Delete_management(IRIS_Diss)
def CompassFromShapefile(RoutesFC,RID_Field,CSV_Out):
    def degToCompass(num):
        if not pd.isnull(num):
            val=int((num/22.5)+.5)
            arr=["W","SW" ,"SW","SW" ,"S","SE" , "SE", "SE" ,"E","NE" ,"NE","NE" ,"N","NW" ,"NW","NW" ]
            return(arr[(val % 16)])
    def FindBMPnEMP(DF):
        df= pd.DataFrame({'BMP':DF.M.min(),'EMP':DF.M.max(),'Compass':DF.Compass.iloc[0]},index=[0])
        return(df)
    def ConvertPLtoCompass(row):
        pl = row.Shape
        pl_df = PolylineToDF(pl)
        L = []
        for i,r in pl_df.iterrows():
            prt_df = ParttoDF(r.Shape)
            prt_df['dx'] = prt_df.X.diff()
            prt_df['dy'] = prt_df.Y.diff()
            prt_df['Angle'] = prt_df.apply(lambda row:math.atan2(row.dy,row.dx)/math.pi*180+180,axis=1)
            prt_df['Compass'] = prt_df.Angle.apply(degToCompass)
            prt_df.loc[0,'Compass'] = prt_df.loc[1,'Compass']
            prt_df['Shifted'] = prt_df.Compass.shift(1).fillna(prt_df.Compass.iloc[0])
            prt_df['Blocks'] = prt_df.apply(lambda row:1 if row.Compass!= row.Shifted else 0,axis=1).cumsum()
            df = prt_df.groupby('Blocks').apply(FindBMPnEMP)
            df.index = df.index.droplevel(1)
            df = df[['BMP','EMP','Compass']]
            if df.shape[0]>1:
                df.BMP.iloc[1:] = df.EMP.shift(+1)
            L.append(df)
        Compass_DF = pd.concat(L)
        return(Compass_DF)
    A = []
    print('[{}] read route data'.format(strftime("%Y-%m-%d %H:%M:%S")))
    R_DF = common.FCtoDF(RoutesFC,selectedFields=[RID_Field],readGeometry=True)
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),R_DF.shape[0]))

    print('[{}] iterating through routes ...'.format(strftime("%Y-%m-%d %H:%M:%S")))
    for i,r in R_DF.iterrows():
        df = ConvertPLtoCompass(r)
        df['INVENTORY'] = r[RID_Field]
        A.append(df)
    df = pd.concat(A)
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),df.shape[0]))
    print('[{}] exporting the results'.format(strftime("%Y-%m-%d %H:%M:%S")))
    df = df[['INVENTORY','BMP','EMP','Compass']]
    df.reset_index(drop=True,inplace=True)
    df.to_csv(CSV_Out,index=False)
    print('[{}] done!'.format(strftime("%Y-%m-%d %H:%M:%S")))
def CON_CompassFromShapefile(WDir,HSMPY_PATH,RoutesFC,RID_Field,CSV_Out,Title=''):
    import sys, os, arcpy, csv, json, math, subprocess
    sys.path.append(HSMPY_PATH)

    pyFN = os.path.join(WDir , 'Compass_' + str(Title) + '.py')
    OutFile = open(pyFN, 'w')
    pyfile = """from time import gmtime, strftime
print(strftime("%Y-%m-%d %H:%M:%S"))
import os, sys
import atexit
import pandas as pd
atexit.register(input, 'Press Enter to continue...')
HSMPY_PATH = r'{}'
RoutesFC = r"{}"
RID_Field = r"{}"
CSV_Out = r"{}"
Title = {}
print("Create Compass " + str(Title))

sys.path.append(HSMPY_PATH) 
import hsmpy3
import arcpy
hsmpy3.network.CompassFromShapefile(RoutesFC,RID_Field,CSV_Out)
print(strftime("%Y-%m-%d %H:%M:%S"))
""".format(HSMPY_PATH,RoutesFC,RID_Field,CSV_Out,Title)
    OutFile.write(pyfile)
    OutFile.close()
    SubProcess = subprocess.Popen(
                [sys.executable, pyFN],
                shell=False,creationflags = subprocess.CREATE_NEW_CONSOLE)
    return(SubProcess)


def ExtractCurves_2(IRIS_FC,Param_CSV,Out_CSV):

    def findangle(p1, p2,p3):
                A = np.array(p1)
                B = np.array(p2)
                C = np.array(p3)
                v1 = B - A
                v2 = C - B
                def unit_vector(vector):
                    return vector / np.linalg.norm(vector)
                v1_u = unit_vector(v1)
                v2_u = unit_vector(v2)
                return(np.degrees(np.arctan2(v2_u[1], v2_u[0])-np.arctan2(v1_u[1], v1_u[0])))
    def findangle_2(l1, l2):
        pt1,pt2 = l1[0],l1[1]
        pt3,pt4 = l2[0],l2[1]
        x1, y1 = pt2[0]-pt1[0],pt2[1]-pt1[1]
        x2, y2 = pt4[0]-pt3[0],pt4[1]-pt3[1]
        inner_product = x1*x2 + y1*y2
        len1 = math.hypot(x1, y1)
        len2 = math.hypot(x2, y2)
        try:
            ang = math.acos(inner_product/(len1*len2))
        except:
            print(x1,y1,x2,y2)
            ang = math.pi * 2
        ang = ang*180.0/math.pi
        return(abs(ang))

    def AddMidPoints(l,desd):
            pntl = [arcpy.Point(X = l[0][0],Y=l[0][1],Z=0,M=l[0][-1])]
            for p in l[1:]:
                curpnt = arcpy.Point(X = p[0],Y=p[1],Z=0,M=p[-1])
                curd = arcpy.PointGeometry(pntl[-1]).distanceTo(curpnt)
                if curd <= desd:
                    pntl.append(curpnt)
                else:
                    n = int(curd/desd)+1
                    delta = curd/n
                    pl = arcpy.Polyline(arcpy.Array([pntl[-1],curpnt]))
                    for j in range(1,n):
                        if j*delta<curd:
                            midpg = pl.positionAlongLine(j*delta)
                            m = float((curpnt.M - pntl[-1].M))/n*j + pntl[-1].M
                            midp = arcpy.Point(midpg.firstPoint.X,midpg.firstPoint.Y,0,m)
                            pntl.append(midp)
                    pntl.append(curpnt)
            return(pntl)

    def RemoveOverlap(CDF):
            for i in range(1,len(CDF)):
                if CDF.loc[i]['BMP']<CDF.loc[i-1]['EMP']:
                    ave = (CDF.loc[i]['BMP']+CDF.loc[i-1]['EMP'])/2 
                    CDF.loc[i]['BMP'] = ave
                    CDF.loc[i-1]['EMP'] = ave
            return(CDF)
    def FindClusters(CD,DegMin):
            flag = False
            j = 0
            R = []
            T = []
            for i in range(len(CD['Radius'])):
                if abs(CD['Radius'][i]) > DegMin:
                    T.append(int(math.copysign(1,CD['Radius'][i])))
                    if not flag:
                        flag = True
                        j += 1
                    else:
                        if CD['Radius'][i]*CD['Radius'][i-1]<=0:
                            j =+ 1
                            flag = True
                else:
                    T.append(0)
                    if flag:
                        j += 1
                        flag = False
                R.append(j)
            return({'CN':R,'CT':T})
    def MergeCurves(DF,MinLen): # Merging curves with same direction if their distance is less than MinLen
            CT = [0]
            for i in range(1,len(DF)-1):
                if DF.loc[i]['Cluster Type'] == 0:
                    if DF.loc[i-1]['Cluster Type'] == DF.loc[i+1]['Cluster Type']:
                        if (DF.loc[i+1]['Milepost']-DF.loc[i-1]['Milepost']) * 5280 <MinLen:
                            CT.append(DF.loc[i-1]['Cluster Type'])
                        else:
                            CT.append(DF.loc[i]['Cluster Type'])
                    else:
                        CT.append(DF.loc[i]['Cluster Type'])
                else:
                    CT.append(DF.loc[i]['Cluster Type'])
            CT.append(0)
            return(CT)
    def CircleFitting(l):
            from scipy import optimize
            import numpy
            def calc_R(xc, yc):
                return numpy.sqrt((x-xc)**2 + (y-yc)**2)
            def f_2(c):
                Ri = calc_R(*c)
                return Ri - Ri.mean()
            x = numpy.array([i[0] for i in l])
            y = numpy.array([i[1] for i in l])
            x_m = sum(x)/max(len(x),1)
            y_m = sum(y)/max(len(y),1)
            center_estimate = x_m, y_m
            center_2, ier = optimize.leastsq(f_2, center_estimate)
            xc_2, yc_2 = center_2
            Ri_2       = calc_R(*center_2)
            R_2        = Ri_2.mean()
            residu_2   = sum((Ri_2 - R_2)**2)
            return({'Radius':R_2,'Center':[xc_2, yc_2]})
    def HorCurvature(Shape):
            import re
            import math
            import arcpy
            from math import acos
            from numpy.linalg import norm
            import numpy
            import json
            def Length(P1,P2):
                return(math.sqrt((P2[0]-P1[0])**2+(P2[1]-P1[1])**2))
            Vertices = json.loads(Shape.JSON)['paths'][0]
            R = [0]
            M = [Vertices[0][3]]
            L = Shape.length
            for i in range(2,len(Vertices)):
                l1 = Length(Vertices[i-2],Vertices[i-1])
                l2 = Length(Vertices[i-1],Vertices[i  ])
                #R.append(Radius(Vertices[i-2],Vertices[i-1],Vertices[i]))
                R.append(findangle(Vertices[i-2],Vertices[i-1],Vertices[i]))
                M.append(Vertices[i-1][3])
            R.append(0)
            M.append(Vertices[-1][3])
            return({'Radius':R,'Milepost':M})

    def FindRadius(Shape,DegMin,MinLen):
            import json
            import pandas as pd
            l = json.loads(Shape.JSON)['paths'][0]
            DF = pd.DataFrame()
            DF['X'] = [i[0] for i in l]
            DF['Y'] = [i[1] for i in l]
            DF['Milepost'] = [i[3] for i in l]
            CD = HorCurvature(Shape)
            CL = FindClusters(CD,DegMin)
            DF['Heading Angle'] = CD['Radius']
            DF['Cluster Number'] = CL['CN']
            DF['Cluster Type'] = CL['CT']
            DF['Cluster Type'] = MergeCurves(DF,MinLen)
            Radius = []
            Cen_X = []
            Cen_Y = []
            Points = []
            kr = [-1]
            Curves= []
            for i in range(len(DF)):
                if not i in kr:
                    if DF.loc[i]['Cluster Type'] == 0:
                        Cen_X.append(0)
                        Cen_Y.append(0)
                        Radius.append(0)
                        Points.append(str(i))
                    else:
                        cl = [[DF.loc[i-1]['X'],DF.loc[i-1]['Y']]]
                        j = i
                        while DF.loc[j]['Cluster Type']==DF.loc[i]['Cluster Type']:
                            cl.append([DF.loc[j]['X'],DF.loc[j]['Y']])
                            j += 1
                        cl.append([DF.loc[j]['X'],DF.loc[j]['Y']])
                        CF = CircleFitting(cl)
                        Curves.append({'BMP':DF.loc[i-1]['Milepost'],'EMP':DF.loc[j]['Milepost'],
                                    'Radius':math.copysign(CF['Radius'],DF.loc[i]['Cluster Type']),
                                    'Cen_X':CF['Center'][0],'Cen_Y':CF['Center'][1],
                                    'PC_X':cl[0][0],'PC_Y':cl[0][1],
                                    'PT_X':cl[-1][0],'PT_Y':cl[-1][1],
                                    'Delta':findangle_2(cl[:2],cl[-2:]),
                                    'Length':(DF.loc[j]['Milepost']-DF.loc[i-1]['Milepost'])*5280.0
                                    })
                        kr = range(i,j)
                        for k in kr:
                                Radius.append(math.copysign(CF['Radius'],DF.loc[i]['Cluster Type']))
                                Cen_X.append(CF['Center'][0])
                                Cen_Y.append(CF['Center'][1])
                                Points.append(';'.join([str(t) for t in range(i-1,j+1)]))
                        
            DF['Radius'] = Radius
            DF['Center_X'] = Cen_X
            DF['Center_Y'] = Cen_Y
            DF['Points'] = Points
            CDF = pd.DataFrame(Curves)
            CDF = RemoveOverlap(CDF)
            if len(CDF)>0:
                CDF = CDF[['BMP', 'EMP', 'Length', 'Radius', 'Delta', 'Cen_X', 'Cen_Y', 'PC_X', 'PC_Y','PT_X', 'PT_Y']]
            #Res = RemoveSharpTurns(DF)
            #DF['Cluster Type'] = Res[0]
            #CDF = CDF.loc[[k for k in list(CDF.index) if not k in Res[1]]]
            return([DF,CDF])
    def RemoveSharpTurns_2(CDF,MaxLength,AveHeadingAngle):
        if len(CDF>0):
            df = CDF[~((CDF.Length<MaxLength) & (CDF.Delta>AveHeadingAngle))]
            df = df[df.Delta<360]
        else:
            df = CDF
        return(df)    
    Out_DF = []
    Param_DF = pd.read_csv(Param_CSV)
    Param_DF.index = Param_DF.RouteType
    print('[{}] reading IRIS FC'.format(strftime("%Y-%m-%d %H:%M:%S")))
    IRIS_DF = hsmpy3.common.FCtoDF(IRIS_FC,readGeometry=True)
    IRIS_DF.index = IRIS_DF.INVENTORY
    print('[{}]  - {}'.format(strftime("%Y-%m-%d %H:%M:%S"),IRIS_DF.shape))

    for inv in IRIS_DF.INVENTORY:
        print('[{}] {}'.format(strftime("%Y-%m-%d %H:%M:%S"),inv))
        l = json.loads(IRIS_DF.Shape.loc[inv].JSON)['paths'][0]
        pntl = AddMidPoints(l,Param_DF.loc[int(inv[5]),'MidPoints'])
        a = arcpy.Array(pntl)
        pl = arcpy.Polyline(a,arcpy.SpatialReference(102672),True,True)
        Res = FindRadius(pl,Param_DF.loc[int(inv[5]),'DegMin'],Param_DF.loc[int(inv[5]),'MinLen'])
        cdf = RemoveSharpTurns_2(Res[1],Param_DF.loc[int(inv[5]),'MaxLength'],Param_DF.loc[int(inv[5]),'MaxDelta'])
        cdf['INVENTORY'] = inv
        Out_DF.append(cdf)
    Out_DF = pd.concat(Out_DF)
    Out_DF.to_csv(Out_CSV,index=False)
