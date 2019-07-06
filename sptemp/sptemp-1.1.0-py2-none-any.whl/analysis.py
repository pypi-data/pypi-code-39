# -*- coding: utf-8 -*-
"""
This module contains all classes of the "sptemp"-package for analysis of spatio temporal data

Todo:
 
"""
import inspect
import functools
import datetime as dt

import shapely.geometry as sg
import shapely.ops as so
import pandas as pd

from sptemp import moving_geometry as mg
from sptemp import zeit
from sptemp import _texts as text

class SPT_DataFrame(object):
    """This class represents a wrapper for a pandas.DataFrame containing spatio-temporal features.
    The class provides functionality to interpolate and slice the features. The pandas dataframe has to be managed by the user.
    
    >>> geo = [TS_Point(shapely.geometry.Point(11, 10), datetime.datetime(2017, 07, 25, 20, 0, 2)),
    ... TS_Point(shapely.geometry.Point(10, 15), datetime.datetime(2017, 07, 25, 20, 0, 5)),
    ... TS_Point(shapely.geometry.Point(11, 21), datetime.datetime(2017, 07, 25, 20, 0, 4)),
    ... TS_Point(shapely.geometry.Point(11.5, 23.1), Time_Period(datetime.datetime(2017, 07, 25, 20, 0, 0), datetime.datetime(2017, 07, 25, 20, 0, 20)))]
    >>> row_id = ["a", "b", "c", "d"]
    >>> df = pandas.DataFrame({"id":row_id, "geometry":geo})
    >>> SPT_DataFrame(df)
    
    Attributes:
        dataframe (pandas.DataFrame): the pandas dataframe associated with the SPT_DataFrame
        crs (pyproj.Proj or NoneType): The coordinate reference system of the geometries stored in the dataframe.
            Only relevant if geometries are of type 'shapely.geometry'.
        geometry_type (type or NoneType): Type of the objects in the geometry column, returns None if dataframe is empty
    """
    
    # possible types of geometry column
    _sg_classes = [x[1] for x in inspect.getmembers(sg, inspect.isclass)]
    _sg_classes.remove(sg.CAP_STYLE)
    _sg_classes.remove(sg.JOIN_STYLE)
    
    _moving_classes = [mg.Moving_Point, mg.Moving_LineString, mg.Moving_LinearRing, mg.Moving_Collection,
                       mg.Moving_Polygon, mg.Moving_MultiPoint, mg.Moving_MultiLineString, mg.Moving_MultiPolygon]
    
    def __init__(self, dataframe, crs=None):
        """
        Note:
            The columns of the dataframe should only contain objects of one type!
        
        Args:
            dataframe (pandas.dataframe): the pandas dataframe associated with the SPT_DataFrame.
                The geometries of the dataframe must be stored in a column named "geometry".
                The geometry column can contain objects of all TS_Geometry-classes, all shapely.geometry classes
                and all Moving_Geometry Classes 
            crs (pyproj.Proj or NoneType): The coordinate reference system of the geometries stored in the dataframe.
                Only relevant if geometries are represented as shapely.geometry objects.
                
        Raises:
            TypeError: if dataframe is not of type pandas.Dataframe OR if crs not of type pyproj.Proj Or
                if geometry column does contain data that is not of type TS_Geometry, shapely.geometry or
                Moving_Point, Moving_LineString, Moving_Linear_Ring or Moving_Collection
            ValueError: if dataframe does not contain a column named 'geometry'
        """
        if isinstance(dataframe, pd.DataFrame) is False:
            raise TypeError(text.SPT_Texts.init_error1)
        
        elif "geometry" not in dataframe.columns:
            raise ValueError(text.SPT_Texts.init_error2)
        
        elif crs:
            import pyproj
            if isinstance(crs, pyproj.Proj) is False:
                raise TypeError(text.SPT_Texts.init_error4)
            
        # check geometry column
        if len(dataframe.geometry) > 0 and type(dataframe.geometry[dataframe.index[0]]) not in self._sg_classes and\
        type(dataframe.geometry[dataframe.index[0]]) not in self._moving_classes and isinstance(dataframe.geometry[dataframe.index[0]], mg.TS_Geometry) is False:
            raise TypeError(text.SPT_Texts.init_error5)

        self.dataframe = dataframe
        self.crs = crs
        
    @property
    def geometry_type(self):
        return type(self.dataframe.geometry[0]) if len(self.dataframe.geometry) > 0 else None
    
    def interpolate(self, time, args_dict={}):
        """
        Args:
            time (datetime.datetime): time for which values will be interpolated
            args_dict (dict, optional): Dictionary holding the args that will be passed two interpolators. 
                The keys of the dictionary should correspond to the index of the relevant row. The values should be dictionaries,
                in which the keys identify the column name of the object. For Moving_Objects the value should be a list holding the args,
                For Moving_Collections the value should be an args_dict that is specific to the interpolated object type.
                
        Returns:
            sptemp.analysis.SPT_DataFrame: dataframe with interpolated values
            
        Raises:
            TypeError: If time not of type datetime.datetime OR if args in args_dict not of type dict or of type list
        """
        if isinstance(time, dt.datetime) is False:
            raise TypeError(text.SPT_Texts.ip_error1)
        
        return_df = pd.DataFrame({x:[] for x in self.dataframe.columns})
        
        for i in self.dataframe.index:
            
            args = args_dict[i] if i in args_dict else {}
            row = self.dataframe.loc[i]
            
            row_df = pd.DataFrame({x:[row[x]] for x in self.dataframe.columns}, index=[i])
            
            for col in self.dataframe.columns:
                
                if isinstance(row[col], zeit.Moving_Object) or isinstance(row[col], mg.Moving_Collection):
                    if col in args:
                        if isinstance(args[col], dict):
                            ip_ts = row[col].interpolate(time, args[col])
                            row_df.at[i,col] = ip_ts.value if ip_ts else None
                        elif isinstance(args[col], list):
                            ip_ts = row[col].interpolate(time, *args[col])
                            row_df.at[i,col] = ip_ts.value if ip_ts else None
                        else:
                            raise TypeError(text.SPT_Texts.ip_error2)
                    else:
                        ip_ts = row[col].interpolate(time)
                        row_df.at[i,col] = ip_ts.value if ip_ts else None
                        
                elif isinstance(row[col], zeit.TS_Object):
                    if time < row[col].start_time() or time > row[col].end_time():
                        row_df.at[i, col] = None
                    else:
                        row_df.at[i, col] = row[col].value
                        
            # delete rows where geometry is None
            if row_df.geometry[i]:
                return_df = return_df.append(row_df, ignore_index=False)
                
        return SPT_DataFrame(return_df, crs=self.crs)
    
    def slice(self, time):
        """
        Args:
            time (sptemp.zeit.Time_Period): time period for which slice will be returned
        
        Returns:
            sptemp.analysis.SPT_DataFrame: dataframe with sliced values
            
        Raises:
            TypeError: if time not of type sptemp.zeit.Time_Period
        """
        if isinstance(time, zeit.Time_Period) is False:
            raise TypeError(text.SPT_Texts.slice_error1)
        
        return_df = pd.DataFrame({x:[] for x in self.dataframe.columns})
        
        for i in self.dataframe.index:
            
            row = self.dataframe.loc[i]
            
            row_df = pd.DataFrame({x:[row[x]] for x in self.dataframe.columns}, index=[i])
            
            for col in self.dataframe.columns:
                
                if isinstance(row[col], zeit.Moving_Object) or isinstance(row[col], mg.Moving_Collection):
                    
                    row_df.at[i,col] = row[col].slice(time)
                
                # slicing TS_Objects as this class has no method 'slice'        
                elif isinstance(row[col], zeit.TS_Object):
                    new_tso = DF_Helper.get_sliced_ts_object(row[col], time)
                    if new_tso != 'no_change':
                        row_df.at[i,col] = new_tso
                        
            # delete rows where geometry is None
            if row_df.geometry[i]:
                return_df = return_df.append(row_df, ignore_index=False)
                
        return SPT_DataFrame(return_df, crs=self.crs)
    
    def resampled_slice(self, times, time_args={}):
        """
        Returns slice between first time instant of times and last time instant of times.
        Calls resampled slice method of all Moving_Objects in dataframe
        
        Args:
            times (list of datetime.datetime): List of time instants
            time_args (dict, optional): Dictionary holding the time_args that will be passed two Interpolators. 
                The keys of the dictionary should correspond to the index of the relevant row. The values should be dictionaries,
                in which the keys identify the column name of the object. The value then should be a Moving_Object for Moving_Objects
                and Moving_Geometries and for Moving_Collection it should be a dictionary holding Moving_Objects.
            
        Returns:
            sptemp.analysis.SPT_DataFrame or None: Returns resampled-slice of original DataFrame,
            returns None if slice is empty.
            
        Raises:
            TypeError: if type of times is not list
            ValueError: if len(times) < 2
        """
        return_df = pd.DataFrame({x:[] for x in self.dataframe.columns})
        
        for i in self.dataframe.index:
            row = self.dataframe.loc[i]
            t_args = time_args[i] if i in time_args else {}
            
            row_df = pd.DataFrame({x:[row[x]] for x in self.dataframe.columns}, index=[i])
            
            for col in self.dataframe.columns:
                
                if isinstance(row[col], zeit.Moving_Object) or isinstance(row[col], mg.Moving_Collection):
                    if col in t_args:
                        row_df.at[i,col] = row[col].resampled_slice(times, t_args[col])
                    else:
                        row_df.at[i,col] = row[col].resampled_slice(times)
                        
                # slicing TS_Objects as this class has no method 'resampled_slice'        
                elif isinstance(row[col], zeit.TS_Object):
                    time = zeit.Time_Period(times[0],times[-1])
                    new_tso = DF_Helper.get_sliced_ts_object(row[col], time)
                    if new_tso != 'no_change':
                        row_df.at[i,col] = new_tso
                        
            # delete rows where geometry is None
            if row_df.geometry[i]:
                return_df = return_df.append(row_df, ignore_index=False)
                
        return SPT_DataFrame(return_df, crs=self.crs)
    
    def reproject(self, to_crs):
        """Transforms coordinate values in dataframe into new coordinate system
         
        Args:
            to_crs (pyproj.Proj): coordinate reference system to which the coordinates are converted to
             
        Raises:
            TypeError: if to_crs is not of type pyproj.Proj
            ValueError: if geometry column holds values of type shapely.geometry and self.crs is None
        """
        if len(self.dataframe) == 0:
            return
         
        elif self.crs is None and type(self.dataframe.geometry[self.dataframe.index[0]]) in self._sg_classes:
            raise ValueError(text.SPT_Texts.re_error1)
         
        import pyproj
         
        if isinstance(to_crs, pyproj.Proj) is False:
            raise TypeError(text.SPT_Texts.re_error2)
         
        if type(self.dataframe.geometry[self.dataframe.index[0]]) in self._sg_classes:
            project = functools.partial(pyproj.transform, self.crs, to_crs)
            for i in self.dataframe.index:
                self.dataframe.at[i,"geometry"] = so.transform(project, self.dataframe.geometry[i])
                 
            self.crs = to_crs
                 
        else:
            for i in self.dataframe.index:
                self.dataframe.geometry[i].reproject(to_crs)
                
                
