import nltk
import krovetz

def porter_stemmer(tokens):
    """ Stem words using porter algorithm
    Args:
        tokens: list of tokens
    Response:
        A list of stemmed tokens
    """
    ps = nltk.stem.PorterStemmer()
    return [ps.stem(token) for token in tokens ]

# We create one instance of this class as it is very slow to load it
ks = krovetz.PyKrovetzStemmer()

def krovetz_stemmer(tokens):
    """ Stem words using Krovetz algorithm
    Args:
        tokens: list of tokens
    Response:
        A list of stemmed tokens
    """
    return [ks.stem(token) for token in tokens ]

def no_stemmer(tokens):
    """ Dummy funcion for stemming
    Args:
        tokens: list of tokens
    Response:
        Same as the input list
    """
    return tokens

def join_str(c):
    """ Fast function for concatenating strings.
    By default, it uses a single white space as seperator.
    Args:
        c: list of strings
    Response:
        A concatenation of the strings in c
    """
    return " ".join(c)

import json
import gensim
import gensim.test.utils
import nltk
import numpy as np
import scipy as sp
from functools import reduce
from .math import empty_sparse_vector, sparse_column_vector

class BaseCorpus(gensim.corpora.TextCorpus):
    """Base class for defining a corpus. It defines the default preprecessing
    pipeline.
    Args:
        path: the path were is located the documents
    """
    def __init__(self, path, *args, **kargs):
        # We can set any tokenizer from NLTK.
        # However, we resort to gensim tokenizer as it is faster than most
        # nltk ones.
        #tokenizer = tokenize.WhitespaceTokenizer().tokenize
        tokenizer = gensim.utils.simple_tokenize
        # Character_filters:
        # None
        character_filters = [gensim.corpora.textcorpus.lower_to_unicode]
        # token filters:
        # remove stopwords
        token_filters = [gensim.corpora.textcorpus.remove_stopwords,
                         krovetz_stemmer
                        ]
        super().__init__(path, *args, tokenizer = tokenizer,
                         character_filters = character_filters,
                         token_filters = token_filters, **kargs)
        self.num_terms = self.dictionary.num_pos
        self.num_docs = self.dictionary.num_docs

    def to_vec(self, doc):
        """
        Using the corpus, create a vectorial representation of a document. If
        a word have not been seen before, this creation will fail.
        Args:
            doc: A string document.
        Response:
            A list of pairs, where the first element is the id of the word and
            the second is the frequency of the word in the document.
        """
        vec = self.dictionary.doc2bow(self.preprocess_text(doc))
        return vec

class GlobalCorpus(BaseCorpus):
    """This class handles a json-based document corpus
    Args:
        path: Path of the corpus
    """
    def __init__(self, path, field_names, *args, **kargs):
        self.field_names = field_names
        super().__init__(path, *args, **kargs)

    def get_texts(self):
        """
        Return all documents as a generator
        """
        for doc in self.getstream():
            s_doc = json.loads(gensim.utils.to_unicode(doc))
            # Merge all the fileds into a single document
            field_str = [ s_doc[field] for field in self.field_names ]
            text = join_str(field_str)
            yield self.preprocess_text(text)

class FieldCorpus(BaseCorpus):
    """It handles a particular field of a json-based document corpus
    Args:
        path: Path of the corpus
        field: Name of the field to include
        dictionary: Provide a dictionary for the corpus
    """
    def __init__(self, path, field, dictionary):
        self.field = field
        super().__init__(path, dictionary = dictionary)

    def get_texts(self):
        """
        Return all documents as a generator
        """
        for doc in self.getstream():
            s_doc = json.loads(gensim.utils.to_unicode(doc))
            yield self.preprocess_text(s_doc[self.field])

class MultiFieldCorpus(object):
    """Base class for multi-field objects. It requires a dictionary,
    a list of field corpuses, and a list of field names.
    Args:
        dictionary: the dictionary of the corpus.
        fields: list of the corpuses for each field.
        field_names: list of the names of the fields.
    """
    def __init__(self, dictionary, fields, field_names):
        self.dictionary = dictionary
        self.fields = fields
        self.field_names = field_names

    def get_docs(self, ids):
        """
        Return certain documents as a generator
        Args:
            ids: ids to retrieve
        """
        i = 0
        for doc in self.fields[0].getstream():
            if i in ids:
                yield json.loads(gensim.utils.to_unicode(doc))
            i += 1

class PlainMultiFieldCorpus(MultiFieldCorpus):
    """It implement MultiFieldCorpus using a plain format for the
    corpuses for the corpus defined in text_file
    Args:
        text_file: Path of the corpus.
        field_names: Name of the fields.
    """
    def __init__(self, text_file, field_names):
        # Read the documents entierly (no field distinction) and get the
        # dictionary
        text_file = gensim.test.utils.datapath(text_file)
        dictionary = GlobalCorpus(text_file, field_names).dictionary
        # Use this dictionary for indexing each field
        fields = [ FieldCorpus(text_file, field_name, dictionary)
                       for field_name in field_names]
        super().__init__(dictionary, fields, field_names)

