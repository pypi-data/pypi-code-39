from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import numpy as np
import time as timelib

def supervised(session_data_clustering, features, n_cluster = 3, verbose = False):
    """
    Compute supervised clustering using K-means
    """
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Computing supervised clustering ...")
        
    session_data_clustering = session_data_clustering.copy(deep=True)
    kmeans = KMeans(n_clusters=n_cluster, random_state=0).fit(session_data_clustering[features])
    session_data_clustering['supervised_cluster_id'] = kmeans.labels_
    
    if verbose == True:
        print("     Supervised clustering computed in %.1f seconds"%(timelib.time() - start_time))
        
    return session_data_clustering['supervised_cluster_id'];

def hierarchical(session_data_clustering, list_features, list_n_clusters, verbose = False):
    """
    Compute hierarchical clustering using K-means 
    """
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Computing hierarchical clustering ...")
        
    session_data_clustering = session_data_clustering.copy(deep=True)
    kmeans = KMeans(n_clusters=list_n_clusters[0], random_state=0).fit(session_data_clustering[list_features[0]])
    session_data_clustering["hc_id"] = kmeans.labels_.astype(str)
    for i in np.arange(1,len(list_features)):
        for j in session_data_clustering.hc_id.unique():
            kmeans = KMeans(n_clusters=list_n_clusters[i], random_state=0).fit(session_data_clustering.loc[session_data_clustering.hc_id==j, list_features[i]])
            session_data_clustering.loc[session_data_clustering.hc_id==j, "hc_id"] = session_data_clustering.loc[session_data_clustering.hc_id==j, "hc_id"] + kmeans.labels_.astype(str)
    c_id = list(map(int,session_data_clustering.hc_id.unique()))
    c_id.sort()
    gcid_dic = {}
    gcid = 0
    len_max = len(str(max(c_id)))
    for i in c_id:
        key = '0'*(len_max - len(str(c_id[gcid]))) + str(i) # during conversion str -> int : '00' -> 0 : need to add for gcid
        gcid_dic[key] = gcid
        gcid = gcid + 1
    session_data_clustering["hc_id"] = session_data_clustering["hc_id"].map(gcid_dic)
    
    if verbose == True:
        print("     Hierarchical clustering computed in %.1f seconds"%(timelib.time() - start_time))
        
    return session_data_clustering["hc_id"];

def unsupervised(session_data_clustering, features, verbose = False):
    """
    Compute unsupervised clustering using dbscan
    """
    if verbose == True:
        start_time = timelib.time()
        print("\n   * Computing unsupervised clustering ...")
        
    session_data_clustering = session_data_clustering.copy(deep=True)
    dbscan = DBSCAN(eps = 0.2, min_samples=5).fit(session_data_clustering[features])
    session_data_clustering["unsupervised_cluster_id"] = dbscan.labels_
    
    if verbose == True:
        print("     Unsupervised clustering computed in %.1f seconds"%(timelib.time() - start_time))
        
    return session_data_clustering["unsupervised_cluster_id"];
