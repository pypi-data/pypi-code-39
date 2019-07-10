import scipy as sp
import numpy as np
import colorlog
import sparse
import numba

logger = colorlog.getLogger(__name__)

def empty_sparse_vector(size):
    """ Empty sparse vector
    Return a sparse csc vector
    Args:
        size: size of the output vector
    Response:
        an empty sparse csc vector
    """
    return empty_sparse_vector_dok(size).tocsc()

def empty_sparse_vector_dok(size):
    """ Empty sparse dok vector
    Return a sparse dok vector
    Args:
        size: size of the output vector
    Response:
        an empty sparse dok vector
    """
    return sp.sparse.dok_matrix((size, 1))

def sparse_column_vector(np_vector):
    """ Create a sparse column vector
    Create sparse vector from a dense vector
    Args:
        np_vector: a numpy vector
    Reponse:
        A sparse vector copy of the input
    """
    # First we create an empty sparse matrix with
    # the expected shape
    ret = sp.sparse.coo_matrix((np_vector.size, 1), dtype = np_vector.dtype)
    # Then we fill the data. This way we avoid
    # expensive checks in the constructor
    ret.row = np.arange(0, np_vector.size, dtype = np.int32)
    ret.col = np.zeros(np_vector.size, dtype = np.int32)
    ret.data = np_vector
    return ret

def sum_along_rows(matrix):
    """Sum all elements in rows.
    Args:
        matrix: a scipy matrix or numpy array or sparse matrix.
            CSR format is faster.
    Response:
        A numpy array with the summation.
    """
    if sp.sparse.isspmatrix(matrix):
        return (matrix * np.ones((matrix.shape[1], 1))).reshape(-1)
    elif isinstance(matrix, np.ndarray):
        return matrix.sum(axis = 1).reshape(-1)
    elif isinstance(matrix, sparse.COO):
        return matrix.sum(axis = 1).todense().reshape(-1)
    else:
        raise RuntimeError('Format not found')

def sum_along_columns(matrix):
    """Sum all elements in columns."
    Args:
        scipy_matrix: a csc sparse matrix
    Response:
        A numpy array with the summation.
    """
    if sp.sparse.isspmatrix_csc(matrix):
        return internal_sum_along_columns(matrix.indptr, matrix.data)
    elif isinstance(matrix, np.ndarray):
        return matrix.sum(axis = 0).reshape(-1)
    elif isinstance(matrix, sparse.COO):
        return np.asarray(matrix.sum(axis = 0)).reshape(-1)
    else:
        raise RuntimeError('Format not found')

@numba.jit(nopython = True, error_model = 'numpy', parallel = True, fastmath = True)
def internal_sum_along_columns(mat_indptr, mat_data):
    """ Fast implementation for csc matrix for summing along columns
    Args:
        mat_indptr: a numpy vector with the indptr.
        mat_data: a numpy vector with the data.
    Response:
        a numpy vector witht the summation
    """
    size = mat_indptr.size - 1
    summation = np.zeros(size, dtype = mat_data.dtype)
    for i in numba.prange(size):
        col = mat_data[mat_indptr[i]:mat_indptr[i+1]]
        acc = 0
        for val in col:
            acc += val
        summation[i] = acc
    return summation

def left_division(A, s):
    """Divide sparse matrix A by vector s on the left.
    The following multiplication is happening:

    div(A, s) = diag(s) \\ A

    Where diag(s) is the diagonal matrix whose main diagonal
    is formed by vector s.
    Args:
        A: A sparse or dense matrix
        s: a numpy vector
    Response:
        A sparse matrix with the result
    """
    # Instead of divide with do:
    # div(A,s) = diag(1/s) * A
    # compute diag(1/s)
    ss = np.divide(1.0, s, out=np.zeros_like(s, dtype=np.float), where=s!=0)
    if sp.sparse.isspmatrix_csc(A) or isinstance(A, sparse.COO):
        # Multiply does column wise multiplication. We need row-wise.
        #We force A to be csc. This method is available in sp.sparse matrices
        #as well as sparse COO matrices.
        return A.tocsc().T.multiply(ss).T.tocsc() # Hack
    elif isinstance(A, np.ndarray):
        return np.dot(np.diag(ss), A)
    else:
        raise RuntimeError('Format not found')

