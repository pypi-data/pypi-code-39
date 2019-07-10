import json
import gensim
import gensim.test.utils
import pickle
import nltk
import numpy as np
import scipy as sp
from functools import reduce
from ..math import empty_sparse_vector, sparse_column_vector
from ..interfaces import FieldABC, InstantFieldABC
from ..string import join_str

class JsonFieldABC(FieldABC):
    """Base class for json-based field
    It defines a get_texts function that parse the input as a json
    object. To extract the data, the function _extractor must need
    defined.
    """
    def _extractor(self, doc):
        """ Extract a document from the dictionary doc
        Args:
            doc: a dictionary containing a document.
        Response:
            A list with the one or more strings
        """
        raise NotImplementedError

    def get_texts(self):
        """
        Return all documents as a generator
        """
        for doc in self.getstream():
            s_doc = json.loads(gensim.utils.to_unicode(doc))
            field_str = self._extractor(s_doc)
            text = join_str(field_str)
            yield self.preprocess_text(text)

class JsonGlobalField(JsonFieldABC):
    """It creates a sigle-field document for each document in
    the corpus, combining all the fields.
    Args:
        path: Path of the corpus
    """
    def __init__(self, path, *args, **kargs):
        super().__init__(path, "global", *args, **kargs)

    def _extractor(self, doc):
        r = [value for value in doc.values() if type(value) == str]
        return r

class JsonSingleField(JsonFieldABC):
    """It creates a single-field document for each document in
    a json corpus, such that only a given field of is used
    Args:
        path: Path of the corpus
        name: Name of the field to include
    """
    def __init__(self, path, name, *args, **kargs):
        super().__init__(path, name, *args, **kargs)

    def _extractor(self, doc):
        return [ doc[self.name] ]

class MmSingleField(gensim.corpora.MmCorpus):
    """It creates a single-field document for each document in
    a Mm format corpus.
    """
    def __init__(self, path, name, dictionary, *args, **kargs):
        self.name = name
        self.dictionary = dictionary
        super().__init__(path, *args, **kargs)

class MultiFieldCorpusABC(object):
    """Base class for multi-field objects.
    It requires a dictionary, and a list of fields.
    Args:
        dictionary: a corpus dictionary
        fields: list of corpus for each field.
    """
    mm_file_suffix = 'mm'
    dict_file_suffix = 'dict'
    field_file_suffix = 'fields.pkl'
    ids_file_suffix = 'state.pkl'
    def __init__(self, dictionary, fields):
        self.dictionary = dictionary
        self.fields = fields

    def save_as_mm(self, base_path):
        """ Save each field in this corpus as mm.
        It create 3 types of files:
            pickle_file: it contains the name of the fields.
            dict_file: it contains the dictionary (store in gensim format)
            field_files: it contains a field in mm format (one for each field)
        This files are returned in a list, following the same order
        as mentioned above.
        Args:
            base_path: a common name for each file. Extension will be added
                to distinguish them.
        Response:
            A list of string, containing the names of the created files.
        """
        files = []
        # store the name of the fields
        pickle_file = "{}.{}".format(base_path, self.field_file_suffix)
        field_names = [ field.name for field in self.fields ]
        with open(pickle_file, 'wb') as f:
            pickle.dump(field_names, f)
        files.append(pickle_file)
        # Store the dictionar
        dict_file = "{}.{}".format(base_path, self.dict_file_suffix)
        self.dictionary.save_as_text(dict_file)
        files.append(dict_file)
        # store the fields
        field_files = []
        for field in self.fields:
            output_file = "{}.{}.{}".format(base_path, field.name, self.mm_file_suffix)
            field.save_as_mm(output_file)
            field_files.append(output_file)
        files = files + field_files
        # for QueryCorpus only
        if hasattr(self, "ids") and hasattr(self, "lengths"):
            # Store ids
            state_file = "{}.{}".format(base_path, self.ids_file_suffix)
            with open(state_file, 'wb') as f:
                pickle.dump((self.ids, self.lengths), f)
            files.append(state_file)
        return files

    @classmethod
    def load_mm(self, base_path):
        """ Load a previously stored mm files.
        It requires the existance of 3 type of files:
            pickle_file: it contains the name of the fields.
            dict_file: it contains the dictionary (store in gensim format)
            field_files: it contains a field in mm format (one for each field)
        Args:
            base_path: the common name for each file. They are distinguished using
                specific extensions.
        Response:
            A MmMultiFieldCorpus object
        """
        dictionary_file = "{}.{}".format(base_path, self.dict_file_suffix)
        with open("{}.{}".format(base_path, self.field_file_suffix), 'rb') as f:
            field_names = pickle.load(f)
        field_files = [ "{}.{}.{}".format(base_path, field, self.mm_file_suffix)
                for field in field_names]
        return MmMultiFieldCorpus(field_files, field_names, dictionary_file)

