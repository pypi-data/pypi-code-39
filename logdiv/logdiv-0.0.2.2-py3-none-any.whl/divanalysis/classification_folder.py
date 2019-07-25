import pandas as pd
import time as timelib

def browsing_pattern_best(weblog,referrer_column,requested_column):
    """
    Calculate 3 highest cases of folder browsing matrix
    """
    referrer_labels = weblog[referrer_column].unique()
    requested_labels =weblog[requested_column].unique()
    
    df = pd.DataFrame(columns=['folder_origin','folder_destination','data'])
    
    for requested_label in requested_labels:
        df_tmp = pd.DataFrame(columns=['folder_origin','folder_destination','data'])    
        df_tmp['folder_origin'] = weblog[weblog[requested_column]==requested_label].groupby(referrer_column).size().sort_values(ascending=False).index
        df_tmp['data'] = weblog[weblog[requested_column]==requested_label].groupby(referrer_column).size().sort_values(ascending=False).values
        df_tmp['folder_destination'] = requested_label
        df = pd.concat([df,df_tmp])
        
    for referrer_label in referrer_labels:
        df_tmp = pd.DataFrame(columns=['folder_origin','folder_destination','data'])    
        df_tmp['folder_destination'] = weblog[weblog[referrer_column]==referrer_label].groupby(requested_column).size().sort_values(ascending=False).index
        df_tmp['data'] = weblog[weblog[referrer_column]==referrer_label].groupby(requested_column).size().sort_values(ascending=False).values
        df_tmp['folder_origin'] = referrer_label
        df = pd.concat([df,df_tmp])
        
    df = df.drop_duplicates(subset=['folder_origin','folder_destination'])
    df_count = df.copy(deep=True)
    df['data'] = df['data']/weblog.shape[0]
    df = df.sort_values(by=['data'],ascending=False)
    df  = df.iloc[:3]
    return df,df_count;

def diversifying_pattern_best(weblog,df_count,referrer_column,requested_column,diversity_columns):
    """
    Calculate 3 highest cases of folder diversifying matrix
    """
    weblog = weblog[weblog[diversity_columns[0]]!=weblog[diversity_columns[1]]]
    
    referrer_labels = weblog[referrer_column].unique()
    requested_labels =weblog[requested_column].unique()
    
    df = pd.DataFrame(columns=['folder_origin','folder_destination','data'])
    
    for requested_label in requested_labels:
        df_tmp = pd.DataFrame(columns=['folder_origin','folder_destination','data'])    
        df_tmp['folder_origin'] = weblog[weblog[requested_column]==requested_label].groupby(referrer_column).size().sort_values(ascending=False).index
        df_tmp['data'] = weblog[weblog[requested_column]==requested_label].groupby(referrer_column).size().sort_values(ascending=False).values
        df_tmp['folder_destination'] = requested_label
        df = pd.concat([df,df_tmp])
        
    for referrer_label in referrer_labels:
        df_tmp = pd.DataFrame(columns=['folder_origin','folder_destination','data'])    
        df_tmp['folder_destination'] = weblog[weblog[referrer_column]==referrer_label].groupby(requested_column).size().sort_values(ascending=False).index
        df_tmp['data'] = weblog[weblog[referrer_column]==referrer_label].groupby(requested_column).size().sort_values(ascending=False).values
        df_tmp['folder_origin'] = referrer_label
        df = pd.concat([df,df_tmp])
    
    df = df.drop_duplicates(subset=['folder_origin','folder_destination'])
    df['folder_route'] = df['folder_origin'].astype(str) + '_' + df['folder_destination'].astype(str)
    df_count['folder_route'] = df_count['folder_origin'].astype(str) + '_' + df_count['folder_destination'].astype(str)
    
    df_count = df_count[df_count.folder_route.isin(df.folder_route.values)]
    
    df_count = df_count.sort_values(by=['folder_origin','folder_destination']).reset_index(drop=True)
    df = df.sort_values(by=['folder_origin','folder_destination']).reset_index(drop=True)
    df['data'] = df['data']/df_count['data']

    df = df.sort_values(by=['data'],ascending=False)
    df  = df.iloc[:3]
    
    return df;    
    
def classification_folder(weblog,analysis_column, threshold_requests_per_session, verbose = False):
    """
    Calculate 3 highest values of brwosing and diversifying matrices
    """
    if verbose== True:
        start_time = timelib.time()
        print("\n   * Computing matrix ...")
    
    diversity_columns=('referrer_topic','requested_topic')

    # Selecting sessions with more than N requests
    requests_per_session=weblog.groupby('session_id').size()
    sessions_requests_over_threshold=list(requests_per_session[requests_per_session>threshold_requests_per_session].index)
    divpat_log = weblog[weblog.session_id.isin(sessions_requests_over_threshold)]
    # Filtering some requests
    divpat_log=divpat_log[~divpat_log.requested_category.isin(['social','search','other'])]
    divpat_log=divpat_log[~divpat_log.referrer_category.isin(['social','search','other'])]
    divpat_log=divpat_log[~divpat_log['requested_'+analysis_column].isin([0])]
    divpat_log=divpat_log[~divpat_log['referrer_'+analysis_column].isin([0])]
    # Defining best
    best_browsing_pattern,df_count = browsing_pattern_best(divpat_log,'referrer_'+analysis_column,'requested_'+analysis_column)
    best_diversifying_pattern = diversifying_pattern_best(divpat_log,df_count,'referrer_'+analysis_column,'requested_'+analysis_column,diversity_columns)
    
    if verbose == True:
        print("     Matrix computed in %.1f seconds."%(timelib.time() - start_time))
    return best_browsing_pattern,best_diversifying_pattern;

def class_folder_tex(f,b_matrix,d_matrix):
    """
    Wirte in latex file 3 highest values of brwosing and diversifying matrices
    """
    f.write("\n% 7. Diversifying patterns according to folder classification")
    digit_dic={'0':'Zero','1':'One','2':'Two','3':'Three','4':'Four','5':'Five','6':'Six','7':'Seven','8':'Eight','9':'Nine'}
    i = 0
    for row in b_matrix.itertuples():
        i+=1
        f.write(("\n\\newcommand{\\%s}{%s}"%('FolderBP%sName'%(digit_dic[str(i)]),'%s$\\rightarrow$%s'%(row.folder_origin,row.folder_destination))))
        f.write("\n\\newcommand{\\%s}{%0.1f}"%('FolderBP%sValue'%(digit_dic[str(i)]),100.0*row.data))
    i=0
    for row in d_matrix.itertuples():
        i+=1
        f.write(("\n\\newcommand{\\%s}{%s}"%('FolderDP%sName'%(digit_dic[str(i)]),'%s$\\rightarrow$%s'%(row.folder_origin,row.folder_destination))))
        f.write("\n\\newcommand{\\%s}{%0.1f}"%('FolderDP%sValue'%(digit_dic[str(i)]),100.0*row.data))   
    return f;
    