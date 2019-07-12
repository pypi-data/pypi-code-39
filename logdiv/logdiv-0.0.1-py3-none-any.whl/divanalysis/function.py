import numpy as np

def proportional_abundance(weblog_tmp,field):
    """
    Calculate proportion of each sub-field in field columns
    """
    weblog_tmp = weblog_tmp.copy(deep = True)
    if weblog_tmp.shape[0]==0:
        raise AssertionError('Empty weblog.')
    histogram=weblog_tmp[field].value_counts()
    pa_df=histogram/histogram.values.sum()
    if abs(1.0-pa_df.values.sum())>1e-8:
        raise AssertionError("ERROR: Proportional abundance distribution does not sum up to one.")
    return pa_df.values,list(pa_df.index);

def rearrange_pa_relative_labels(pa,reference_labels,actual_labels):
    pa_out=np.zeros((len(reference_labels)))
    for i in range(len(reference_labels)):
        if reference_labels[i] in actual_labels:
            pa_out[i]=pa[actual_labels.index(reference_labels[i])]
    return pa_out;

def ShannonEntropy(P,normalize=False):
    """
    Calculate Shannon entropy
    """
    P=np.array(P)
    if normalize:
        P=P/P.sum()
    P=P[P>1e-20]
    return -np.sum(P*np.log2(P));

def zf(s):
    """
    Number digit with a '0'
    """
    s=str(s)
    if len(s)==1:
        return '0'+s;
    else:
        return s;