def right_division(A, s):
    """ Divide sparse matrix A by a vector s on the right.
    The following multiplication is happening:

    div(A, s) = A / diag(s)

    Where diag(s) is the diagonal matrix whose main diagonal
    is formed by vector s.
    Args:
        A: A sparse or dense matrix
        s: a numpy vector
    Response:
        A sparse matrix with the result
    """
    ss = np.divide(1.0, s, out=np.zeros_like(s, dtype = np.float), where=s!=0)
    if sp.sparse.isspmatrix_csc(A) or isinstance(A, sparse.COO):
        return A.tocsr().multiply(ss).tocsc() # Hack
    elif isinstance(A, np.ndarray):
        return np.dot(A, np.diag(ss))
    else:
        raise RuntimeError('Format not found')

def normalise(A):
    """Normalise matrix A according to the sum of each row.
    The normalisation is done by computing the row wise multiplication of each row
    in A. This algorithm is faster than creating a diagonal matrix and multiplying
    both.
    Args:
        A: matrix to normalise.
    Response:
        A normalised version of A in csc sparse format.
    """
    s = sum_along_rows(A)
    return left_division(A, s)

def normalise_col(A):
    """Normalise matrix A according to the sum of each column.
    Args:
        A: matrix to normalise.
    Response:
        A normalised version of A in csc sparse format.
    """
    if sp.sparse.isspmatrix_csc(A):
        # The normalisation result is stored in the same matrix.
        _normalise(A.indptr, A.data)
        return A
    else:
        s = sum_along_columns(A)
        return right_division(A, s)

@numba.jit(nopython = True, parallel = True, fastmath = True)
def _normalise(mat_indptr, mat_data):
    """ Fast implementation of normalisation for CSR/CSC sparse
    matrices. If is CSR matrix, the normalisation is row-based.
    If is CSC matrix, the normalisation is column-based.
    The change is performed over the same data.
    Args:
        mat_indptr: A numpy vector with indice pointers.
        mat_data: A numpy array with the values.
    """
    size = mat_indptr.size - 1
    for i in numba.prange(size):
        col = mat_data[mat_indptr[i]:mat_indptr[i+1]]
        acc = 0
        for val in col:
            acc += val
        # assign value over the same input matrix. No return is performed
        mat_data[mat_indptr[i]:mat_indptr[i+1]] = col / acc

def sparse_vector_to_sparse_diagonal_dia(vec, N):
    """Generate a sparse diagonal from a sparse vector.
    Args:
        vector: A sparse vector (either column or row vector).
        shape: The shape of the expected sparse matrix.
    Response:
        A sparse matrix.
    """
    ret = sp.sparse.dia_matrix((N, N))
    ret.data = vec.toarray().reshape((1, N))
    ret.offsets = np.array([0], dtype = np.int32)
    return ret

def sparse_vector_to_sparse_diagonal_csc(vec, N):
    """Generate a square sparse diagonal from a sparse vector.
    Args:
        vector: A sparse vector (either column or row vector).
        N: the size of the matrix.
    Response:
        A sparse matrix in csc format.
    """
    ret = sp.sparse.csc_matrix((N, N))
    ret.data = vec.data
    ret.indices = vec.indices
    diff = np.diff(np.concatenate(([0], vec.indices, [N])))
    ret.indptr = np.concatenate([np.zeros(1, dtype=np.int32)] +
            [np.full(a,i, dtype=np.int32) for a, i in zip(diff, np.arange(vec.indices.size+1) )]
            )
    return ret

