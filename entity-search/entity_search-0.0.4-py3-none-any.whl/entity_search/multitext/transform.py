import gensim
from itertools import zip_longest
from ..interfaces import TfidfModel, MmSave
from .corpus import *

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

# Functions for handling gensim calls

def tfidf_model(field, **kargs):
    """ Create tfidf_model using gensim. Kargs are sent to
    gensim constructor.
    Args:
        field: input corpus
    Response:
        a gensim Tfidf model
    """
    return TfidfModel(field, **kargs)

class TransformedField(gensim.interfaces.TransformedCorpus, MmSave):
    """ Transform a field according to a model using a given training corpus
    """
    def __init__(self, field, training_field, tfidf_model_kargs, name = None):
        """
        Args:
            field: the field to transform
            training_field: the field (gensim corpus) used to training the transformation
            tfidf_model_kargs: function to create kargs elements send to the transformation.
            name: name of the field (it overrides the name of the original field).
        """
        # Create kargs and then create tfidf model
        kargs = tfidf_model_kargs(training_field)
        model = tfidf_model(training_field, **kargs)
        # override name if necessary
        self.name = name if name else field.name
        # copy attributes from original field to new transformed field
        if hasattr(field, "dictionary"):
            self.dictionary = field.dictionary
        self.num_terms = field.num_terms
        self.num_docs = field.num_docs
        self.num_nnz = field.num_nnz
        super().__init__(model, field)

class TransformedCorpus(MultiFieldCorpusABC):
    """ Transform a multi corpus using TFIDF interface
    """
    def __init__(self, corpus, training_corpus, tfidf_model_kargs):
        """
        Args:
            corpus: a multi field corpus
            training_corpus: a corpus used for training each field
            tfidf_model_kargs: functions to create kargs submitted to the creation of each
                transformed field.
        """
        # if corpus is not a multi-field, do nothing
        if not isinstance(corpus, MultiFieldCorpusABC):
            raise RuntimeError(''
                + 'corpus {} is not an instance of MultiFieldCorpusABC'.format(type(corpus)))
        # Manually copy some attributes
        if isinstance(corpus, QueryCorpus):
            self.ids = corpus.ids
            self.lengths = corpus.lengths
        # Check weather the number of fields is the same, or the original corpus has only
        # one field
        num_fields = len(corpus.fields)
        num_training_fields = len(training_corpus.fields)
        if num_fields != num_training_fields and num_fields != 1:
            raise RuntimeError(''
                + 'Number of field in corpus ({}) is not equal to the '.format(num_fields)
                + 'number of training fields ({})'.format(num_training_fields))
        if num_fields == 1:
            # We perform a 1-to-many training. This means we take the single field in the
            # original corpus and we transformed into several fields using the fields
            # given in the training corpus. The resulting corpus will have the same
            # number of field than the training corpus. However, each of them is a
            # transformation of the singleton field in the original corpus with respect to
            # individual fields in the training corpus.
            field = corpus.fields[0]
            # We need to change the name, otherwise we could produce mm files with same names
            names = [ "{}.{}".format(field.name, i) for i in range(num_training_fields)]
            self.fields = [
                TransformedField(field, training_field, tfidf_model_karg, name = name)
                for training_field, tfidf_model_karg, name in
                zip(training_corpus.fields, tfidf_model_kargs, names)]
        else:
            # 1-to-1 training. Here, we just pair each field in the original corpus with
            # a field in the training corpus. The resulting transformed corpus has the same
            # number of fields as the original corpus ( which is the same than the training
            # corpus)
            self.fields = [
                TransformedField(field, training_field, tfidf_model_karg)
                for field, training_field, tfidf_model_karg in
                zip(corpus.fields, training_corpus.fields, tfidf_model_kargs) ]
        # keep a reference of the dictionary
        self.dictionary = corpus.dictionary
