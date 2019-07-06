
class TP_Texts:
    # __init__()
    init_error1 = "Start and End must be of type datetime.datetime!"
    init_error2 = "End must be larger than start!"
    
    # start()
    start_error1 = "Time must be of type datetime.datetime!"
    start_error2 = "start must be smaller than end of Time_Period!"
    
    # end()
    end_error1 = "end must be larger than start of TimePeriod!"
    
    # general
    general_error1 = "'another' must be of type datetime.datetime or sptemp.zeit.Time_Period!"
    general_error2 = "'another' must be of type sptemp.zeit.Time_Period!"
    
class TS_Texts:
    # __init__()
    init_error1 = "ts must be of type datetime.datetime or sptemp.zeit.Time_Period!"
    
    # value()
    v_error1 = "value must be of same type as old value of the TS_Object!"
    
class Unit_Texts:
    # __init__()
    init_error1 = "value must be of type 'types.FunctionType'!"
    init_error2 = "ts must be of type sptemp.zeit.Time_Period!"
    
    #interpolate()
    i_error1 = "start_ts AND end_ts must be of type sptemp.zeit.TS_Object!"
    i_error2 = "Time must be of type datetime.datetime!"
    i_error3 = "start_ts.end_time() must be included in self.ts!"
    #i_error4 = "end_ts.start_time() must be included in self.ts!"
    i_error5 = "time must be included in self.ts!"
    
class IP_Texts:
    
    # __init__()
    init_error1 = "Empty instantiation not possible!"
    init_error2 = "ts_unit_list must be list holding objects of type sptemp.zeit.TS_Unit!"
    init_error3 = "TS_Unit elements of ts_unit_list must be time-sorted and end_times of units must equal start_times of next unit!"
    
    # setitem()
    set_error1 = "Index must be of type integer! Slices not allowed"
    set_error2 = "Value must be of type TS_Unit!"
    set_error3 = "Index out of range!"
    set_error4 = "Value must cover same time_period as the value it replaces!"
    
    # delitem()
    del_error1 = "Only first and last item can be deleted!"
    del_error2 = "Interpolator object cannot be empty!"
    
    # interpolate()
    ip_error1 = "start_ts and end_ts must be of type sptemp.zeit.TS_Object!"
    ip_error2 = "time must be of type datetime.datetime!"
    ip_error3 = "start_ts.end_time() must be >= self.start_time()!"
    ip_error4 = "time must be >= start_ts.end_time() and <= end_ts.start_time()!"
    ip_error5 = "time must be >= self.start_time() and <= self.end_time()!"
    ip_error6 = "start_ts.end_time() must be < end_ts.start_time()!"
    
    # value()
    val_error1 = "time must be of type datetime.datetime!"
    
    # value()
    slice_error1 = "time must be of type sptemp.zeit.Time_Period!"
    slice_error2 = "slice produces empty Interpolator. Either time.start or time.end must be contained in timespan of Interpolator!"
    
    # append()
    app_error1 = "Value must be of type sptemp.zeit.TS_Unit!"
    app_error2 = "Value.start_time() must equal Interpolator.end_time()"
    
    # insert()
    in_error1 = "Value must be of type sptemp.zeit.TS_Unit!"
    in_error2 = "Either value.start_time() or value.end_time() must be >= Interpolator.start_time() and <= Interpolator.end_time()!"
    
    # delete()
    delete_error1 = "time must be of type sptemp.zeit.Time_Period!"
    delete_error2 = "Interpolator object cannot be empty!"
    delete_error3 = "Invalid time. Time must overlap Interpolator.start_time() or Interpolator.end_time()!"
    