class JsonMultiFieldCorpus(MultiFieldCorpusABC):
    """It defines a multi-field corpus where each field corresponds
    to a SingleFieldJsonCorpus. Each of this field is created from
    the list of fields defined and a common dictionary. If no
    dictionary is provided, a new one is created.
    Args:
        text_file: Path of the corpus.
        field_names: Name of the fields.
        dictionary: Dictionary of the corpus
    """
    def __init__(self, text_file, field_names, dictionary = None):
        # If no dictionary is provided, generate it
        if dictionary is None:
            dictionary = JsonGlobalField(text_file).dictionary
        # Use this dictionary for indexing each field
        super().__init__(dictionary,
                [JsonSingleField(text_file, field_name, dictionary)
                    for field_name in field_names])

class MmMultiFieldCorpus(MultiFieldCorpusABC):
    """It defines a multi-field corpus where each field corresponds
    to a SingleFieldMmCorpus. Each of the filed is created from a list
    of files in Matrix Market format and a common dictionary. If no
    dictionary is provided, a new one is created.
    Args:
        field_files: List of the paths for each field in Matrix Market format.
        field_names: List of the name of the fields.
        dictionary_file: The file of the dictionary.
    """
    def __init__(self, field_files, field_names, dictionary_file):
        dictionary = gensim.corpora.Dictionary.load_from_text(dictionary_file)
        super().__init__(dictionary,
                [MmSingleField(field_file, field_name, dictionary)
                    for field_file, field_name in zip(field_files, field_names)])

class QueryField(FieldABC):
    """This class handles the query field of a query corpus
    Args:
        path: Path of the corpus
        dictionary_path: Path of the dictionary
    """
    def __init__(self, path, *args, **kargs):
        super().__init__(path, "query", *args, **kargs)

    def get_texts(self):
        """
        Return all queries as a generator
        """
        for doc in self.getstream():
            _, text = doc.decode('utf-8').split("\t")
            text = gensim.utils.to_unicode(text)
            yield self.preprocess_text(text)

    def get_ids(self):
        for doc in self.getstream():
            _id, _ = doc.decode('utf-8').split("\t")
            yield _id

class InstantQueryField(InstantFieldABC):
    """ This class handle the query field for a query corpus
    created as it is read remotely
    Args:
        documents: String containing the documents. One for each line.
        dictionary_path: Path of the dictionary
    """
    def __init__(self, documents, *args, **kargs):
        super().__init__(documents, "inst-query", *args, **kargs)

    def get_texts(self):
        """
        Return all queries as a generator
        """
        for doc in self.getstream():
            doc = json.loads(doc)
            yield self.preprocess_text(doc['keywords'])

    def get_ids(self):
        """
        Return all ids as a generator
        """
        for doc in self.getstream():
            doc = json.loads(doc)
            yield doc['id']

class QueryCorpus(MultiFieldCorpusABC):
    """ It merges QueryField and QueryIdField into a single
    corpus.
    """
    def __init__(self, text_file, dictionary):
        # Dictionary must be provided
        queries = QueryField(text_file, dictionary = dictionary)
        self.ids = list(queries.get_ids())
        self.lengths = np.array([len(q) for q in queries])
        super().__init__(dictionary, [queries])

    @classmethod
    def load_mm(cls, base_path):
        # Load ids
        pickle_file = "{}.{}".format(base_path, cls.ids_file_suffix)
        with open(pickle_file, 'rb') as f:
            ids, lengths = pickle.load(f)
        mmcorpus = MultiFieldCorpusABC.load_mm(base_path)
        mmcorpus.ids = ids
        mmcorpus.lengths = lengths
        return mmcorpus

class InstantQueryCorpus(MultiFieldCorpusABC):
    def __init__(self, json_queries, dictionary):
        # Dictionary must be provided
        queries = InstantQueryField(json_queries, dictionary = dictionary)
        self.ids = list(queries.get_ids())
        self.lengths = np.array([len(q) for q in queries])
        super().__init__(dictionary, [queries])
