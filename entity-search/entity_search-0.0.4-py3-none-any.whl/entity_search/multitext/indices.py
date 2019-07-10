import gensim
import numpy as np
import scipy as sp
from functools import reduce, partial
from itertools import zip_longest
from ..interfaces import TfidfModel
from .similarities import JaccardSimilarity, CosineSimilarity
from ..math import empty_sparse_vector, sparse_column_vector,sparse_vector_to_sparse_diagonal_csc

def simple_wglobal(docfreq, totaldocs):
    return 1

# Normalisations

def unique_words_norm(doc, return_norm = False, average = 1.0):
    """ Compute unique word normalisation for a document
    Args:
        doc: document in bag of word format
        return_norm: Whether return the norm in the result or not.
        average: Average number words in a document in the collection.
    Response:
        a tuple containing a document and the norm value.
    """
    unique_words = len(doc)
    norm = unique_words/average
    if return_norm:
        return (doc, norm)
    return doc

def fit_similarity(similarity, field):
    """ Fit similarity for field.
    Args:
        similarity: Similarity constructor.
        field: A gensim corpus.
    """
    return similarity(field, maintain_sparsity = True,
            num_terms = field.num_terms, num_docs = field.num_docs,
            num_nnz = field.num_nnz)

# Output of a search

class QueryResponseSet(gensim.utils.SaveLoad):
    """This class contains the response of an index
    The response set is composed by sparse vector, each of them containing
    the response for a certain query.
    Args:
        csc_sparse_matrix: a csc sparse matrix
        list_query_names: a list with the names (IDs) of the queries
    """
    def __init__(self, csc_sparse_matrix, list_query_names):
        self.matrix = csc_sparse_matrix
        self.query_names = list_query_names

# indices

class FIndex(gensim.utils.SaveLoad):
    """Base index for multi-fielded corpus. It creates a vector space and
    index for each field in the corpus.
    Args:
        corpus: a multi-field corpus
        weights: the importance of each field in the corpus. It must add to 1.
        similarity: the similarity function to use for indexing.
        args: commands send to similarity constructor
    """
    def __init__(self, corpus, weights):
        self.corpus = corpus
        sum_weights = np.sum(weights)
        if not np.isclose(sum_weights, 1.0):
            raise RuntimeError('Weights must add to 1, found {}'.format(sum_weights))
        self.weights = np.array(weights)
        self.indexes = self._index(self.corpus.fields)

    @classmethod
    def _index(cls, fields):
        """ Index (create similarity indices) fields.
        Args:
            fields: a list of gensim corpus
        Response:
            A list of indices (similarity), one for each field.
        """
        # Keep corpuses that at least have one non-null element.
        # Set to None otherwise
        return [ fit_similarity(cls.similarity, field)
            for field in fields]

    @classmethod
    def _generate_queries(cls, query_field, dtype):
        """ Generate query matrix using the given query model.
        Args:
            query_field: a gensim corpus.
            dtype: the type of the resulting csc matrix
        Response:
            A sparse csc matrix or a list of sparse csc matrices.
        """
        if cls is BM25FIndex:
            # make queries single term. Since BM25 sets queries in the diagonal,
            # we need to create a slightly digional matrix for queries
            trans_queries = ([(term, val)] for q in query_field for term, val in q)
        else:
            # default quries. It produces a column vector with the terms
            trans_queries = (q for q in query_field)
        mat = gensim.matutils.corpus2csc(
                trans_queries, num_terms=query_field.num_terms, num_docs=query_field.num_docs,
                dtype=dtype, printprogress=10000 ).tocsc()
        mat.eliminate_zeros()
        return mat

    @classmethod
    def _prepare_queries(cls, query_corpus, dtype):
        """ For each query model, transform into csc matrix.
        Args:
            query_corpus: a query corpus
            query_model: a tfidf model for queries
            dtype: type for resultin sparse matrices
        Response:
            A list of generated (csc) queries.
        """
        return [cls._generate_queries(query_field, dtype)
                for query_field in query_corpus.fields ]

    @classmethod
    def _tfidf_model_kargs(cls, field):
        """ Generator of arguments when creating tfifd model.
        Args:
            field: a gensim corpus
        Response:
            a list of arguments (kargs)
        """
        return {'smartirs': cls.smartirs}

    @classmethod
    def _tfidf_query_model_kargs(cls, field):
        """ Generator for aguments when creating tfidf models for queries
        Args:
            field: a gensim corpus
        Response:
            a list of arguments (kargs).
        """
        return {'smartirs': cls.query_smartirs}

    @classmethod
    def resolve(cls, indices, query_mat):
        """ Resolve a set of queries for ech field.
        Compute the response of a set of queries for the entire list of indices.
        The output is a vector containing the response for each document in the
        corpus for the specific index in question.
        Args:
            index: a similarity index of the field to query.
            queriies: a sparse csc matrix of the queries.
        Response:
            A sparse vector containing the query result.
        """
        return [ index[queries] for queries, index in zip(query_mat, indices)]

    def _combine_results(self, results_by_fields):
        """ Combine results of fields into a single score
        Args:
            results_by_fields: List of the outputs for each field.
        Response:
            A csc sparse matrix with the pondered summation of the field scores.
        """
        return reduce(np.add, map(lambda M,w: M*w, results_by_fields, self.weights))

    def _normalise(self, scores, query_lengths):
        """ Normalisation of the query result.
        Args:
            scores: sparse matrix with the final results.
            query_lengths: the lengths of the queries
        Response:
            a csc sparse matrix with normalised results
        """
        # do nothing
        return scores

    def resolve_all(self, query_corpus):
        """Resolve a corpus of queries
        Compute the response of a set of queries across the entire corpus, including
        each field on it. The output is a linear combination of the field's responses.
        Args:
            query_corpus: a query corpus
        Response:
            A sparse vector containg the result for each query
        """
        query_lengths = query_corpus.lengths
        query_mat = self._prepare_queries(query_corpus, self.indexes[0].index.dtype)
        results_by_fields = self.resolve(self.indexes, query_mat)
        results = self._combine_results(results_by_fields)
        return QueryResponseSet( self._normalise(results, query_lengths), query_corpus.ids )

