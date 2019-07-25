import pandas as pd
import numpy as np
import time as timelib

def ShannonEntropy(P,normalize=False):
    P=np.array(P)
    if normalize:
        P=P/P.sum()
    P=P[P>1e-20]
    return -np.sum(P*np.log2(P));

def star_chain_like(weblog,weblog_columns_dict):
    return weblog[~weblog[weblog_columns_dict['requested_page_column']].isin(weblog[weblog_columns_dict['referrer_page_column']])].shape[0]/weblog.shape[0];

def mean_interval_time(weblog,weblog_columns_dict):
    if weblog.shape[0]==0:
        return 0.0
    return weblog[weblog_columns_dict['timestamp_column']].apply(lambda x: pd.Timestamp(x)).diff().apply(lambda x: x.seconds).mean();

def variance_interval_time(weblog,weblog_columns_dict):
    if weblog.shape[0]==0:
        return 0.0
    return weblog[weblog_columns_dict['timestamp_column']].apply(lambda x: pd.Timestamp(x)).diff().apply(lambda x: x.seconds).var()

def compute_session_features(weblog,pages,session_data,session_features,weblog_columns_dict,classification_columns_diversity=[],verbose = False):
    """
    Calculate entry "session_features" for each session and return session_data with added features columns 
    
    Parameters
    ----------
        weblog: pandas dataframe of requests
        
        pages: pandas dataframe of pages
                        
        session_data: pandas dataframe of pages
        
        session_features: list of string, features wanted to compute
                
        weblog_columns_dict: dict recupered with function of 'file_function'
        
        classification_columns_diversity: list of string, if classification_entropy is in sessions_features, calculate entropy of sessions 
                                    for each classification in classification_columns_diversity

    Returns
    -------
        Pandas dataframe
    """    
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Computing session features ...")
        
    if 'requests' in session_features:
        session_data['requests']=session_data.session_id.map(weblog.session_id.value_counts())
    if 'timespan' in session_features:
        session_data['timespan'] = session_data.apply(lambda row: pd.Timedelta(row.end-row.start).seconds, axis=1)
    if 'classification_entropy' in session_features:
        for classification_column in classification_columns_diversity:
        # to gain time, calcule entropy for session_data.requests > 1, after that session_data.requests == 1 -> entropy = 0
            list_sessions_reduced = session_data[session_data.requests >1].session_id.values
            weblog_reduced = weblog[weblog.session_id.isin(list_sessions_reduced)]
            entropy = weblog_reduced[["session_id", "requested_"+classification_column]].groupby("session_id").\
                        apply(lambda x: x.groupby("requested_"+classification_column).aggregate(lambda y: y.count()/x.shape[0]))
            shannon = entropy.session_id.groupby("session_id").apply(lambda x: ShannonEntropy(x.values))
            session_data[classification_column+"_entropy"] = session_data.session_id.map(pd.Series(data=shannon.values, index=shannon.index))
            # if session_data.requests==1: session_data[classification_column+'_entropy'] = 0.
            session_data.loc[session_data[classification_column+'_entropy']!=\
                                         session_data[classification_column+'_entropy'],classification_column+"_entropy"] = 0.
    if 'star_chain_like' in session_features:
        scindex = weblog[[weblog_columns_dict['referrer_page_column'], weblog_columns_dict['requested_page_column'], 'session_id']].groupby('session_id').aggregate(lambda x: star_chain_like(x,weblog_columns_dict))
        session_data['star_chain_like'] = session_data.session_id.map(scindex[weblog_columns_dict['referrer_page_column']])
    if 'inter_req_sd' in session_features:
        lut=weblog[[weblog_columns_dict['timestamp_column'], 'session_id']].groupby('session_id').aggregate(lambda x: x.timestamp.sort_values().diff().apply(lambda x: x.seconds).std())
        session_data["inter_req_sd"] = session_data.session_id.map(pd.Series(index=lut.index,data=lut[weblog_columns_dict['timestamp_column']]))
    if 'inter_req_mean' in session_features:
        lut=weblog[[weblog_columns_dict['timestamp_column'], 'session_id']].groupby('session_id').aggregate(lambda x: x.timestamp.sort_values().diff().apply(lambda x: x.seconds).mean())
        session_data['inter_req_mean'] = session_data.session_id.map(pd.Series(index=lut.index,data=lut[weblog_columns_dict['timestamp_column']]))

    if verbose == True:
        print("     Session features computed in %.1f seconds."%(timelib.time() - start_time))
    return session_data;