def count_by(in_values):
    """Count equal values.
    Count the number of equal values for each value in
    the input list.
    Args:
        in_values: list of values.
    Response:
        A numpy struct array, where the first element is
        the key value, and the second is the number of
        times key appeared in the input list.
    """
    values = in_values.copy()
    values.sort()
    diff = np.concatenate(([1], np.diff(values)))
    idx = np.concatenate((np.where(diff)[0],[len(values)]))
    index = np.empty(len(idx)-1,dtype='u4,u4')
    index['f0']=values[idx[:-1]]
    index['f1']=np.diff(idx)
    return index

def sparse_eye(n, format = 'csc', dtype = 'float'):
    """Compute an eye matrix
    Create a eye sparse matrix with size (n,n)
    Args:
        n: size of the matrix
        format: Format of the sparse matrix
        dtype: type of the values of the output matrix
    Response:
        A sparse eye matrix of shape (n,n) for the given
        type and format.
    """
    return sp.sparse.identity(n, dtype = dtype, format = format)

def sparse_one(n):
    """Create an sparse matrix column vector of ones
    Args:
        n: number of rows
    Response:
        A sparse matrix with shape (n,1) in csc format
    """
    return sparse_column_vector( np.ones(n)).tocsc()
    #return sp.sparse.coo_matrix((np.ones(n),(np.arange(n), np.zeros(n))),
    #        shape = (n,1)).tocsc()

def sparse_zero(n):
    """ Empty sparse matrix
    Args:
        n: size of the matrix
    Response:
        A sparse matrix in csc format
    """
    return sp.sparse.dok_matrix((n, n)).tocsc()

def corpus2sparse(corpus, num_terms = None, dtype=np.float64, num_docs=None, num_nnz=None, printprogress=0):
    """Create a sparse matrix for corpus
    Similar to gensim.matutils.corpus2csc, here a sparse matrix is created for a given
    corpus. The output is a sparse.COO matrix.
    Args:
        corpus: The corpus to transform
        num_terms: The number of terms in the corpus.
        dtype: The type in the resulting matrix
        num_docs: The number of documents in the corpus.
        num_nnz: The number of nonzero values in the corpus.
        pritprogress: If print the progress.
    Response:
        a sparse.COO matrix
    """
    try:
        # if the input corpus has the `num_nnz`, `num_docs` and `num_terms` attributes
        # (as is the case with MmCorpus for example), we can use a more efficient code path
        if num_terms is None:
            num_terms = corpus.num_terms
        if num_docs is None:
            num_docs = corpus.num_docs
        if num_nnz is None:
            num_nnz = corpus.num_nnz
    except AttributeError:
        pass  # not a MmCorpus...
    if printprogress:
        logger.info("creating sparse matrix from corpus")
    if num_terms is not None and num_docs is not None and num_nnz is not None:
        # faster and much more memory-friendly version of creating the sparse csc
        posnow = 0
        indices_x = np.empty((num_nnz,), dtype=np.int32)
        indices_y = np.empty((num_nnz,), dtype=np.int32)  # HACK assume feature ids fit in 32bit integer
        data = np.empty((num_nnz,), dtype=dtype)
        for docno, doc in enumerate(corpus):
            if printprogress and docno % printprogress == 0:
                logger.info("PROGRESS: at document #%i/%i", docno, num_docs)
            posnext = posnow + len(doc)
            # zip(*doc) transforms doc to (token_indices, token_counts]
            indices_y[posnow: posnext], data[posnow: posnext] = zip(*doc) if doc else ([], [])
            indices_x[posnow: posnext] = [docno]*len(doc)
            posnow = posnext
        assert posnow == num_nnz, "mismatch between supplied and computed number of non-zeros"
        coords = np.vstack([indices_y, indices_x]) #They are inverted as the matrix should be
        result = sparse.COO(coords, data, shape=(num_terms, num_docs))
    else:
        # slower version; determine the sparse matrix parameters during iteration
        num_nnz, data, indices_x, indices_y = 0, [], [], []
        for docno, doc in enumerate(corpus):
            if printprogress and docno % printprogress == 0:
                logger.info("PROGRESS: at document #%i", docno)

            # zip(*doc) transforms doc to (token_indices, token_counts]
            doc_indices, doc_data = zip(*doc) if doc else ([], [])
            indices_y.extend(doc_indices)
            data.extend(doc_data)
            num_nnz += len(doc)
            indices_x.extend([docno]*len(doc_indices))
        if num_terms is None:
            num_terms = max(indices_y) + 1 if indices_y else 0
        num_docs = docno + 1
        # now num_docs, num_terms and num_nnz contain the correct values
        data = np.asarray(data, dtype=dtype)
        coords = np.vstack([indices_y, indices_x]) #They are inverted as the matrix should be
        result = sparse.COO(coords, data, shape=(num_terms, num_docs))
    return result

    return a + trace

