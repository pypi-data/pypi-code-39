PATH = "../data/pin_data/"
import datetime
import numpy as np
import pandas as pd
import csv
import time
from typing import List, Tuple, Dict
nested_list_strs = List[List[str]]

#########################################################
##### GENERAL PURPOSE FILE OPENERS AND DICTIONARIES #####

def get_kanton_dict(date: str) -> Dict[str,int]:
    """Returns viewer's Kanton on a given date"""
    with open(f'{PATH}SocDem_{date}.pin','r',encoding='latin-1') as f :
        df_socdem = pd.read_csv(f,dtype='int32',usecols = ['SampleId','Person','SocDemVal5'])
    df_socdem['H_P'] = df_socdem['SampleId'].astype(str) + "_" + df_socdem['Person'].astype(str)
    kanton_dict = {a : b for a,b in zip(df_socdem['H_P'].values.tolist(),
                                         df_socdem['SocDemVal5'].values.tolist())}
    return kanton_dict

def get_station_id(chan_name: str) -> int:
    """Returns the ID of a chan"""
    with open(f'{PATH}Station.pin','r',encoding='latin-1') as f :
        df_sta = pd.read_csv(f)
        if chan_name in df_sta['StationName'].values :
            return df_sta.loc[df_sta['StationName'] == chan_name,'StationID'].values[0]
        elif chan_name in df_sta['StationAbbr'].values :
            return df_sta.loc[df_sta['StationAbbr'] == chan_name,'StationID'].values[0]
        else : print(f"Please provide valid station chan_name, {chan_name} not found in Channel list")
            
def get_station_dict() -> Dict[int,str]:
    """Returns a dictionary mapping station IDs to their names"""
    with open(f'{PATH}Station.pin','r',encoding='latin-1') as f :
        df_sta = pd.read_csv(f)
    return {k : v for k,v in zip(df_sta['StationID'].tolist(),df_sta['StationAbbr'].tolist())}

def get_chan_title_start(df: pd.DataFrame, ch_d: Dict[int,str]):
    """Helper function to return lists of titles, start times, channels, from a df"""
    t = df['Title'].tolist()
    s = df['StartTime'].apply(lambda x : x.strftime("%H%M")).tolist()
    c = df['ChannelCode'].map(ch_d).tolist()
    return c, t, s

def get_weight_dict(date: str) -> Dict[str,float]:
    """Returns viewer's weight on a given date"""
    with open(f'{PATH}Weight_{date}.pin','r',encoding='latin-1') as f:
        df_wei = pd.read_csv(f)

    df_wei['H_P'] = df_wei['SampledIdRep'].astype(str) + "_" + df_wei['PersonNr'].astype(str)
    weight_dict = {a : b for a,b in zip(df_wei['H_P'].values.tolist(),
                                         df_wei['PersFactor'].values.tolist())}
    return weight_dict

def get_lang_dict(date : str) -> Dict[str,int]:
    """Returns viewer's language on a given date"""
    with open(f'{PATH}SocDem_{date}.pin','r',encoding='latin-1') as f :
        df_socdem = pd.read_csv(f,dtype='int32',usecols = ['SampleId','Person','SocDemVal4'])
    df_socdem['H_P'] = df_socdem['SampleId'].astype(str) + "_" + df_socdem['Person'].astype(str)
    lang_dict = {a : b for a,b in zip(df_socdem['H_P'].values.tolist(),
                                         df_socdem['SocDemVal4'].values.tolist())}
    return lang_dict

def get_age_dict(date: str) -> Dict[str,int]:
    """Returns viewer's age on a given date"""
    with open(f'{PATH}SocDem_{date}.pin','r',encoding='latin-1') as f :
        df_socdem = pd.read_csv(f,dtype='int32',usecols = ['SampleId','Person','SocDemVal1'])
    df_socdem['H_P'] = df_socdem['SampleId'].astype(str) + "_" + df_socdem['Person'].astype(str)
    age_dict = {a : b for a,b in zip(df_socdem['H_P'].values.tolist(),
                                         df_socdem['SocDemVal1'].values.tolist())}
    return age_dict

