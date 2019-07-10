import numpy as np
import pandas as pd

def dcg_at_k(r, k, form = 0):
    """Discounted cumulative gain (dcg)
    Relevance is positive real values.
    >>> r = np.array([3,2,3,0,0,1,2,2,3,0])
    >>> dcg_at_k(r, 1)
    3.0
    >>> dcg_at_k(r, 2)
    4.26
    >>> dcg_at_k(r, 10)
    8.31
    >>> dcg_at_k(r, 11)
    8.31
    >>> dcg_at_k(r, 10, 1)
    16.80
    Args:
        r: Relevance scores in order
        k: Number of results to consider
        form: scoring system to use
            if 0, it uses r
            if 1, it uses np.power(2, r)
    Returns:
        Discounted cumulative gain
    """
    r = r[:k]
    if r.size:
        pos  = np.arange(1,len(r)+1)
        if form == 0:
            return np.sum((r)/(np.log2(pos+1)))
        elif form == 1:
            return np.sum((np.power(2, r) - 1)/(np.log2(pos+1)))
        else:
            raise ValueError('method must be 0 or 1.')
    return 0.

def ndcg_at_k(r, ideal, k, form = 0):
    """Normalised discounted cumulative gain (ndcg)
    Relevance is positive real values.
    Args:
        r: relevance scores in order
        ideal: relevance scores expected in an ideal system
        k: Number of results to consider
        form: scoring system to use
            if 0, it uses r
            if 1, it uses np.power(2, r)
    Returns:
        Normalised discounted cumulative gain
    """
    dcg_actual = dcg_at_k(r, k, form)
    dcg_ideal = dcg_at_k(ideal, k, form)
    if dcg_ideal > 0:
        return dcg_actual / dcg_ideal
    return 0

def nan_to_zero(r):
    """If r is np.nan then it is transformed into 0
    >>>nan_to_zero(np.nan)
    0
    Args:
        r: number to check
    Returns:
        r as number
    """
    if np.isnan(r):
        return 0
    return r

def ndcg_Ks(actual, Ks):
    """NCDG at every k in Ks for data.
    Data contains the score for a single query or instance.
    It is assumed that 'actual' dataframe have column 'relevance' and 'score'
    Args:
        actual: Dataframe with data to compare
        Ks: List with k-numbers for ncdg@k
    Response:
        A list containing the keys the ncdg@k for every k.
    """
    actual_rel = np.array([ (nan_to_zero(r), s )
                    for r,s in actual[['relevance', 'score']].values
                    if not np.isnan(s) ], dtype = 'u4,f')
    # We sort indirectly to avoid bias towards relevance column
    actual_rel_pos = np.argsort(actual_rel['f1'])[::-1]
    actual_rel = actual_rel[actual_rel_pos]
    actual_rel = actual_rel['f0']
    gt_rel = np.array([ nan_to_zero(r) for r in actual.relevance.values],
            dtype = 'u4')
    return [ ndcg_at_k(actual_rel, np.sort(gt_rel)[::-1], k) for k in Ks ]

def ndcg_Ks_all(actual, Ks):
    """NCDG at every k in Ks for data.
    Data contains several queries or instances.
    It is assumed that 'actual' dataframe has column 'query' and 'types',
    which are used to group by the entities.
    Args:
        actual: Dataframe with data to compare
        Ks: List with k-numbers for ncdg@k
    Response:
        A dataframe containing ncdg@k for every query-type key.
    """
    data = [  [key[0], key[1], ndcg_Ks(group, Ks)]
            for key,group in actual.groupby(['query','type'])]
    new_data = []
    for k0, k1, elem in data:
        entry = [k0, k1]
        for i in range(len(Ks)):
            entry.append(elem[i])
        new_data.append(entry)
    my_columns = ["query", "type"]
    for k in Ks:
        s = "ndcg@{}".format(k)
        my_columns.append(s)
    return pd.DataFrame(new_data, columns = my_columns).set_index(["query","type"])

def evaluate_ndcg(gt_file_path, actual_file_path, Ks):
    gt = pd.read_csv(gt_file_path, sep = '\t', header = None,
            names = ['query','type','entity','relevance'],
            index_col = ['query','type','entity'])
    actual = pd.read_csv(actual_file_path, sep = ' ', header = None,
            names = ['query','type','entity','position','score','algo'],
            index_col = ['query','type','entity'])
    j = actual.join(gt, how = 'outer')
    return ndcg_Ks_all(j, Ks)
