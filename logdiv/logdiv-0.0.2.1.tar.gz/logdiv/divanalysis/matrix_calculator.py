import numpy as np

#################################
# Elementary Matrix Calculators #
#################################

def compute_count_matrix(weblog,referrer_column,requested_column,labels=[]):
    """
    Calculate matrix with category of pages alon lines and colupns,
    number of requests that make transaction in cases
    """
    # retrieving labels
    if len(labels)==0:
        referrer_labels = weblog[referrer_column].unique()
        requested_labels = weblog[requested_column].unique()
    else:
        referrer_labels = labels
        requested_labels = labels
    # Filtering log
    weblog=weblog[(weblog[referrer_column].isin(referrer_labels))&(weblog[requested_column].isin(requested_labels))]
    # The matrix with the values
    matrix=np.zeros((len(referrer_labels)+1,len(requested_labels)+1))
    # Filling the inside of the matrix
    for i,referrer_label in enumerate(referrer_labels):
        for j,requested_label in enumerate(requested_labels):
            matrix[i,j]=weblog[(weblog[referrer_column]==referrer_label)&(weblog[requested_column]==requested_label)].shape[0]
    # Filling the bottom of the matrix
    i=len(referrer_labels)
    for j,requested_label in enumerate(requested_labels):
        matrix[i,j]=weblog[(weblog[requested_column]==requested_label)].shape[0]
    # Filling the right of the matrix
    j=len(requested_labels)
    for i,referrer_label in enumerate(referrer_labels):
        matrix[i,j]=weblog[(weblog[referrer_column]==referrer_label)].shape[0]
    # Filling the bottom-right element of the matrix
    matrix[len(referrer_labels),len(requested_labels)]=weblog.shape[0]

    # Check the matrix is conformal
    if matrix[:-1,:-1].sum()!=matrix[-1,-1]:
        raise AssertionError('Computed Count Matrix is not conformal!')

    return matrix,referrer_labels,requested_labels;

def compute_change_matrix(weblog,referrer_column,requested_column,diversity_columns,labels=[]):
    """
    Same as count matrix, but with just requests that have changed topic
    """
    # retrieving labels
    if len(labels)==0:
        referrer_labels = weblog[referrer_column].unique()
        requested_labels = weblog[requested_column].unique()
    else:
        referrer_labels = labels
        requested_labels = labels
    # Filtering log
    weblog=weblog[(weblog[referrer_column].isin(referrer_labels))&(weblog[requested_column].isin(requested_labels))]
    # Computing the change matrix
    change_matrix=np.zeros((len(referrer_labels)+1,len(requested_labels)+1))
    change_weblog=weblog[weblog[diversity_columns[0]]!=weblog[diversity_columns[1]]]
    for i,referrer_label in enumerate(referrer_labels):
        for j,requested_label in enumerate(requested_labels):
            change_matrix[i,j]=change_weblog[(change_weblog[referrer_column]==referrer_label)&(change_weblog[requested_column]==requested_label)].shape[0]
    # Filling the bottom of the matrix
    i=len(referrer_labels)
    for j,requested_label in enumerate(requested_labels):
        change_matrix[i,j]=change_weblog[(change_weblog[requested_column]==requested_label)].shape[0]
    # Filling the right of the matrix
    j=len(requested_labels)
    for i,referrer_label in enumerate(referrer_labels):
        change_matrix[i,j]=change_weblog[(change_weblog[referrer_column]==referrer_label)].shape[0]
    # Filling the bottom-right element of the matrix
    change_matrix[len(referrer_labels),len(requested_labels)]=change_weblog.shape[0]

    return change_matrix,referrer_labels,requested_labels;

##############################
# Pattern Matrix Calculators #
##############################

def compute_browsing_matrix(weblog,referrer_column,requested_column,labels=[]):
    """
    Count matrix / Sum of all cases in count matrix
    """
    # retrieving labels
    if len(labels)==0:
        labels = list(set(weblog[referrer_column].unique())|set(weblog[requested_column].unique()))
    # retrieving the count matrix
    count_matrix,_,_=compute_count_matrix(weblog,referrer_column,requested_column,labels=labels)
    browsing_matrix=count_matrix/count_matrix[-1,-1]
    return browsing_matrix,labels;


def compute_markov_matrix(weblog,referrer_column,requested_column,labels=[]):
    
    # retrieving labels
    if len(labels)==0:
        labels = list(set(weblog[referrer_column].unique())|set(weblog[requested_column].unique()))
    # retrieving the count matrix
    count_matrix,_,_=compute_count_matrix(weblog,referrer_column,requested_column,labels=labels)
    # Computing markov_matrix
    markov_matrix=np.zeros(count_matrix.shape)
    markov_matrix[:-1,:-1]=count_matrix[:-1,:-1]/(count_matrix[:-1,:-1].sum(axis=1)[:, np.newaxis])
    markov_matrix[:-1,-1]=count_matrix[:-1,-1]/(count_matrix[:-1,-1].sum())
    markov_matrix[-1,:-1]=count_matrix[-1,:-1]/(count_matrix[-1,:-1].sum())
    markov_matrix[-1,-1]=1.0
    return markov_matrix,labels;

def compute_diversifying_matrix(weblog,referrer_column,requested_column,diversity_columns,labels=[],threshold=50):
    """
    Change matrix divised by each correspinding cases in change count matrix
    """
    # retrieving labels
    if len(labels)==0:
        labels = list(set(weblog[referrer_column].unique())|set(weblog[requested_column].unique()))
    # Computing the count and change matrix
    count_matrix,_,_=compute_count_matrix(weblog,referrer_column,requested_column,labels=labels)
    change_matrix,_,_=compute_change_matrix(weblog,referrer_column,requested_column,diversity_columns,labels=labels)
    # Computing the diversifying matrix
    diversifying_matrix=change_matrix/count_matrix
    diversifying_matrix[count_matrix<threshold]=np.nan
    return diversifying_matrix,labels;