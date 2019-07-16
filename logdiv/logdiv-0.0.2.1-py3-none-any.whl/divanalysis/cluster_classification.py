from .matrix_calculator import compute_browsing_matrix
from .matrix_calculator import compute_diversifying_matrix
import time as timelib
import numpy as np

def cluster_classification(weblog, session_data_threshold, cluster_type, categories, verbose = False):
    """
    Call function of matrix_calculator.py to return matrices for each cluster. 
    Select requested_category of weblog that are only in entry "categories"
    """
    if verbose== True:
        start_time = timelib.time()
        print("\n   * Computing cluster matrices ...")    
    categories = list(set(categories)-{'social','search','other'})
    browsing_matrix = {}
    diversifying_matrix = {}
    # Selecting sessions from each cluster
    for cluster_id in session_data_threshold[cluster_type].unique():
        sessions_cluster = session_data_threshold[session_data_threshold[cluster_type]==cluster_id].session_id
        divpat_log = weblog[weblog.session_id.isin(sessions_cluster)]
        # Filtering some requests
        divpat_log=divpat_log[divpat_log.requested_category.isin(categories)]
        divpat_log=divpat_log[divpat_log.referrer_category.isin(categories)]
        
         # Defining matrices
        diversity_columns=('referrer_topic','requested_topic')
        browsing_matrix[cluster_id],_ = compute_browsing_matrix(divpat_log,'referrer_category','requested_category',labels=categories)
        diversifying_matrix[cluster_id],_ = compute_diversifying_matrix(divpat_log,'referrer_category','requested_category',\
                                                                             diversity_columns,labels = categories)
    if verbose == True:
        print("     Cluster matrices computed in %.1f seconds."%(timelib.time() - start_time))
        
    return browsing_matrix, diversifying_matrix;

def star_chain_str(star_chain_index_mean):
    """
    Arbitry choices to associate star-chain index with geometry
    """
    if star_chain_index_mean<=1/3:
        return 'chain';
    elif star_chain_index_mean<=2/3:
        return 'mixed';
    else:
        return 'star';

def length(requests_mean):
    """
    Arbitry choices to associate number of requests with length
    """
    if requests_mean<=5.:
        return 'short';
    elif requests_mean<=10:
        return 'medium';
    else:
        return 'long';
  
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

def cluster_classification_tex(f,browsing_matrix,diversifying_matrix, weblog,session_data_threshold,cluster_type,categories):
    """
    Write on latex file variables that are calculated with cluster classification
    """
    divpat_categories = list(set(categories)-{'social','search','other'})
    divpat_N_categories=len(divpat_categories)
    f.write("\n% 6. Cluster Classification")
    columns_latex = '|'+'c|'*len(session_data_threshold[cluster_type].unique())
    f.write("\n\\newcommand{\\%s}{%s}"%('DivColumnsLatex',columns_latex))      
    columns_blank = ' ' + '& '*(len(session_data_threshold[cluster_type].unique()) -1)
    f.write("\n\\newcommand{\\%s}{%s}"%('DivColumnsBlank',columns_blank))      
    cluster_list = []
    ieuc_clusters = []
    star_chain_like_clusters = []
    length_clusters = []
    browsing_pattern_1 = []
    browsing_pattern_2 = []
    browsing_pattern_3 = []
    diversifying_pattern_1 = []
    diversifying_pattern_2 = []
    diversifying_pattern_3 = []
    cluster_ids = session_data_threshold[cluster_type].unique()
    cluster_ids.sort()
    for cluster_id in cluster_ids:
        cluster_list.append(str(cluster_id))
        
        cluster_session_list=session_data_threshold[session_data_threshold[cluster_type]==cluster_id].session_id.values
        temp_cluster_weblog=weblog[weblog.session_id.isin(cluster_session_list)]
        pa,pa_names = proportional_abundance(temp_cluster_weblog,'requested_topic')
        cluster_entropy=ShannonEntropy(pa,normalize=True)
    
        ieuc_clusters.append(str(round(np.power(2.0,cluster_entropy),2)))
        star_chain_like_clusters.append(star_chain_str(session_data_threshold[session_data_threshold[cluster_type]==cluster_id].star_chain_like.mean()))
        length_clusters.append(length(session_data_threshold[session_data_threshold[cluster_type]==cluster_id].requests.mean()))
        # Browsing patterns
        r,c=np.unravel_index(browsing_matrix[cluster_id][:-1,:-1].argsort(axis=None)[::-1][:3],dims=(divpat_N_categories,divpat_N_categories))
        browsing_pattern_1.append('%.1f\%%: %s$\\rightarrow$%s'%(100.0*browsing_matrix[cluster_id][r[0],c[0]],divpat_categories[r[0]],divpat_categories[c[0]]))
        browsing_pattern_2.append('%.1f\%%: %s$\\rightarrow$%s'%(100.0*browsing_matrix[cluster_id][r[1],c[1]],divpat_categories[r[1]],divpat_categories[c[1]]))
        browsing_pattern_3.append('%.1f\%%: %s$\\rightarrow$%s'%(100.0*browsing_matrix[cluster_id][r[2],c[2]],divpat_categories[r[2]],divpat_categories[c[2]]))
        
        #  Diversifying patterns
        r,c=np.unravel_index(np.nan_to_num(diversifying_matrix[cluster_id])[:-1,:-1].argsort(axis=None)[::-1][:3],dims=(divpat_N_categories,divpat_N_categories))
        diversifying_pattern_1.append('%.1f\%%: %s$\\rightarrow$%s'%(100.0*diversifying_matrix[cluster_id][r[0],c[0]],divpat_categories[r[0]],divpat_categories[c[0]]))
        diversifying_pattern_2.append('%.1f\%%: %s$\\rightarrow$%s'%(100.0*diversifying_matrix[cluster_id][r[1],c[1]],divpat_categories[r[1]],divpat_categories[c[1]]))
        diversifying_pattern_3.append('%.1f\%%: %s$\\rightarrow$%s'%(100.0*diversifying_matrix[cluster_id][r[2],c[2]],divpat_categories[r[2]],divpat_categories[c[2]]))

        del temp_cluster_weblog
    
    f.write("\n\\newcommand{\\%s}{%s}"%('DivClusterList',' & '.join(cluster_list)))
    f.write("\n\\newcommand{\\%s}{%s}"%('DivIEUCClusters',' & '.join(ieuc_clusters)))
    f.write("\n\\newcommand{\\%s}{%s}"%('StarChainClusters',' & '.join(star_chain_like_clusters)))
    f.write("\n\\newcommand{\\%s}{%s}"%('LengthClusters',' & '.join(length_clusters)))
    f.write("\n\\newcommand{\\%s}{%s}"%('BrowsingPatternClustersOne',' & '.join(browsing_pattern_1)))
    f.write("\n\\newcommand{\\%s}{%s}"%('BrowsingPatternClustersTwo',' & '.join(browsing_pattern_2)))
    f.write("\n\\newcommand{\\%s}{%s}"%('BrowsingPatternClustersThree',' & '.join(browsing_pattern_3)))
    f.write("\n\\newcommand{\\%s}{%s}"%('DiversifyingPatternClustersOne',' & '.join(diversifying_pattern_1)))
    f.write("\n\\newcommand{\\%s}{%s}"%('DiversifyingPatternClustersTwo',' & '.join(diversifying_pattern_2)))
    f.write("\n\\newcommand{\\%s}{%s}"%('DiversifyingPatternClustersThree',' & '.join(diversifying_pattern_3)))

    return f;

        

        
    
