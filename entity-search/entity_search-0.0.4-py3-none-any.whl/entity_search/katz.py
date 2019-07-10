import numpy as np
import scipy as sp
from scipy import sparse
from itertools import groupby
from functools import reduce
from operator import itemgetter
#from .preprocessing import relationship_dict

def get_triples(synset_set):
    """
    Transform a synset set into a set of triples
    """
    return np.array([(synset.id, pointer[1], relationship_dict[pointer[0]] ) 
           for synset in synset_set for pointer in synset.pointers.list], 
        dtype = "u4,u4,u2")

from scipy import sparse
from itertools import groupby

def group_by(in_values):
    """
    Count equal values in a list of values
    """
    values = in_values.copy()
    values.sort()
    diff = np.concatenate(([1], np.diff(values)))
    idx = np.concatenate((np.where(diff)[0],[len(values)]))
    index = np.empty(len(idx)-1,dtype='u4,u4')
    index['f0']=values[idx[:-1]]
    index['f1']=np.diff(idx)
    return index

def get_outgoing_vec(triples, n):
    """
    Count the number of outgoing links for each vertex
    """
    outgoing = group_by(triples['f0'])
    outgoing_vec = np.zeros((n), dtype = 'f')
    outgoing_vec[outgoing['f0']] = 1/outgoing['f1']
    return outgoing_vec

def get_itf_vec(triples):
    """
    Compute ITF score for each relationship type
    """
    rel = group_by(triples['f2'])
    itf_vec = np.zeros((len(rel)), dtype = 'f')
    itf_vec[rel['f0']] = np.log(np.sum(rel['f1'])/rel['f1'])
    return itf_vec

def create_csc_matrix(rel_triples, n):
    """
    Given a triple set, create a sparse csc matrix. It assumes that all
    triples have the same relationship type
    """
    return sparse.coo_matrix((np.ones(len(rel_triples), dtype = 'f'), 
            (rel_triples['f0'], rel_triples['f1'])), shape = (n,n)).tocsc()

def get_matrices(triples, n):
    """
    Given a triple set with many relationship types, create a sparse matrix
    for each relationship. It returns a list of matrices, one for each
    relationship found in the triples.
    """
    sortkeyfn = itemgetter(2)
    return np.array([
        create_csc_matrix(np.array(list(group), dtype = 'u4,u4,u2'), n)
        for key, group in groupby(triples, key=sortkeyfn) ], dtype = 'O')

def get_frequencies(mat):
    """
    Count the number of times a relationship is occurring in mat
    """
    return np.array(mat.sum(axis=1).T.tolist()).flatten()

def pf_score(adjacencies, outgoing_vec):
    """
    Compute PF score for each adjacency matrix. The outgoing_vec contains the
    number of outgoing links for each vertex.
    """
    return np.array([
         sparse.diags(np.multiply(get_frequencies(mat), outgoing_vec), 0)*mat
         for mat in adjacencies ], dtype = 'O')

def pfitf_score(adjacencies, outgoing_vec, itf_vec):
    """
    Compute the PF-ITF score for each adjacency matrix. The ITF scores and
    outgoing links are given. Notice that itf is a single value.
    """
    return np.array([ 
        mat*itf
        for mat, itf in zip(pf_score(adjacencies, outgoing_vec), itf_vec)])

def sum_excl(s1, s2, non):
    """
    Compute exclusivity score for each pair indicated by non and using the 
    summation s1 and s2 (row or column).
    """
    return 1/ (s1[non[0]] + s1[non[1]] + s2[non[0]] + s2[non[1]] - 1)

def get_coo_excl(adj):
    """
    Get the exclusivity matrix in coo format for the given adjacency matrix
    """
    non = adj.nonzero()
    excl = sum_excl(np.array(np.sum(adj, axis = 0)).reshape(-1), 
                    np.array(np.sum(adj, axis = 1)).reshape(-1), non)
    return sparse.coo_matrix((excl, non), shape=adj.shape)
    
def exclusivity_score(adjacencies):
    """
    Produces exclusivity weighting schema for each adjacency matrix in
    adjacencies
    """
    return np.array([ get_coo_excl(adj).tocsc() for adj in adjacencies],
                    dtype = "O")

def triples_to_adjacencies(triples, scoring_system = 0):
    """
    Generate a set of adjacency matrices for the given triples. For each 
    relationship type there will be an adjacency matrix
    """
    # Triples need to be sorted before creating matrix. Otherwise
    # group_by function would be too slow and falty.
    triples = np.sort(triples, order = 'f2')
    n = max( max(triples['f0']), max(triples['f1'])) + 1
    adjacency = get_matrices(triples, n)
    if scoring_system == 0: #Equivalent
        return adjacency
    elif scoring_system == 1: # PF-ITF
        return pfitf_score(adjacency, get_outgoing_vec(triples, n), 
                           get_itf_vec(triples))
    elif scoring_system == 2: # Exclusivity
        return exclusivity_score(adjacency)
    else:
        raise RuntimeError('Scoring system not valid')

def collapse_matrices(adjacencies):
    """
    Given a list of matrices for a set relationships, collapse all matrices
    into a single one. The operation for collapising is addition of the scores
    """
    return reduce(np.add, adjacencies)

def get_adjacency_matrix(synset_set):
    """
    Given a synset set, get a single adjacency matrix
    """
    triples = get_triples(synset_set)
    triples = np.sort(triples, order = ['f2'])
    adjacencies = get_matrices(triples)
    return collapse_matrices(adjacencies)

def katz_operator(T, b, t):
    """
    Compute Katz operator for matrix T with beta(b) parameter for t times.
    """
    n = T.shape[0]
    K = sparse.csc_matrix((n,n), dtype = "u2")
    Ac = sparse.csc_matrix(sparse.identity(n))
    for i in range(0, t):
        Ac = Ac*(b*T)
        K = K + Ac
    return K

def normalise(A):
    """
    Normalise A according to the sum of each row.
    """
    s = np.zeros(A.shape[0])
    ss = np.array(A.sum(axis = 1)).flatten()
    ind = np.where(ss > 0)[0]
    s[ind] = 1/ss[ind]
    D = sparse.dia_matrix((s,0), shape = A.shape).tocsc()
    return D*A

class KatzOperator(object):
    """
    This class produces the accumulation of Katz value. Once initialised, it
    expands the progression until max_t, without accumulating the values.
    Only when the method acc is called, the accumulation is produced, using
    beta as the drop parameter.
    """
    def __init__(self, T, max_t):
        """
        Create and store the geometric progression for T until max_t
        iterations
        """
        self.n = T.shape[0]
        self.latest = sparse.csc_matrix(sparse.identity(self.n))
        self.progression = np.array([ self._next_katz(T) 
                                     for i in range(0, max_t)], dtype = "O")
    
    def _next_katz(self, T):
        """
        Get next value in Katz progression
        """
        _next = self.latest * T
        self.latest = _next
        return self.latest
    
    def acc(self, beta, i):
        """
        Accumulate the values in the progression until element i, using
        beta as drop factor.
        """
        ids = np.arange(0, i).tolist()
        betas = np.array([beta**(_id+1) for _id in ids])
        return reduce(np.add, self.progression[ids]*betas)
        