class MO_Texts:
    
    # init()
    init_error1 = "Empty instantiation not possible!"
    init_error2 = "ts_object_list must be list holding objects of type sptemp.zeit.TS_Object!"
    init_error3 = "interpolator must be of type sptemp.zeit.Interpolator!"
    init_error4 = "TS_Objects must have same type!"
    init_error5 = "ts_object_list must be time-sorted and TS_Objects must be disjoint!"
    
    # setitem()
    set_error1 = "Index must be of type integer! Slices not allowed"
    set_error2 = "Value must be of type TS_Object!"
    set_error3 = "Value.type must be equal to self.type!"
    set_error4 = "Index out of range!"
    set_error5 = "Value and existing TS_Objects in Moving_Object are not disjoint!"
    
    # delitem()
    del_error1 = "key must be of type interger or slice!"
    del_error2 = "Moving_Object cannot become empty!"
    
    # interpolate()
    i_error1 = "time must be of type datetime.datetime!"
    i_error2 = "time must be >= self.start_time() and <= self.end_time()!"
    i_error3 = "Interpolator must return TSO_object with same type as self.type!"
    
    # slice()
    slice_error1 = "Time must be of type sptemp.zeit.Time_Period!"
    slice_error2 = "interpolator must be of type sptemp.zeit.Interpolator!"
    slice_error3 = "Slice is empty!"
    
    # resampled_slice()
    re_slice_error1 = "Times must be of type slice!"
    re_slice_error2 = "Lenght of times must be > 1!"
    re_slice_error3 = "interpolator must be of type sptemp.zeit.Interpolator!"
    
    # prev_ts()
    prev_error1 = "Time must be of type datetime.datetime!"
    
    # append()
    app_error1 = "Value must be of type spetemp.zeit.TS_Object!"
    app_error2 = "Value.start_time() must be > Moving_Object.end_time()"
    
    # insert()
    in_error1 = "Value must be of type spetemp.zeit.TS_Object!"
    in_error2 = "Value.ts and timestamps of esisting TS_Objects in Moving_Object must be disjoint!"
    in_error3 = "Value.type must be equal to self.type!"
    
    # delete()
    delete_error1 = "Time must be of type sptemp.zeit.Time_Period!"
    delete_error2 = "Moving_Object cannot become empty!"
    
class TS_Geometry_Texts:
    
    # __init__():
    init_error1 = "Value must be of type shapely.geometry!"
    init_error2 = "Value must not be empty!"
    init_error3 = "crs must be of type pyproj.Proj!"
    
    # value()
    v_error1 = "value must be equal to self.type!"
    v_error2 = "self.has_z and value.has_z must be equal!"
    
    # reproject()
    r_error1 = "TS_Geometry has no coordinate reference system!"
    r_error2 = "to_crs must be of type pyproj.Proj!"
    
class TS_Point_Texts:
    
    # __init__():
    init_error1 = "Value must be of type shapely.geometry.Point!"
    init_error2 = "Point must not be empty!"
    init_error3 = "crs must be of type pyproj.Proj!"
    
    # value()
    v_error1 = "value must be of type shapey.geometry.Point!"
    v_error2 = "self.has_z and value.has_z must be equal!"
    
    # reproject()
    r_error1 = "TS_Point has no coordinate reference system!"
    r_error2 = "to_crs must be of type pyproj.Proj!"
    
class MG_Texts:
    
    # within
    w_error1 = "another must be of type shapely.geometry or TS_Geometry or Moving_Geometry or Moving_Collection!"
    w_error2 = "timedelta must be positive!"
    w_error3 = "td1 must be larger or equal to td2!"

class MP_Texts:
    
    # __init__()
    init_error1 = "ts_objects_list can only elements of type sptemp.moving_geometry.TS_Points!"
    init_error2 = "coordinate reference system of all TS_Points in ts_object_list must be equal!"
    init_error3 = "TS_Point.has_z must be equal for all TS_Points in ts_object_list!"
    
    # __setitem__()
    set_error1 = "value must be of type sptemp.moving_geometry.TS_Point!"
    
    # __append__()
    app_error1 = "value must be of type sptemp.moving_geometry.TS_Point!"
    
    # insert()
    in_error1 = "value must be of type sptemp.moving_geometry.TS_Point!"
    
    # reproject()
    re_error1 = "Moving_Object has no coorinate reference system!"
    
class TS_LineString_Texts:
    
    # __init__():
    init_error1 = "Value must be of type shapely.geometry.LineString!"
    init_error2 = "LineString must not be empty!"
    init_error3 = "crs must be of type pyproj.Proj!"
    
    # value()
    v_error1 = "value must be of type shapey.geometry.LineString!"
    v_error2 = "self.has_z and value.has_z must be equal!"
    
    # reproject()
    r_error1 = "TS_LineString has no coordinate reference system!"
    r_error2 = "to_crs must be of type pyproj.Proj!"
    
