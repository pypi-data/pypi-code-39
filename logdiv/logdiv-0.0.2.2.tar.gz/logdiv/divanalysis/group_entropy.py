import numpy as np

def cluster_entropy(session_data, group, classification_column):
    """
    Calculate entropy and IEUC of group
    
        Parameters
    ----------
        session_data: pandas dataframe of sessions
        
        group: group wanted to analyse
        
        classification_column: string, classification_column used to calculate entropy
                    
    Returns
    -------
        2 dict
    """
    entropy_vector = {}
    ieuc_vector = {}
    for sub_group in session_data[group].unique():
        entropy_vector[sub_group] = session_data[session_data[group] == sub_group][classification_column+'_entropy'].mean()
        ieuc_vector[sub_group] = np.power(2,entropy_vector[sub_group])
        
    return entropy_vector,ieuc_vector;
