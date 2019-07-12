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

def origin(df,category,weblog_columns_dict):
    """
    return True if sessions originate from entry "category" and False else
    """
    if category not in df.referrer_category.unique():
        return False;
    list_requested_page = df[weblog_columns_dict['requested_page_column']].values
    for row in df.itertuples():
        if row.referrer_category == category:
            if df[weblog_columns_dict['referrer_page_column']].at[row.Index] not in list_requested_page:
                return True;
    return False;


def compute_session_features(weblog,pages,session_data,session_features,weblog_columns_dict,main_page_ids=[],verbose = False):
    """
    Calculate entry "session_features" for each sessions and return session_data with added features columns 
    """
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Computing session features ...")
        
    if 'requests' in session_features:
        session_data['requests']=session_data.session_id.map(weblog.session_id.value_counts())
    if 'timespan' in session_features:
        session_data['timespan'] = session_data.apply(lambda row: pd.Timedelta(row.end-row.start).seconds, axis=1)
    if 'category_richness' in session_features:
        session_data['category_richness']=session_data.session_id.map(weblog[['session_id','requested_category']].groupby('session_id').nunique()['requested_category'])
    if 'topic_richness' in session_features:
        session_data['topic_richness']=session_data.session_id.map(weblog[['session_id','requested_topic']].groupby('session_id').nunique()['requested_topic'])
    if 'category_entropy' in session_features:
        pass
    if 'topic_entropy' in session_features:
        # to gain time, calcule entropy for session_data.requests > 1, after that session_data.requests == 1 -> entropy = 0
        list_sessions_reduced = session_data[session_data.requests >1].session_id.values
        weblog_reduced = weblog[weblog.session_id.isin(list_sessions_reduced)]
        entropy = weblog_reduced[["session_id", "requested_topic"]].groupby("session_id").apply(lambda x: x.groupby("requested_topic").aggregate(lambda y: y.count()/x.shape[0]))
        shannon = entropy.session_id.groupby("session_id").apply(lambda x: ShannonEntropy(x.values))
        session_data["topic_entropy"] = session_data.session_id.map(pd.Series(data=shannon.values, index=shannon.index))
        # if session_data.requests==1: session_data.topic_entropy = 0.
        session_data.loc[session_data.topic_entropy!=session_data.topic_entropy,"topic_entropy"] = 0.
    if 'root_social' in session_features:
        origin_social = weblog[[weblog_columns_dict['referrer_page_column'],weblog_columns_dict['requested_page_column'],'referrer_category',\
                                'session_id']].groupby('session_id').aggregate(origin,'social',weblog_columns_dict).referrer_category            
        session_data['root_social'] = session_data.session_id.map(origin_social)
    if 'root_search' in session_features:
        origin_search = weblog[[weblog_columns_dict['referrer_page_column'],weblog_columns_dict['requested_page_column'],'referrer_category',\
                                'session_id']].groupby('session_id').aggregate(origin,'search',weblog_columns_dict).referrer_category            
        session_data['root_search'] = session_data.session_id.map(origin_search)
    if 'main_page' in session_features:
        origin_main = weblog[[weblog_columns_dict['referrer_page_column'], 'session_id']].groupby('session_id').aggregate(lambda x: any([(n in main_page_ids) for n in x]))
        session_data['main_page'] = session_data.session_id.map(origin_main.referrer_page)
    if 'star_chain_like' in session_features:
        scindex = weblog[[weblog_columns_dict['referrer_page_column'], weblog_columns_dict['requested_page_column'], 'session_id']].groupby('session_id').aggregate(lambda x: star_chain_like(x,weblog_columns_dict))
        session_data['star_chain_like'] = session_data.session_id.map(scindex[weblog_columns_dict['referrer_page_column']])
    if 'bifurcation' in session_features:
        pass
    if 'inter_req_sd' in session_features:
        lut=weblog[[weblog_columns_dict['timestamp_column'], 'session_id']].groupby('session_id').aggregate(lambda x: x.timestamp.sort_values().diff().apply(lambda x: x.seconds).std())
        session_data["inter_req_sd"] = session_data.session_id.map(pd.Series(index=lut.index,data=lut[weblog_columns_dict['timestamp_column']]))
    if 'inter_req_mean' in session_features:
        lut=weblog[[weblog_columns_dict['timestamp_column'], 'session_id']].groupby('session_id').aggregate(lambda x: x.timestamp.sort_values().diff().apply(lambda x: x.seconds).mean())
        session_data['inter_req_mean'] = session_data.session_id.map(pd.Series(index=lut.index,data=lut[weblog_columns_dict['timestamp_column']]))

    if verbose == True:
        print("     Session features computed in %.1f seconds."%(timelib.time() - start_time))
    return session_data;