class MmMultiFieldCorpus(MultiFieldCorpus):
    """Implements MultiFieldCorpus using Matrix Market format. The
    corpuses and dictionary must be already created.
    Args:
        dictionary_path: Path to the dictionary in dict format.
        corpus_files: List of the paths for each field in Matrix Market format.
        field_names: List of the name of the fields.
    """
    def __init__(self, dictionary_path, corpus_files, field_names):
        super().__init__(gensim.corpora.Dictionary.load_from_text(dictionary_path),
                [gensim.corpora.MmCorpus(corpus_file) for corpus_file in corpus_files],
                field_names)

class Similarity(gensim.similarities.SparseMatrixSimilarity):
    """ Generic similarity class. No normalisation is performed.
    """
    def __init__(self, corpus, num_features=None, num_terms=None,
                 num_docs=None, num_nnz=None, num_best=None, chunksize=500,
                 dtype=np.float32, maintain_sparsity=False):
        self.num_best = num_best
        self.normalize = False
        self.chunksize = chunksize
        self.maintain_sparsity = maintain_sparsity

        if corpus is not None:
            # iterate over input corpus, populating the sparse index matrix
            try:
                # use the more efficient corpus generation version, if the
                # input `corpus` is MmCorpus-like (knows its shape and number
                # of non-zeroes).
                num_terms, num_docs, num_nnz = corpus.num_terms, corpus.num_docs, corpus.num_nnz
                #logger.debug("using efficient sparse index creation")
            except AttributeError:
                # no MmCorpus, use the slower version (or maybe user supplied the
                # num_* params in constructor)
                pass
            if num_features is not None:
                # num_terms is just an alias for num_features, for
                # compatibility with MatrixSimilarity
                num_terms = num_features
            if num_terms is None:
                raise ValueError("refusing to guess the number of sparse features: specify num_features explicitly")

            # We dont normalise the vector when creating the index
            corpus = (gensim.matutils.scipy2sparse(v) if sp.sparse.issparse(v) else
                      (gensim.matutils.full2sparse(v) if isinstance(v, np.ndarray) else
                       v) for v in corpus)
            self.index = gensim.matutils.corpus2csc(
                corpus, num_terms=num_terms, num_docs=num_docs, num_nnz=num_nnz,
                dtype=dtype, printprogress=10000
            ).T

    def __len__(self):
        """Get size of index."""
        return self.index.shape[0]

class JaccardSimilarity(Similarity):
    """ Compute Jaccard similarity
    """
    def get_similarities(self, query):
        """ Given a query compute the jacard similarity. We use the dot
        product to first identify non-zero elements in the adjacency matrix.
        Later we iterate non-zero values and compute jaccard for them.
        Args:
            query: A query
        Response:
            A numpy array containing the similarities
        """
        query, query_length = query

        # compute dot product against every other document in the collection
        dot_index_query = self.index * query.tocsc()  # N x T * T x C = N x C

        # get summation of elements and compute difference between summ
        # and dot_index_query
        try:
            diff = self.summ - np.asarray(dot_index_query.todense())
        except AttributeError:
            self.summ = np.asarray(self.index.sum(axis = 1), dtype = 'f').reshape(dot_index_query.shape)
            diff = self.summ - np.asarray(dot_index_query.todense())

        # add query normalisation (query length)
        diff = np.add(diff, query_length)

        # Compute score and return
        s = np.divide(1, diff, where=diff!=0)
        return dot_index_query.multiply(s)

class CosineSimilarity(Similarity):
    """ Compute Jaccard similarity
    """
    def get_similarities(self, query):
        """ Given a query compute binary similarity. We use the dot
        product and then the result is ceiled to 1
        Args:
            query: A query
        Response:
            A numpy array containing the similarities
        """
        query, _ = query
        result = self.index * query.tocsc()  # N x T * T x C = N x C
        return result

class BM25Similarity(Similarity):
    def __init__(self, corpus, b_parameter, num_features=None, num_terms=None,
            num_docs=None, num_nnz=None, num_best=None, chunksize=500,
            dtype=np.float32, maintain_sparsity=False):
        super().__init__(corpus, num_features, num_terms, num_docs, num_nnz,
                        num_best, chunksize, dtype, maintain_sparsity)
        # Compute idf
        self.idf = self.index.sum(axis = 0)

        # Compute normalisation factors
        lengths = np.array([len(v) for v in corpus])
        # Avoid zero division
        lengths_mean = np.mean(lengths)
        if lengths_mean != 0:
            B = 1 - b_parameter + b_parameter * lengths/lengths_mean
        else:
            B = b_parameter + lengths
        B = np.divide(1.0, B, out=np.zeros_like(B), where=B!=0)
        B = sp.sparse.diags(B)

        # Now we do BM25 normalisation
        self.index = B * self.index

    def get_similarities(self, query):
        return self.index * query

