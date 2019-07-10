import gensim
import gensim.utils as utils
import numpy as np
import scipy as sp
import colorlog
from .string import krovetz_stemmer, porter_stemmer, no_stemmer, join_str

logger = colorlog.getLogger(__name__)

class Similarity(gensim.similarities.SparseMatrixSimilarity):
    """ Generic similarity class. No normalisation is performed. We reimplement SparseMatrixSimilarity
    in order to build the object properly when needed and to reduce the overhead of 'getitem' method.
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
            try:
                # Check if num_terms and num_docs are available. This attributes
                # are set when reading a json-based corpus.
                num_terms, num_docs = corpus.num_terms, corpus.num_docs
            except AttributeError:
                # not available, try manual parameters
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
            ).T.tocsc()

    def __getitem__(self, query):
        """Get similarities of the given document or corpus against this index.
        Uses :meth:`~gensim.interfaces.SimilarityABC.get_similarities` internally.
        Notes
        -----
        Passing an entire corpus as `query` can be more efficient than passing its documents one after another,
        because it will issue queries in batches internally.
        Parameters
        ----------
        query : {list of (int, number), iterable of list of (int, number)}
            Document in the sparse Gensim bag-of-words format, or a streamed corpus of such documents.
        Returns
        -------
        {`scipy.sparse.csr.csr_matrix`, list of (int, float)}
            Similarities given document or corpus and objects corpus, depends on `query`.
        """
        if self.normalize:
            # self.normalize only works if the input is a plain gensim vector/corpus (as
            # advertised in the doc). in fact, input can be a numpy or scipy.sparse matrix
            # as well, but in that case assume tricks are happening and don't normalize
            # anything (self.normalize has no effect).
            if not gensim.matutils.ismatrix(query):
                is_corpus, query = gensim.utils.is_corpus(query)
                if is_corpus:
                    query = [gensim.matutils.unitvec(v) for v in query]
                else:
                    query = gensim.matutils.unitvec(query)
        result = self.get_similarities(query)

        if self.num_best is None:
            return result

        # if maintain_sparsity is True, result is scipy sparse. Sort, clip the
        # topn and return as a scipy sparse matrix.
        if getattr(self, 'maintain_sparsity', False):
            return gensim.matutils.scipy2scipy_clipped(result, self.num_best)

        # if the input query was a corpus (=more documents), compute the top-n
        # most similar for each document in turn
        if gensim.matutils.ismatrix(result):
            return [gensim.matutils.full2sparse_clipped(v, self.num_best) for v in result]
        else:
            # otherwise, return top-n of the single input document
            return gensim.matutils.full2sparse_clipped(result, self.num_best)

class TfidfModel(gensim.models.TfidfModel):
    """ This is the same clase with a minor change when performing
    transformation. Gensim does not include zero values when a token
    has not been seen before. Including those zeros can help to
    create query documents that are consistents across several indices,
    reducing the overhead when integreating severa query results into
    a single one.
    """

    def __init__(self, corpus=None, eps=1e-12, **kargs):
        super().__init__(corpus, **kargs)
        self.eps = eps

    def __getitem__(self, bow):
        """Get the tf-idf representation of an input vector and/or corpus.
        bow : {list of (int, int), iterable of iterable of (int, int)}
            Input document in the `sparse Gensim bag-of-words format
            <https://radimrehurek.com/gensim/intro.html#core-concepts>`_,
            or a streamed corpus of such documents.
        eps : float
            Threshold value, will remove all position that have tfidf-value less than `eps`.
        Returns
        -------
        vector : list of (int, float)
            TfIdf vector, if `bow` is a single document
        :class:`~gensim.interfaces.TransformedCorpus`
            TfIdf corpus, if `bow` is a corpus.
        """
        # if the input vector is in fact a corpus, return a transformed corpus as a result
        is_corpus, bow = utils.is_corpus(bow)
        if is_corpus:
            return self._apply(bow)

        # unknown (new) terms will be given zero weight (NOT infinity/huge weight,
        # as strict application of the IDF formula would dictate)

        termid_array, tf_array = [], []
        for termid, tf in bow:
            termid_array.append(termid)
            tf_array.append(tf)

        tf_array = self.wlocal(np.array(tf_array))

        vector = [
            (termid, tf * self.idfs.get(termid, 0.0)) # ptorres: put zero if values is not found
            for termid, tf in zip(termid_array, tf_array) if abs(self.idfs.get(termid, 0.0)) > self.eps
        ]

        if self.normalize is True:
            self.normalize = matutils.unitvec
        elif self.normalize is False:
            self.normalize = utils.identity

        # and finally, normalize the vector either to unit length, or use a
        # user-defined normalization function
        if self.pivot is None:
            norm_vector = self.normalize(vector)
            norm_vector = [(termid, weight) for termid, weight in norm_vector if abs(weight) > self.eps]
        else:
            _, old_norm = self.normalize(vector, return_norm=True)
            pivoted_norm = (1 - self.slope) * self.pivot + self.slope * old_norm
            norm_vector = [
                (termid, weight / float(pivoted_norm))
                for termid, weight in vector
                if abs(weight / float(pivoted_norm)) > self.eps
            ]
        return norm_vector

class MmWriter(gensim.matutils.MmWriter):
    """ Gensim MmWriter does not write values close to zero in the
    output file. While this is understandable, we aregue that should
    be the user the one that decide which value remove from the corpus
    before storing as Mm file. Thus, this class store the corpus as
    it is, without checking values.
    """
    def write_vector(self, docno, vector):
        """Write a single sparse vector to the file.
        Parameters
        ----------
        docno : int
            Number of document.
        vector : list of (int, number)
            Document in BoW format.
        Returns
        -------
        (int, int)
            Max word index in vector and len of vector. If vector is empty, return (-1, 0).
        """
        assert self.headers_written, "must write Matrix Market file headers before writing data!"
        assert self.last_docno < docno, "documents %i and %i not in sequential order!" % (self.last_docno, docno)
        vector = sorted((i, w) for i, w in vector)
        for termid, weight in vector:  # write term ids in sorted order
            # +1 because MM format starts counting from 1
            self.fout.write(utils.to_utf8("%i %i %s\n" % (docno + 1, termid + 1, weight)))
        self.last_docno = docno
        return (vector[-1][0], len(vector)) if vector else (-1, 0)

    @staticmethod
    def write_corpus(fname, corpus, progress_cnt=1000, index=False, num_terms=None, metadata=False):
        """Save the corpus to disk in `Matrix Market format <https://math.nist.gov/MatrixMarket/formats.html>`_.
        Parameters
        ----------
        fname : str
            Filename of the resulting file.
        corpus : iterable of list of (int, number)
            Corpus in streamed bag-of-words format.
        progress_cnt : int, optional
            Print progress for every `progress_cnt` number of documents.
        index : bool, optional
            Return offsets?
        num_terms : int, optional
            Number of terms in the corpus. If provided, the `corpus.num_terms` attribute (if any) will be ignored.
        metadata : bool, optional
            Generate a metadata file?
        Returns
        -------
        offsets : {list of int, None}
            List of offsets (if index=True) or nothing.
        Notes
        -----
        Documents are processed one at a time, so the whole corpus is allowed to be larger than the available RAM.
        See Also
        --------
        :func:`gensim.corpora.mmcorpus.MmCorpus.save_corpus`
            Save corpus to disk.
        """
        mw = MmWriter(fname) # ptorrestr: we use oure MmWriter

        # write empty headers to the file (with enough space to be overwritten later)
        mw.write_headers(-1, -1, -1)  # will print 50 spaces followed by newline on the stats line

        # calculate necessary header info (nnz elements, num terms, num docs) while writing out vectors
        _num_terms, num_nnz = 0, 0
        docno, poslast = -1, -1
        offsets = []
        if hasattr(corpus, 'metadata'):
            orig_metadata = corpus.metadata
            corpus.metadata = metadata
            if metadata:
                docno2metadata = {}
        else:
            metadata = False
        for docno, doc in enumerate(corpus):
            if metadata:
                bow, data = doc
                docno2metadata[docno] = data
            else:
                bow = doc
            if docno % progress_cnt == 0:
                logger.info("PROGRESS: saving document #%i", docno)
            if index:
                posnow = mw.fout.tell()
                if posnow == poslast:
                    offsets[-1] = -1
                offsets.append(posnow)
                poslast = posnow
            max_id, veclen = mw.write_vector(docno, bow)
            _num_terms = max(_num_terms, 1 + max_id)
            num_nnz += veclen
        if metadata:
            gensim.utils.pickle(docno2metadata, fname + '.metadata.cpickle')
            corpus.metadata = orig_metadata

        num_docs = docno + 1
        num_terms = num_terms or _num_terms

        if num_docs * num_terms != 0:
            logger.info(
                "saved %ix%i matrix, density=%.3f%% (%i/%i)",
                num_docs, num_terms, 100.0 * num_nnz / (num_docs * num_terms), num_nnz, num_docs * num_terms
            )

        # now write proper headers, by seeking and overwriting the spaces written earlier
        mw.fake_headers(num_docs, num_terms, num_nnz)

        mw.close()
        if index:
            return offsets

class MmCorpus(gensim.corpora.mmcorpus.MmCorpus):
    """ We redefine MmCorpus in order to use our own MmReader
    """
    @staticmethod
    def save_corpus(fname, corpus, id2word=None, progress_cnt=1000, metadata=False):
        """Save a corpus to disk in the sparse coordinate Matrix Market format.
        Parameters
        ----------
        fname : str
            Path to file.
        corpus : iterable of list of (int, number)
            Corpus in Bow format.
        id2word : dict of (int, str), optional
            Mapping between word_id -> word. Used to retrieve the total vocabulary size if provided.
            Otherwise, the total vocabulary size is estimated based on the highest feature id encountered in `corpus`.
        progress_cnt : int, optional
            How often to report (log) progress.
        metadata : bool, optional
            Writes out additional metadata?
        Warnings
        --------
        This function is automatically called by :class:`~gensim.corpora.mmcorpus.MmCorpus.serialize`, don't
        call it directly, call :class:`~gensim.corpora.mmcorpus.MmCorpus.serialize` instead.
        Example
        -------
        .. sourcecode:: pycon
            >>> from gensim.corpora.mmcorpus import MmCorpus
            >>> from gensim.test.utils import datapath
            >>>
            >>> corpus = MmCorpus(datapath('test_mmcorpus_with_index.mm'))
            >>>
            >>> MmCorpus.save_corpus("random", corpus)  # Do not do it, use `serialize` instead.
            [97, 121, 169, 201, 225, 249, 258, 276, 303]
        """
        logger.info("storing corpus in Matrix Market format to %s", fname)
        num_terms = len(id2word) if id2word is not None else None
        return MmWriter.write_corpus(
            fname, corpus, num_terms=num_terms, index=True, progress_cnt=progress_cnt, metadata=metadata
        )

class MmSave(object):
    """ A class that use MmCorpus to save a gensim corpus
    """
    def save_as_mm(self, output_file_path):
        """ Save field/corpus as mm corpus
        Args:
            output_file_path: a file path where to store the mm corpus.
        """
        MmCorpus.serialize(output_file_path, self,
                id2word = self.dictionary)

class FieldABC(gensim.corpora.TextCorpus, MmSave):
    """Base class for any corpus.
    It defines the default preprecessing pipeline for a text corpus.
    Args:
        path: the path where documents are located.
    """
    def __init__(self, path, name, *args, **kargs):
        self.name = name
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
        self.num_terms = len(self.dictionary)
        self.num_docs = self.dictionary.num_docs
        self.num_nnz = None

class InstantFieldABC(FieldABC):
    """ This corpus takes the input parameter as documents, where each line corresponds a
    single document.
    """
    def getstream(self):
        """Generate documents from the underlying input text (each line is a separate document).
        Yields
        ------
        str
            Document read from plain-text file.
        Notes
        -----
        After generator end - initialize self.length attribute.
        """
        num_texts = 0
        for line in self.input.splitlines():
            yield line
        num_texts += 1
        self.length = num_texts
