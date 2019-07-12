import numpy as np

def cluster_entropy(session_data, group):
    """
    Calucalte entropy and IEUC of group
    """
    entropy_vector = {}
    ieuc_vector = {}
    for sub_group in session_data[group].unique():
        entropy_vector[sub_group] = session_data[session_data[group] == sub_group]['topic_entropy'].mean()
        ieuc_vector[sub_group] = np.power(2,entropy_vector[sub_group])
        
    return entropy_vector,ieuc_vector;