class FIndex(object):
    """Base index for multi-fielded corpus. It creates a vector space and
    index for each field in the corpus.
    Args:
        corpus: a multi-field corpus
        weights: the importance of each field in the corpus. It must add to 1.
        similarity: the similarity function to use for indexing.
        args: commands send to similarity constructor
    """
    def __init__(self, corpus, weights, similarity, *args):
        self.corpus = corpus
        sum_weights = np.sum(weights)
        if not np.isclose(sum_weights, 1.0):
            raise RuntimeError('Weights must add to 1, found {}'.format(sum_weights))
        # We store weights vector as sparse to simplify multiplication later on
        data = np.array(weights)
        length = len(weights)
        ix = np.arange(length)
        iy = np.zeros(length)
        self.weights = sp.sparse.coo_matrix((data, (ix, iy)),
                                            shape=(length, 1)).tocsc()

        # Keep corpuses that at least have one non-null element.
        # Set to None otherwise
        self.indexes = [ similarity(field, *arg,
                                   num_terms = field.num_terms,
                                   num_docs = field.num_docs,
                                   num_nnz = field.num_nnz,
                                   maintain_sparsity = True)
                        if field.num_nnz > 0 else None
                        for field, *arg in zip(corpus.fields, *args)]

    def prepare_query (self, keywords):
        """ Transform query into a vector.
        Notice that we have a unique vector for the entire set of fields. This
        is possible since all index matrices have the same shape.
        Args:
            keywords: free-text query (str)
        Response:
            A tuple containing the a sparse vector of the query and the number
            of none zero values.
        """
        q = self.corpus.dictionary.doc2bow(keywords)
        query_length = len(q)
        query = gensim.matutils.corpus2csc([q], self.indexes[0].index.shape[1],
                                    dtype=self.indexes[0].index.dtype)
        # We sent the vector and its length
        return (query, query_length)

    def query(self, keywords):
        """ Given a free-text query, compute the response
        Args:
            keywords: free-text query (str).
        Response:
            A sparse vector containing the query result.
        """
        size = len(self.indexes[0])
        # Create vector query. The vector is the same for each field.
        query = self.prepare_query(keywords)
        # Combine field score into a single sparse matrix
        score = sp.sparse.hstack([index[query] if index else empty_sparse_vector(size)
                          for index in self.indexes]).tocsc()
        return score * self.weights

class JaccardFIndex(FIndex):
    """Multi-fielded index with Jaccard similarity
    Args:
        corpus: a multi-field corpus
        weights: the importance of each field in the corpus. It must add to 1.
    """
    name = 'jaccf'
    def __init__(self, corpus, weights):
        super().__init__(corpus, weights, JaccardSimilarity)

class CosineFIndex(FIndex):
    """Multi-fielded index with Cosine similarity
    Args:
        corpus: a multi-field corpus
        weights: the importance of each field in the corpus. It must add to 1.
    """
    name = 'cosf'
    def __init__(self, corpus, weights):
        super().__init__(corpus, weights, CosineSimilarity)

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
    def __init__(self, corpus, weights, bs, k):
        self.k = k
        super().__init__(corpus, weights, BM25Similarity, bs)
        self.weights = np.asarray(self.weights.todense()).reshape(-1)

    def query(self, keywords):
        """ Query the index using keywords
        Args:
            Keywords: a query in text plain format.
        Response:
            A dense vector containing the result of the query.
        """
        size = self.indexes[0].index.shape[1]
        # Create diagonal matrix with query
        q = np.array(self.corpus.dictionary.doc2bow(keywords), dtype = 'u4,f')
        q = sp.sparse.coo_matrix((q['f1'], (q['f0'], q['f0'])), shape = (size, size))

        # Compute tf for each field and then combine scores per term
        tfs = np.array([index[q] for index in self.indexes if index])
        tfs = reduce(np.add, [tf*v_s for tf, v_s in zip(tfs, self.weights)])

        # Compute sigmoid  tf / (k + tf)
        tfs_k = tfs.copy()
        tfs_k.data = np.divide(1, np.ones_like(tfs_k.data)*self.k + tfs_k.data)
        tfs = tfs.multiply(tfs_k)

        # Compute idf for each term in query
        try:
            self.idfs
        except AttributeError:
            # Compute idf   log( N - n + 0.5 / (n + 0.5) )
            idf = np.asarray(reduce(np.add,
                [index.idf for index in self.indexes if index])).reshape(-1)
            idf_top = (idf.size + 0.5) - idf
            idf_bottom = idf + 0.5
            self.idfs = sparse_column_vector(
                np.log(np.divide(idf_top, idf_bottom))).tocsc()
        finally:
            bm25f = tfs * self.idfs

        return bm25f