def jaccard_norm(intersections, sets_1_length, sets_2_length):
    """ Compute jaccard norm.
    Determine the norm for the given intersections matrix (the dot product,
    between the index and the query, and apply it to the values in the matrix.
    Args:
        intersections: a csc sprase matrix
        sets_1_length: a numpy vector with the sum of the columns of the query.
        sets_2_length: a numpy vector with the sum of the rows of the index.
    Response:
        the intersections matrix with the normalisation applied.
    """
    intersections.data = internal_jaccard_norm(intersections.indptr,
            intersections.indices, intersections.data, sets_1_length, sets_2_length)
    return intersections

@numba.jit(nopython=True, error_model='numpy')
def internal_jaccard_norm(inter_indptr, inter_indices, inter_data, sets_1_length,
        sets_2_length):
    """ Fast implementation to compute jaccard norm.
    Args:
        inter_indptr: a numpy vector with the indptr
        inter_indices: a numpy vector with the indices.
        inter_data: a numpy vector the data.
        sets_1_length: a numpy vector with the sum of the columns of the query.
        sets_2_length: a numpy vector with the sum of the rows of the index.
    """
    x = inter_indptr
    # Create memory to expand sets_1_length
    new_sets_1_length = np.zeros_like(inter_data)
    k = 0
    # For each query length and number of intersections, assign the length
    # to new_sets_1_length
    for i, j in zip(np.diff(x), sets_1_length):
        new_k = k + i
        new_sets_1_length[k:new_k] = j
        k = new_k
    # Retrieve lengths from index for each intersection.
    new_sets_2_length = sets_2_length[inter_indices]
    # Compute norm and apply it.
    norm = new_sets_1_length + new_sets_2_length - inter_data
    return inter_data / norm

@numba.jit(nopython=True, error_model='numpy', parallel=True)
def isin(array1, array2):
    """ Fast version for numpy equivalent isin
    Args:
        array1: numpy array unsorted and not assumed unique
        array2: python set
    Response:
        An numpy boolean array with true for coincidence and false
        otherwise.
    """
    n = array1.shape[0]
    out = np.empty(n, dtype=np.bool_)
    for i in numba.prange(n):
        if array1[i] in array2:
            out[i] = True
        else:
            out[i] = False
    return out

@numba.jit(nopython = True, error_model = 'numpy', parallel = True)
def _argsort_sparse_matrix(indptr, indices, data, shape, max_items):
    """ Parallel argsort for scipy csc sparse matrix
    Args:
        indptr: sparse matrix indptr
        indices: sparse matrix indices
        data: sparse matrix data
        shape: sparse matrix shape
        max_items: number of max items to return per column.
    Response:
        A dense matrix with the arg of the sort for each column. If
        the column has less values than max_items, then missing positions
        are filled with -1.
    """
    m, n = shape
    # Where to store matrix
    out = np.full((max_items, n), -1, dtype = np.int32)
    for i in numba.prange(n):
        data_i = data[ indptr[i]:indptr[i+1] ]
        # do sort
        arg = np.argsort(data_i)[::-1]
        if max_items <= len(arg):
            items = max_items
        else:
            items = len(arg)
        out[:items, i] = arg[:items]
    return out

def argsort_sparse_matrix(csc_matrix, max_items):
    """ Calls equivalent numba function.
    """
    return _argsort_sparse_matrix(csc_matrix.indptr, csc_matrix.indices,
            csc_matrix.data, csc_matrix.shape, max_items)