class JaccardFIndex(FIndex):
    """Multi-fielded index with Jaccard similarity
    """
    name = 'jaccf'
    smartirs = 'bnn'
    similarity = JaccardSimilarity
    query_smartirs = 'bnn'

class CosineFIndex(FIndex):
    """Multi-fielded index with Cosine similarity
    """
    name = 'cosf'
    smartirs = 'ntc'
    similarity = CosineSimilarity
    query_smartirs = 'ntc'

class BM25FIndex(FIndex):
    """Basic text index class. It creates a index using the corpus provided,
    according to the dictionary. To measure similarity, it uses SimFunction.
    Additional parameters are forwarded to TfidfModel.
    Args:
        corpus: Corpus of the index
        weights: a list of the weights
        bs: a list of the parameter B
        k: parameter k
    """
    name = 'bm25f'
    smartirs = 'nnn'
    similarity = CosineSimilarity
    query_smartirs = 'bnn'
    pivot = 1.0
    def __init__(self, corpus, weights, k):
        self.k = k
        super().__init__(corpus, weights)

    @classmethod
    def _tfidf_model_kargs(cls, field, slope):
        average_length = np.mean([len(doc) for doc in field])
        return { 'wlocal' : gensim.utils.identity,
            'wglobal' : simple_wglobal,
            'normalize' : partial(unique_words_norm, average = average_length),
            'pivot' : cls.pivot,
            'slope' : slope}

    @classmethod
    def _tfidf_query_model_kargs(cls, field):
        """ Generator for aguments when creating tfidf models for queries
        Args:
            field: a gensim corpus
        Response:
            a list of arguments (kargs).
        """
        return {'smartirs': cls.query_smartirs, 'eps': -1}

    def _normalise(self, scores, query_lengths):
        # Compute sigmoid  tf / (k + tf)
        scores.data = np.divide(scores.data, np.full_like(scores.data, self.k) + scores.data)
        # Determine number of document where query terms are occurring (n_q)
        dtf = np.diff(scores.indptr) # hack
        num_docs = scores.shape[0]
        #compute idf
        idf = np.log(np.divide(num_docs - dtf + 0.5, dtf + 0.5))/np.log(2)
        k = 0
        # Expand idf in order to create one for each value in data
        idf2 = np.zeros_like(scores.data)
        for i, j in zip(dtf, idf):
            new_k = k + i
            idf2[k:new_k] = j
            k = new_k
        # do element-wise multiplication
        scores.data = scores.data * idf2
        # In order to do the summation, we need just to modify the indptr such that
        # it relfects the actual number of queries. Then, we can just call sum_duplicates
        # to merge the scores across the terms.
        # Compute size of new indptr
        indptr = np.zeros(query_lengths.size + 1, dtype = np.int32)
        k = 0
        # For each actual query
        for i in range(query_lengths.size):
            new_k = k + query_lengths[i]
            indptr[i+1] = scores.indptr[new_k]
            k = new_k
        # We now create the resulting matrix with the new shape and assign
        # the values of the prievous one
        new_scores = sp.sparse.csc_matrix((scores.data, scores.indices, indptr),
                shape=(scores.shape[0], query_lengths.size))
        # and remove duplicates
        new_scores.sum_duplicates()
        return new_scores