def get_brc(date,seqzero = True) :
    """
    Returns the broadcast file of 'date' with right dtypes
    assigned. Also keeps only sequence number 0
    of segmented programs when seqzero is True.
    """
    with open(f'{PATH}BrdCst_{date}.pin','r',encoding='latin-1') as f :
        brc = pd.read_csv(f,dtype = {'Date' : 'object', 'StartTime' : 'object', 
                                     'ChannelCode' : 'int'})
    # Padding time to 6 digits and to datetime
    brc['StartTime'] = brc['Date'] + brc['StartTime'].str.zfill(6)
    brc['StartTime'] = pd.to_datetime(brc['StartTime'],format='%Y%m%d%H%M%S')
    # Flagging data belonging to the next day, adding 1 day to dates
    new_day_tresh = pd.to_datetime("020000",format='%H%M%S').time()
    brc['add_day'] = (brc['StartTime'].dt.time < new_day_tresh).astype(int)
    brc['StartTime'] += pd.to_timedelta(brc['add_day'],'d')
    # Getting end time from start and duration
    brc['EndTime'] = brc['StartTime'] + pd.to_timedelta(brc['Duration'],'s')
    # By default, returns only BrdCstSeq > 0 for segmented programs 
    if seqzero : brc = brc[~((brc['SumPieces'] > 0) & (brc['BrdCstSeq'] == 0))]
    return brc

######################################
##### PREPROCESSING OF LIVE DATA #####
# Flow: 
# 1. get_live_viewers. -> all live usage from a date
# 2. get_brc. -> all programs from a date
# 3. map_viewers. -> maps viewers to shows from the 2 above files
# 4. df_to_disk. -> saves results to disk.

def get_live_viewers(prog_name=None,start_hour=None,date = "20180101",
                     chan_name = None, guests = False,agemin = 0,agemax = 100) :
    """Helper function to open the Live Usage file for a given date, 
    format it to right dtypes and filter on the parameters passed to the function."""

    with open(f'{PATH}UsageLive_{date}.pin','r',encoding='latin-1') as f : 
        df_usagelive = pd.read_csv(f, dtype = {'HouseholdId' : 'object', 
                                               'IndividualId' : 'object',
                                               'EndTime' : 'object', 
                                               'StartTime' : 'object'})
    
    cond0 = (df_usagelive['AudienceType'] == 1)  # Live Viewing
    if chan_name is not None : 
        cond0 = cond0 & (df_usagelive['StationId'] == get_station_id(chan_name))
    if not guests : 
        cond0 = cond0 & (df_usagelive['IndividualId'].astype(int) < 16) # Guests
    df_usagelive = df_usagelive[cond0]
    
    df_usagelive['H_P'] = df_usagelive['HouseholdId'] + "_" + df_usagelive['IndividualId']

    df_usagelive['Sprache'] = df_usagelive['H_P'].map(get_lang_dict(date))
    df_usagelive = df_usagelive[df_usagelive['Sprache'] == 1] # Filtering on language
    
    df_usagelive['Age'] = df_usagelive['H_P'].map(get_age_dict(date))
    cond2 = (df_usagelive['Age'] >= agemin) & (df_usagelive['Age'] <= agemax) # Filtering on age
    df_usagelive = df_usagelive[cond2] # Filtering on age
    
    # Formating date, start and end time
    ud_str = str(df_usagelive['UsageDate'].iloc[0])
    ud = pd.to_datetime(ud_str,format="%Y%m%d")
    df_usagelive['UsageDate'] = ud 
    
    st_vec = df_usagelive['StartTime'].tolist()
    st_vec = [ud_str + o.zfill(6) for o in st_vec]
    st_vec = pd.to_datetime(st_vec,format="%Y%m%d%H%M%S")
    df_usagelive['StartTime'] = st_vec
    
    et_vec = df_usagelive['EndTime'].tolist()
    et_vec = [ud_str + o.zfill(6) for o in et_vec]
    et_vec = pd.to_datetime(et_vec,format="%Y%m%d%H%M%S")
    df_usagelive['EndTime'] = et_vec
    df_usagelive['add_day'] = (df_usagelive['StartTime'] > df_usagelive['EndTime']).astype(int)
    df_usagelive['EndTime'] += pd.to_timedelta(df_usagelive['add_day'],'d')
    df_usagelive['Weights'] = df_usagelive['H_P'].map(get_weight_dict(date))
    
    # If no channel or program name given, return DF. Otherwise filter further
    if (chan_name is None) | (prog_name is None) : return df_usagelive
    else : return filter_live_usage(df_usagelive,prog_name,start_hour,date,chan_name)