class ML_Texts:
    
    # __init__()
    init_error1 = "ts_objects_list can only elements of type sptemp.moving_geometry.TS_LineString!"
    init_error2 = "coordinate reference system of all TS_LineStrings in ts_object_list must be equal!"
    init_error3 = "TS_LineSTring.has_z must be equal for all TS_LineStrings in ts_object_list!"
    
    # __setitem__()
    set_error1 = "value must be of type sptemp.moving_geometry.TS_LineString!"
    
    # __append__()
    app_error1 = "value must be of type sptemp.moving_geometry.TS_LineString!"
    
    # insert()
    in_error1 = "value must be of type sptemp.moving_geometry.TS_LineString!"
    
    # reproject()
    re_error1 = "Moving_Object has no coordinate reference system!"
    
class TS_LinearRing_Texts:
    
    # __init__():
    init_error1 = "Value must be of type shapely.geometry.LinearRing!"
    
class MLR_Texts:
    
    # __init__()
    init_error1 = "ts_objects_list can only elements of type sptemp.moving_geometry.TS_LinearRing!"
    init_error2 = "coordinate reference system of all TS_LinearRings in ts_object_list must be equal!"
    init_error3 = "TS_LinearRing.has_z must be equal for all TS_LinearRings in ts_object_list!"
    
    # __setitem__()
    set_error1 = "value must be of type sptemp.moving_geometry.TS_LinearRing!"
    
    # __append__()
    app_error1 = "value must be of type sptemp.moving_geometry.TS_LinearRing!"
    
    # insert()
    in_error1 = "value must be of type sptemp.moving_geometry.TS_LinearRing!"
    
class MC_Texts:
    
    # __init__()
    init_error1 = "moving_list cannot be empty!"
    init_error2 = "moving_list must be of type list!"
    init_error3 = "moving_list can only contain values of type Moving_Point, Moving_LineString and Moving_Polygon!"
    
    # interpolate()
    ip_error1 = "time must be of type datetime.datetime!"
    ip_error2 = "args_dict must be of type dict!"
    
    # slice()
    slice_error1 = "time must be type sptemp.zeit.TimePeriod!"
    slice_error2 = "interpolator_dict must be of type dict!"
    
    # resampled_slice()
    re_slice_error1 = "Times must be of type slice!"
    re_slice_error2 = "Lenght of times must be > 1!"
    re_slice_error3 = "interpolator must be of type dict!"
    
class MPL_Texts:
    
    # __init__()
    init_error1 = "exterior ring must be of type sptemp.moving_geometry.Moving_LinearRing!"
    init_error2 = "interior rings must be of type list!"
    init_error3 = "interior ring must be of type sptemp.moving_geometry.Moving_LinearRing!"
    
    # interpolate()
    ip_error1 = "time must be of type datetime.datetime!"
    ip_error2 = "args_dict must be of type dict!"
    
    # slice()
    slice_error1 = "time must be of type sptemp.zeit.Time_Period!"
    slice_error2 = "interpolator_dict must be of type dict!"
    
class MMP_Texts:
    
    # __init__()
    init_error1 = "moving_list cannot be empty!"
    init_error2 = "moving_list must be of type list!"
    init_error3 = "moving_list can only contain values of type Moving_Point!"
    
    
class MML_Texts:
    
    # __init__()
    init_error1 = "moving_list cannot be empty!"
    init_error2 = "moving_list must be of type list!"
    init_error3 = "moving_list can only contain values of type Moving_LineString!"
    
class MMPL_Texts:
    
    # __init__()
    init_error1 = "moving_list cannot be empty!"
    init_error2 = "moving_list must be of type list!"
    init_error3 = "moving_list can only contain values of type Moving_Polygon!"
    
    # slice()
    slice_error1 = "time must be type sptemp.zeit.TimePeriod!"
    slice_error2 = "interpolator_dict must be of type dict!"

class MG_Helper_Texts:
    
    # has_z_equal()
    hz_error1 = "has_z and has_z must be consistent!"
    
    # crs_equal()
    crs_error1 = "crs must be consistent!"
    
