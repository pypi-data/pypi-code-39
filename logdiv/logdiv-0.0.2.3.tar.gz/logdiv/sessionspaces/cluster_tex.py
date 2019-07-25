import numpy as np

def proportional_abundance(weblog_tmp,field):
    weblog_tmp = weblog_tmp.copy(deep = True)
    if weblog_tmp.shape[0]==0:
        raise AssertionError('Empty weblog.')
    histogram=weblog_tmp[field].value_counts()
    pa_df=histogram/histogram.values.sum()
    if abs(1.0-pa_df.values.sum())>1e-8:
        raise AssertionError("ERROR: Proportional abundance distribution does not sum up to one.")
    return pa_df.values,list(pa_df.index);

def ShannonEntropy(P,normalize=False):
    P=np.array(P)
    if normalize:
        P=P/P.sum()
    P=P[P>1e-20]
    return -np.sum(P*np.log2(P));

def cluster_tex(f, session_data_threshold,weblog,cluster_type,classification_column,entropy_group,ieuc_group):
    """
    Write in latex the number of sessions, entropy, ieuc, entropy indvidual, ieuc individual of each cluster
    
    Parameters
    ----------   
        f: file
        
        session_data_threshold: pandas dataframe of sessions
    
        weblog: pandas dataframe of requests
        
        cluster_type: string, cluster type wanted
        
        classification_column: string, classification_column with which calculate diversity

        entropy_group: numpy array, recupered with function "group_entropy"
        
        ieuc_group: numpy array, recupered with function "group_entropy"

    Returns
    -------
        File
    """
    f.write("\n% 3. Clusterization")
    f.write("\n\\newcommand{\\%s}{%d}"%('TotalNumberClusters',len(session_data_threshold[cluster_type].unique())))
    f.write("\n\\newcommand{\\%s}{%s}"%('ClustersType',cluster_type.replace('_',' ')))    
    columns_latex = '|'+'c|'*len(session_data_threshold[cluster_type].unique())
    f.write("\n\\newcommand{\\%s}{%s}"%('ColumnsLatex',columns_latex))        
    cluster_list = []
    sessions_clusters = []
    pc_sessions_clusters = []
    entropy_clusters = []
    ieuc_clusters = []
    entropy_ind_clusters = []
    ieuc_ind_clusters = []
    cluster_ids = session_data_threshold[cluster_type].unique()
    cluster_ids.sort()
    for cluster_id in cluster_ids:
        cluster_list.append(str(cluster_id))
        sessions_clusters.append(str(session_data_threshold[session_data_threshold[cluster_type]==cluster_id].shape[0]))
        pc_sessions_clusters.append(str(round(100.0*session_data_threshold[session_data_threshold[cluster_type]==cluster_id].\
                                              shape[0]/session_data_threshold.shape[0],2)))
        
        cluster_session_list=session_data_threshold[session_data_threshold[cluster_type]==cluster_id].session_id.values
        temp_cluster_weblog=weblog[weblog.session_id.isin(cluster_session_list)]
        pa,pa_names = proportional_abundance(temp_cluster_weblog,'requested_'+classification_column)
        cluster_entropy=ShannonEntropy(pa,normalize=True)
        
        entropy_clusters.append(str(round(cluster_entropy,2)))
        ieuc_clusters.append(str(round(np.power(2.0,cluster_entropy),2)))
        entropy_ind_clusters.append(str(round(entropy_group[cluster_id],2)))
        ieuc_ind_clusters.append(str(round(ieuc_group[cluster_id],2)))

        del temp_cluster_weblog
    f.write("\n\\newcommand{\\%s}{%s}"%('ClusterList',' & '.join(cluster_list)))
    f.write("\n\\newcommand{\\%s}{%s}"%('SessionsClusters',' & '.join(sessions_clusters)))
    f.write("\n\\newcommand{\\%s}{%s}"%('PCSessionsClusters',' & '.join(pc_sessions_clusters)))
    f.write("\n\\newcommand{\\%s}{%s}"%('EntropyClusters',' & '.join(entropy_clusters)))
    f.write("\n\\newcommand{\\%s}{%s}"%('IEUCClusters',' & '.join(ieuc_clusters)))
    f.write("\n\\newcommand{\\%s}{%s}"%('EntropyIndividualClusters',' & '.join(entropy_ind_clusters)))
    f.write("\n\\newcommand{\\%s}{%s}"%('IEUCIndividualClusters',' & '.join(ieuc_ind_clusters)))
    return f;