class DF_Helper:
    
    @staticmethod
    def get_sliced_ts_object(tso, time):
        """
        Args:
            tso (sptemp.zeit.TS_Object): TS_Object for which slice will be returned
            time (sptem.zeit.Time_Period): Time_Period of slice
            
        Returns:
            sptemp.zeit.TS_Object or None or string: Returnes sliced TS_Object or None 
                or string 'no_change' if TS_Object.ts is included in 'time'
        """
        if time.before(tso.ts) or time.after(tso.ts):
            return None
        
        elif time.includes(tso.ts):
            return 'no_change'
        
        elif isinstance(tso.ts, zeit.Time_Period):
            new_ts = None
                        
            if time.overlaps(tso.ts):
                new_ts = zeit.Time_Period(tso.start_time(), time.end)
                
            elif time.overlappedBy(tso.ts):
                new_ts = zeit.Time_Period(time.start, tso.end_time())
                
            elif (tso.ts).includes(time):
                new_ts = zeit.Time_Period(time.start, time.end)
                
            elif time.meets(tso.ts):
                new_ts = time.end
                
            elif time.metBy(tso.ts):
                new_ts = time.start
            
            if new_ts:
                return tso.__class__(tso.value, new_ts, tso.crs) if isinstance(tso, mg.TS_Geometry) else tso.__class__(tso.value, new_ts)
            else:
                return 'no_change'
                            
            