def map_viewers(sched: pd.DataFrame, lv: pd.DataFrame) -> Tuple[nested_list_strs]:
    """
    'sched': schedule dataframe. 'lv': live usage dataframe.
    Maps viewer's live usage to shows.
    """
    out_viewers = []
    out_shows = []
    for index,show in sched.iterrows():
        viewers = get_live_viewers_from_show(show,lv)
        if len(viewers) > 0 : 
            out_viewers.append(viewers)
            out_shows.append(show[['Title','StartTime','EndTime','BrdCstId','Description']])
    return out_viewers, out_shows

def get_live_viewers_from_show(show: pd.Series, live_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters 'live_df' to keep only the viewers of 'show'
    'live_df' is a live_usage dataframe, 'show' is a row from a broadcast dataframe.
    """
    df_live = live_df[live_df['station'] == show['station']].copy()
    df_live['duration'] = (df_live['EndTime'].clip(upper = show["EndTime"]) 
                           - df_live['StartTime'].clip(lower = show['StartTime'])).dt.total_seconds()
    df_live = df_live[df_live['duration'] > 0]
    return df_live

def df_to_disk(vw: nested_list_strs, sh: nested_list_strs, d0: str, d1: str) -> None:
    """Saves a preprocessed PIN file"""
    lens = [[len(l) for l in ls] for ls in vw]
    lens = [o for subo in lens for o in subo]
    
    viewers = [[l for l in ls] for ls in out_viewers]
    viewers = [o for subo in viewers for o in subo]
    viewers = pd.concat(viewers,axis=0)
    
    tits = [[l['Title'] for l in ls] for ls in sh]
    tits = [o for subo in tits for o in subo]
    titls = [[o]*l for o,l in zip(tits,lens)]
    titls = [o for subo in titls for o in subo]
    
    viewers['Title'] = titls
    
    end = [[l['EndTime'] for l in ls] for ls in sh]
    end = [o for subo in end for o in subo]
    ends = [[o]*l for o,l in zip(end,lens)]
    ends = [o for subo in ends for o in subo]
    
    viewers['show_endtime'] = ends
    
    start = [[l['StartTime'] for l in ls] for ls in sh]
    start = [o for subo in start for o in subo]
    starts = [[o]*l for o,l in zip(start,lens)]
    starts = [o for subo in starts for o in subo]
    
    viewers['show_starttime'] = starts
    
    bid = [[l['BrdCstId'] for l in ls] for ls in sh]
    bid = [o for subo in bid for o in subo]
    bids = [[o]*l for o,l in zip(bid,lens)]
    bids = [o for subo in bids for o in subo]
    
    viewers['broadcast_id'] = bids
    
    viewers.to_csv(f"{d0}_{d1}_Live_DE_15_49_mG.csv",index=False)

##############################################
##### PREPROCESSING OF TIME SHIFTED DATA #####
# Flow:
# 1. get_tsv_viewers. -> all shifted usage from a date
# 2. get_brc for 7 days before tsv date -> all programs that ran in the last 7 days
# 3. map_viewers_ovn. -> maps usage to shows, from the 2 above files
# 4. df_to_disk_ovn. -> saves to disk. 

def get_tsv_viewers(prog_name : str = None, start_hour : str = None, 
                    weight_date : str = "20180101", date : str = "20180101",
                    chan_name : str = None, guests : bool = False, 
                    agemin : int = 0, agemax : int = 100) -> pd.DataFrame:
    
    date_cols = ['UsageDate','RecordingDate']
    time_cols = ['ViewingStartTime','ViewingTime','RecordingStartTime']
    
    with open(f'{PATH}UsageTimeShifted_{date}.pin','r',encoding='latin-1') as f : 
        df = pd.read_csv(f, dtype = {**{c : 'object' for c in date_cols},
                                     **{c : 'object' for c in time_cols}})
    
    # Filtering out channels and guests
    cond0 = df['ViewingActivity'].isin([4,10]) # TSV activity
    if chan_name is not None : 
        cond0 = cond0 & (df['StationId'] == pin_functions.get_station_id(chan_name)) 
    if not guests :
        cond0 = cond0 & (df['IndividualId'].astype(int) < 16)
    df = df[cond0]
    
    df['H_P'] = df['HouseholdId'].astype(str) + "_" + df['IndividualId'].astype(str)
    
    # Filtering out based on ages
    df['age'] = df['H_P'].map(pin_functions.get_age_dict(date))
    df = df[(df['age'] >= agemin) & (df['age'] <= agemax)]
    
    # Filtering on language
    df = df[df['H_P'].map(pin_functions.get_lang_dict(date)) == 1]
    
    # Assigining the right dtypes to date cols
    for tc in time_cols[:2] : 
        df[tc] = pd.to_datetime(df['UsageDate'] + df[tc].str.zfill(6), 
                                format = "%Y%m%d%H%M%S")
    df['add_day'] = (df['ViewingStartTime'] > df['ViewingTime']).astype(int)
    df['ViewingTime'] += pd.to_timedelta(df['add_day'],'d')
    
    df['duration'] = df['ViewingTime'] - df['ViewingStartTime']
    df['RecordingStartTime'] = pd.to_datetime(df['RecordingDate'] + 
                                              df['RecordingStartTime'].str.zfill(6), 
                                              format = "%Y%m%d%H%M%S")
    df['RecordingEndTime'] = df['RecordingStartTime'] + df['duration']
    
    # Mapping weights
    df['Weights'] = df['H_P'].map(pin_functions.get_weight_dict(weight_date))
    df['Kanton'] = df['H_P'].map(get_kanton_dict(date))
    return df

def map_viewers_ovn(sched: pd.DataFrame, ovn_df: pd.DataFrame) -> Tuple[nested_list_strs]:
    """
    'sched': schedule dataframe. 'ovn_df': time shifted usage dataframe.
    Maps viewer's time shifted usage to shows.
    """
    out_viewers = []
    out_shows = []
    for index,show in sched.iterrows():
        viewers = get_OVN_viewers_from_show(show,ovn_df)
        if len(viewers) > 0 : 
            out_viewers.append(viewers)
            out_shows.append(show[['Title','StartTime','EndTime','BrdCstId','Description']])
    return out_viewers, out_shows

def get_OVN_viewers_from_show(show: pd.Series, df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters 'df' to keep only the viewers of 'show'
    'df' is a time shifted usage dataframe, show is a row from a broadcast dataframe.
    """
    df = df[df['station'] == show['station']].copy()
    df['duration'] = (df['RecordingEndTime'].clip(upper = show["EndTime"])
                           - df['RecordingStartTime'].clip(lower = show['StartTime'])).dt.total_seconds()
    df = df[df['duration'] > 0]
    return df

def df_to_disk_ovn(vw: nested_list_strs, sh: nested_list_strs, d0: str, d1: str) -> None:
    """Saves a preprocessed PIN file"""
    lens = [[len(l) for l in ls] for ls in vw]
    lens = [o for subo in lens for o in subo]
    
    viewers = [[l for l in ls] for ls in out_viewers]
    viewers = [o for subo in viewers for o in subo]
    viewers = pd.concat(viewers,axis=0)
    
    tits = [[l['Title'] for l in ls] for ls in sh]
    tits = [o for subo in tits for o in subo]
    titls = [[o]*l for o,l in zip(tits,lens)]
    titls = [o for subo in titls for o in subo]
    
    viewers['Title'] = titls
    
    end = [[l['EndTime'] for l in ls] for ls in sh]
    end = [o for subo in end for o in subo]
    ends = [[o]*l for o,l in zip(end,lens)]
    ends = [o for subo in ends for o in subo]
    
    viewers['show_endtime'] = ends
    
    start = [[l['StartTime'] for l in ls] for ls in sh]
    start = [o for subo in start for o in subo]
    starts = [[o]*l for o,l in zip(start,lens)]
    starts = [o for subo in starts for o in subo]
    
    viewers['show_starttime'] = starts
    
    bid = [[l['BrdCstId'] for l in ls] for ls in sh]
    bid = [o for subo in bid for o in subo]
    bids = [[o]*l for o,l in zip(bid,lens)]
    bids = [o for subo in bids for o in subo]
    
    viewers['broadcast_id'] = bids
    
    viewers.to_csv(f"{d0}_{d1}_Timeshifted_DE_15_49_mG.csv",index=False)

##########################
##### POSTPROCESSING #####
# Flow:
# 1. Open the preprocessed files from above
# 2. add_individual_ratings(_ovn) will add a column
#    'individual_Rt-T' that tells how much each viewer
#    contributed to the total Rt-T of a program.
# 3. get the total Rt-T of all shows:
#    df.groupby('broadcast_id')['individual_Rt-T].sum()
# 4. get the total Rt-T of a particular show:
#    df[df[broadcast_id] == XXXX]['individual_Rt-T].sum()

def add_individual_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """Computes Rt-T per viewer, per show"""
    df['segment_duration'] = (df['show_endtime'] - df['show_starttime']).dt.total_seconds()
    
    # Dict: {broadcast_id : total_program_duration} 
    prog_dur_dict = (df.groupby(['broadcast_id','show_starttime'])['segment_duration'].nth(0).to_frame()
                     .groupby('broadcast_id')['segment_duration'].sum().to_dict())
    df['program_duration'] = df['broadcast_id'].map(prog_dur_dict)
    # Rt-T formula
    df['individual_Rt-T'] = df['duration'] * df['Weights'] / df['program_duration']

def add_individual_ratings_ovn(df: pd.DataFrame) -> pd.DataFrame:
    """Computes Rt-T per viewer, per show, for time shifted usage"""
    df['segment_duration'] = (df['show_endtime'] - df['show_starttime']).dt.total_seconds()
    
    # Dict: {broadcast_id : total_program_duration} 
    prog_dur_dict = (df.groupby(['broadcast_id','show_starttime'])['segment_duration'].nth(0).to_frame()
                     .groupby('broadcast_id')['segment_duration'].sum().to_dict())
    df['program_duration'] = df['broadcast_id'].map(prog_dur_dict)
    
    offset_index = (df['show_endtime'] >= df['RecordingEndTime']).astype(int)
    # Very weird infosys magic, adding one arbitrary second. Still waiting for explanations.
    df['duration'] += offset_index
    # Rt-T formula
    df['individual_Rt-T'] = df['duration'] * df['Weights'] / df['program_duration']

####################################################################################################
##### TO DEPRECATE - Need to write better functions for that, to use on the preprocessed files #####

def filter_live_usage(df_usagelive,prog,start,date,chan) :
    """Helper function to filter an usage DF on the segmented programs of a channel"""
    # Was used with "old" pin functions, most probably not needed with the preprocessed PIN files
    cond = False
    sts_dus = get_start_and_dur(prog,start,date,chan)
    for el in sts_dus :
        new_cond = (df_usagelive['EndTime'] >= el[0]) & (df_usagelive['StartTime'] <= el[0] + el[1])
        cond = cond | new_cond
    return df_usagelive[cond & (df_usagelive['StationId'] == get_station_id(chan))]

def get_live_rating(prog_name,start_hour,date,chan_name = None,guests = False,agemin = 0,agemax = 100,viewer_list = None, df_usagelive = None, ma = False) :
    """Compute the live ratings of a program. A live usage file can be optionally passed as parameter."""
    # Was used with "old" pin functions, most probably not needed with the preprocessed PIN files
    if df_usagelive is None:
        df_usagelive = get_live_viewers(prog_name,start_hour,date,chan_name,guests,agemin,agemax)
    else :
        df_usagelive = filter_live_usage(df_usagelive,prog_name,start_hour,date,chan_name)
    if viewer_list is not None:
        # Filtering the df with an optional viewer list
        df_usagelive = df_usagelive[df_usagelive['H_P'].isin(viewer_list)]
    sts_dus = get_start_and_dur(prog_name,start_hour,date,chan_name) # Getting starts and durations of potentially segmented program

    if isinstance(sts_dus[0],list) : # Segmented program
        sts = [o[0] for o in sts_dus]
        dus = [o[1] for o in sts_dus] # durations of seg program
        ends = [get_endzeit(st,du) for st,du in zip(sts,dus)] # Getting end times of segmented program
        num_acc = 0
        denom_acc = 0
        
        # Looping on program segments, computing ratings for each segment, then aggregating
        for st,du,end in zip(sts,dus,ends) :

            cond = (df_usagelive['EndTime'] >= st) & (df_usagelive['StartTime'] <= end) # Filtering on Start and end time
            tp = df_usagelive[cond].copy() # Now the usage file contains only rows on the right show, and on the right viewers

            if tp.shape[0] != 0:
                
                tp['EndTime'].clip(upper=end, inplace=True)
                tp['StartTime'].clip(lower=st, inplace=True)
                tp['Usage'] = tp['EndTime'] - tp['StartTime'] # Computing their usage time on the program
                contrib = (tp['Usage'].apply(lambda x : x.total_seconds())).dot(tp['Weights'].astype('float'))
                #if ma : contrib = contrib / get_live_rating_zs(st.strftime("%H%M"),end.strftime("%H%M"),date,chan_name=None,guests=guests,agemax=agemax,agemin=agemin)
                num_acc = num_acc + contrib #Rt-T formula
            denom_acc = denom_acc + du.total_seconds()
        acc = num_acc/denom_acc   
        if ma : acc = acc / get_live_rating_zs(sts[0].strftime("%H%M"),ends[-1].strftime("%H%M"),date,chan_name=None,guests=guests,agemax=agemax,agemin=agemin)   
    else : # Not a segmented program
        st = sts_dus[0]
        du = sts_dus[1]
        end = get_endzeit(st,du)
        cond = (df_usagelive['EndTime'] >= st) & (df_usagelive['StartTime'] <= end) # Filtering on Start and end time
        tp = df_usagelive[cond].copy() # Now the usage file contains only rows on the right show, and on the right viewers
        if tp.shape[0] == 0 : return 0.0
        tp.loc[:,'Weights'] = tp['H_P'].map(get_weight_dict(date)) # Adding the weights of the viewers
        tp.loc[:,'EndTime'] = tp['EndTime'].apply(lambda x : min(x,end)) # Truncating their view time to the end of the program at maxiumum
        tp.loc[:,'StartTime'] = tp['StartTime'].apply(lambda x : max(x,st)) # Truncating their view time to the beginning of the program at minimum 
        tp.loc[:,'Usage'] = tp['EndTime'] - tp['StartTime'] # Computing their usage time on the program
        return (tp['Usage'].apply(lambda x : x.total_seconds())).dot(tp['Weights'].astype('float'))/(du.total_seconds()*get_live_rating_zs(st.strftime("%H%M"),end.strftime("%H%M"),date,chan_name=None,guests=guests,agemax=agemax,agemin=agemin)) # Rt-T formula
    return acc

def get_live_rating_zs(start_time,end_time,date,chan_name = None,guests = False,agemin = 0,agemax = 100) :
    """Computes ratings for a zeitschiene. I.e. no program name given. Give no channel to get the Rt-T of total TV, used for MA-% computations"""
    # Was used with "old" pin functions, most probably not needed with the preprocessed PIN files
    print(start_time,end_time,date,chan_name)
    df_usagelive = get_live_viewers(prog_name=None,start_hour=start_time,date = date,
                     chan_name = chan_name, guests = guests,agemin = agemin,agemax = agemax)
    start_time = pd.Timestamp.combine(pd.to_datetime(df_usagelive['UsageDate'].iloc[0],format="%Y%m%d"),datetime.datetime.strptime(start_time,"%H%M%S").time())
    end_time = pd.Timestamp.combine(pd.to_datetime(df_usagelive['UsageDate'].iloc[0],format="%Y%m%d"),datetime.datetime.strptime(end_time,"%H%M%S").time())
    df_usagelive.loc[df_usagelive.query('StartTime > EndTime').index,'EndTime'] = df_usagelive.loc[df_usagelive.query('StartTime > EndTime').index,'EndTime'].apply(lambda x : x + datetime.timedelta(hours=24))
    cond = (df_usagelive['EndTime'] >= start_time) & (df_usagelive['StartTime'] <= end_time)
    df_usagelive = df_usagelive[cond].copy()
    df_usagelive.loc[:,'Weights'] = df_usagelive['H_P'].map(get_weight_dict(date))
    df_usagelive.loc[:,'EndTime'] = df_usagelive['EndTime'].apply(lambda x : min(x,end_time))
    df_usagelive.loc[:,'StartTime'] = df_usagelive['StartTime'].apply(lambda x : max(x,start_time))
    df_usagelive.loc[:,'Usage'] = df_usagelive.loc[:,'EndTime'] - df_usagelive.loc[:,'StartTime']
    df_usagelive.loc[:,'WeightedSum'] = (df_usagelive['Usage'].apply(lambda x : x.total_seconds()).astype(int))*df_usagelive['Weights']
    grp = df_usagelive.groupby('H_P')
    grp_us = grp['Usage'].sum().apply(lambda x : x.total_seconds())#.tolist()
    grp_we = grp['Weights'].mean()#.tolist()
    toret = pd.DataFrame([grp_us,grp_we]).T
    toret['UsageDate'] = df_usagelive['UsageDate'].iloc[0]
    return toret['Usage'].dot(toret['Weights'])/(end_time - start_time).total_seconds()

def get_start_and_dur(prog_name,start_hour,date_,chan_name) :
    """Returns exact starting time and duration of program given by prog_name, start_hour, date, chan_name"""
    # Was used with "old" pin functions, most probably not needed with the preprocessed PIN files
    with open(f'{PATH}BrdCst_{date_}.pin','r',encoding='latin-1') as f :
        reader = csv.reader(f,quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL)
        df_brc = pd.DataFrame([l for l in reader])
        df_brc.columns = df_brc.iloc[0,:]
        df_brc.drop(index=0,inplace=True)
    cond = ((df_brc['Title'] == prog_name) & (df_brc['ChannelCode'] == str(get_station_id(chan_name))) 
            & (df_brc['StartTime'].apply(lambda x : x.startswith(start_hour))) & (df_brc["BrdCstSeq"] == "0"))
    if df_brc.loc[cond].shape[0] == 0 :
        print(f"Please provide a valid program title, {prog_name} not found on {chan_name} on the {date_} starting at {start_hour}")
    else :
        progID = df_brc.loc[cond,'BrdCstId'].values[0]
        exact_start = df_brc[df_brc['BrdCstId'] == progID]["StartTime"].values
        duration = df_brc.loc[df_brc['BrdCstId'] == progID,"Duration"].values
        if int(df_brc.loc[df_brc['BrdCstId'] == progID,'SumPieces'].iloc[0]) == 0 : # Not segmented program
            return [[pd.Timestamp.combine(date = pd.to_datetime(str(date_),format="%Y%m%d"), 
                                          time = pd.to_datetime(exact_start[0],format="%H%M%S").time()),
                     datetime.timedelta(seconds=int(duration[0]))]]
        else : # Segmented program, returnging start and durations of all segments
            toret = []
            for i in range(1,int(df_brc.loc[df_brc['BrdCstId'] == progID,'SumPieces'].iloc[0]) + 1) :
                toret.append([pd.Timestamp.combine(date = pd.to_datetime(str(date_),format="%Y%m%d"), 
                                                   time = pd.to_datetime(exact_start[i],format="%H%M%S").time()),
                              datetime.timedelta(seconds=int(duration[i]))])
            return toret

#########################################################
##### DEPRECATED - please use replacement functions #####

def get_endzeit(startzeit,duration) :
    """Returns endzeit from startzeit and duration"""
    return startzeit + duration

def t_conv(t : int) -> datetime.time :
    """Formats time from PIN data."""
    # DEPRECATED - slow as death, please use functions based on 'str'.zfill instead
    # See get_brc() for example.
    # '130' -> '01:30' -> datetime object
    t_ = time_padder(str(t),6)
    t_ = pd.to_datetime(t_,format="%H%M%S").time()
    return t_

def time_padder(t,l) :
    """Pads time from PIN data"""
    # DEPRECATED - slow as death, please use functions based on 'str'.zfill instead
    # See get_brc() for example.
    # '130' -> '0130'
    lt = len(t)
    if lt < l :
        t = "0"*(l - lt) + t
    return t

def get_duration(startzeit,endzeit) :
    
    return endzeit - startzeit

def proc_brc(brc,min_len_sec=None,min_start_h=None,max_start_h = None,seq_nr_zero = False):
    """Helper function to format broadcast file to the right dtypes."""
    # DEPRECATED - use get_brc instead
    brc['BrdCstSeq'] = brc['BrdCstSeq'].astype(int)
    if seq_nr_zero : brc = brc[(brc['BrdCstSeq'] == 0)]
    else : brc = brc[brc['BrdCstSeq']!=0]
    brc['Duration'] = brc['Duration'].astype(int)
    if min_len_sec is not None : 
        brc = brc[(brc['Duration'] > min_len_sec)]
    tm = [o.zfill(6) for o in brc['StartTime'].tolist()]
    brc['StartTime'] = pd.to_datetime(tm,format="%H%M%S")
    brc['StartTime'] = brc['StartTime'].dt.time
    brc['Date'] = pd.to_datetime(brc['Date'])
    brc['StartTime'] = (brc[['Date','StartTime']].T.
                        apply(lambda x : pd.Timestamp.combine(date = x[0], time = x[1])))
    brc["EndTime"] = brc['StartTime'] + pd.to_timedelta(brc["Duration"],unit='s')
    if (min_start_h is not None) & (max_start_h is not None) :
        brc = brc[(brc['StartTime'].apply(lambda x : x.hour) >= min_start_h)
                  | (brc['StartTime'].apply(lambda x : x.hour) < max_start_h)]
    elif (min_start_h is not None) :
        brc = brc[(brc['StartTime'].apply(lambda x : x.hour) >= min_start_h)
                  | (brc['StartTime'].apply(lambda x : x.hour) < 2)]
    elif max_start_h is not None :
        brc = brc[(brc['StartTime'].apply(lambda x : x.hour) < max_start_h)]
    brc['ChannelCode'] = brc['ChannelCode'].astype(int)
    return brc

def op_brc(date) :
    """Opening broadcaster file"""
    # DEPRECATED - use get_brc instead
    with open(f'{PATH}BrdCst_{date}.pin','r',encoding='latin-1') as f :
        reader = csv.reader(f,quotechar='"', delimiter=',',quoting=csv.QUOTE_ALL)
        df_brc = pd.DataFrame([l for l in reader])
        df_brc.columns = df_brc.iloc[0,:]
        df_brc.drop(index=0,inplace=True)
    return df_brc

def get_rt(chan) :
    """Not a helper function, was used to create Cohort Graphs"""
    daily_vw = get_live_rating_zs("200000","222900",daterange_str[0],chan,True,15,49)
    for el in daterange_str[1:] : 
        daily_vw = pd.concat([daily_vw,get_live_rating_zs("200000","222900",el,chan,True,15,49)],axis=0)
    daily_vw.reset_index(inplace=True,level=0)
    daily_vw['Weekday'] = daily_vw['UsageDate'].apply(lambda x : calendar.day_abbr[x.weekday()])
    daily_vw['Month'] = daily_vw['UsageDate'].apply(lambda x : x.month)
    daily_vw['Day'] = daily_vw['UsageDate'].apply(lambda x : x.day)
    stp = []
    for mo in range(1,13) :
        stp.append(daily_vw[daily_vw['Month'] == mo]['H_P'].values.tolist())
    st = [list(set(o)) for o in stp]
    df_rt = pd.DataFrame(columns = [calendar.month_abbr[i] for i in range(1,13)], index = [calendar.month_abbr[i] for i in range(1,13)])
    for ref_month in range(1,13) :
        for month in range(1,13) :
            m_days = set(daily_vw[daily_vw['Month'] == month]['Day'])
            cumrt = []
            for day in m_days : 
                daily = daily_vw[(daily_vw['Month'] == month) & (daily_vw['Day'] == day)] #(daily_vw['H_P'].isin(stich_allmonths)) & (daily_vw['H_P'].isin(st[ref_month-1])) & 
                weights = daily['Weights']
                usage = daily['Usage']
                cumrt.append(weights.dot(usage)/(8940))
            df_rt.iloc[month-1,ref_month-1] = np.mean(cumrt)
            
    return df_rt, st  