class IC_Texts:
    
    # linear()
    error1 = "start_ts AND end_ts must be of type sptemp.zeit.TS_Object!"
    error2 = "Time must be of type datetime.datetime!"
    error3 = "start_ts.type must be equal to end_ts.type"
    error4 = "start_ts must lay before end_ts on the time_axis"
    
class IPoint_Texts:
    
    # linear_point()
    lp_error1 = "start_ts and end_ts must be of type sptemp.moving_geometry.TS_Point!"
    lp_error2 = "time must be of type datetime.datetime!"
    lp_error3 = "start_ts.has_z must be equal to end_ts.has_z!"
    lp_error4 = "start_ts must lay before end_ts on the time_axis!"
    lp_error5 = "time must be >= start_ts.end_time() and <= end_ts.start_time()!"
    lp_error6 = "start_ts.crs must be equal to end_ts.crs!"
    
    # curve_point()
    c_error1 = "start_ts and end_ts must be of type sptemp.moving_geometry.TS_Point!"
    c_error2 = "time must be of type datetime.datetime!"
    c_error3 = "curve must be of type shpely.geometry.LineString!"
    c_error4 = "start_ts.has_z, end_ts.has_z and curve.has_z must be equal!"
    c_error5 = "start_ts.crs must be equal to end_ts.crs!"
    c_error6 = "start_ts must lay before end_ts on the time_axis"
    c_error7 = "time must be >= start_ts.end_time() and <= end_ts.start_time()!"
    c_error8 = "start_ts.value must be equal to start point of curve and end_ts.value must be equal to end point of curve!"
    
class ICurve_Texts:
    
    # basic_linear()
    bl_error1 = "start_ts and end_ts must be of type sptemp.moving_geometry.TS_LineString!"
    bl_error2 = "time must be of type datetime.datetime!"
    bl_error3 = "start_ts.has_z and end_ts.has_z must be equal!"
    bl_error4 = "start_ts.crs must be equal to end_ts.crs!"
    bl_error5 = "start_ts must lay before end_ts on the time_axis"
    bl_error6 = "time must be >= start_ts.end_time() and <= end_ts.start_time()!"
    bl_error7 = "s_type must be in ['angle', 'distance']!"
    
class IRing_Texts:
    
    # linear_translation()
    lt_error1 = "start_ts and end_ts must be of type sptemp.moving_geometry.TS_LinearRing!"
    lt_error2 = "time must be of type datetime.datetime!"
    lt_error3 = "start_ts.has_z and end_ts.has_z must be equal!"
    lt_error4 = "start_ts.crs must be equal to end_ts.crs!"
    lt_error5 = "start_ts must lay before end_ts on the time_axis"
    lt_error6 = "time must be >= start_ts.end_time() and <= end_ts.start_time()!"
    lt_error7 = "s_type must be in ['angle', 'distance']!"
    
class IHelper_Texts:
    
    # linear_point()
    lp_error1 = "invalid coordinate dimensions!"
    
    # angle()
    ang_error1 = "invalid coordinate dimensions!"
    
class SPT_Texts:
    
    # __init__()
    init_error1 = "dataframe must be of type pandas.DataFrame!"
    init_error2 = "Geometry column must have name 'geometry'!"
    #init_error3 = "empty instantiation not possible!"
    init_error4 = "crs must be of type pyproj.Proj!"
    init_error5 = "Geometry type must be shapely.geometry or Moving_Point, Moving_LineString, Moving_LinearRing or Moving_Collection!"
    
    # interpolate
    ip_error1 = "time must be of type datetime.datetime!"
    ip_error2 = "args must be stored in dict for Moving_Collections and in list for Moving_Objects!"
    
    # slice
    slice_error1 = "time must be of type sptemp.zeit.Time_Period!"
    
    # reproject
    re_error1 = "If geometry column holds values of type shapely.geometry SPT_DataFrame.crs has to be set for reprojection!"
    re_error2 = "to_crs must be of type pyproj.Proj!"
    
    # read_from_json
    rj_error1 = "File does not exist!"
    rj_error2 = "interpolator_dict must of type dict!"
    rj_error3 = "For empty instantiation, column_names must be defined!"
    
    
    
    
    