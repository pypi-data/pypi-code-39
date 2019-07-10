import numpy as np
import pandas as pd
import sparse

class Reader(object):
    """
    Simple text reader. It stores each line in a list
    """
    comment_start = ' '

    def readfile(self, path):
        with open(path) as f:
            lines = f.readlines()
        return [line for line in lines if line[0] != self.comment_start]

class Parser(Reader):
    """
    This is a simple class to parse elements from a file. It assumes that
    each line in the file is a single item to parse.
    The parsing for item is done by a input function
    """
    def parse(self, files, function, *args, **kargs):
        """
        For the given files, parse each line using function
        """
        return np.array([item for file in files
            for item in self.parseline(file, function, *args, **kargs)], dtype = "O")

    def parseline(self, file, function, *args, **kargs):
        """
        For a given file, parse its line using function
        """
        return np.array([function(line, *args)
            for line in self.readfile(file)],dtype = "O")

class Writer(object):
    """
    Basic class to store data in text format. It assumes data is given
    as list of string
    """
    def writefile(self, data, file_path):
        with open(file_path, 'w') as f:
            data_str = '\n'.join(data)
            f.write(data_str)

class Serialiser(Writer):
    """
    Class for serialising data
    """

    def serialise(self, data, output_file):
        """
        List data is serialised item by item and stored in output_file
        """
        data_str = [self.serialise_item(item) for item in data]
        self.writefile(data_str, output_file)

    def serialise_item(self, item):
        """
        Each element in the item is serialised as str
        """
        item_str = [str(i) for i in item]
        return ','.join(item_str)

class StrAndInt(object):
    """
    Tuple of str-int
    """
    def __init__(self, entry, *argv):
        items = entry.strip().split(',')
        self.tuple = (items[0], int(items[1]))

class StrAndStr(object):
    """
    Tuple of str-str
    """
    def __init__(self, entry, *argv):
        items = entry.split(',')
        self.tuple = (items[0], items[1])

class Dict(Serialiser, Parser):
    """
    Generic dictionary with store and load functions
    """
    def __init__(self, parsing_func, tuples):
        self.parsing_func = parsing_func
        self.dict = dict(tuples)

    def store(self, file):
        self.serialise(self.dict.items(), file)

    def load(self, file):
        self.dict = self.parse([file], self.parsing_func)
        self.dict = dict([t.tuple for t in self.dict])

def write_trec_ranking_file(rank, file_path):
    """Write to csv file the dataframe rank. The format of the columns is
    fixed.
    Args:
        rank: The dataframe to store
        file_path: Path to the output file
    """
    rank = rank.assign(type='Q0')
    rank = rank.assign(alg='katz')
    rank.to_csv(file_path, sep = ' ', header = False, index = False,
                columns = ['query','type','entity','rank','score','alg'])


def read_trec_gt_file(file_path, separator = '|'):
    """Read trec ground truth file.
    Args:
        file_path: Path to the input file.
    Response:
        a dataframe containing the ground truth
    """
    return pd.read_csv(file_path, sep = separator, header = None,
                    names = ['s','o','p'])

def read_trec_mapping_file(file_path, separator = '|'):
    """Read trec mapping file. It contains the uris for the ids.
    Args:
        file_path: Path to the input file.
        separator: character used to divide columns in csv file
    Response:
        a dataframe containing the mapping file
    """
    return pd.read_csv(file_path, sep = '|', header = None,
                    names = ['entity_id', 'uri'], index_col = ['entity_id'])

def triple_set_to_sparse_matrix(triple_set):
    """Transfor a triple set (Pandas DataFrame) to a sparse matrix.
    The triple set is composed by three columns: subject, object and
    predicate. Each triple is an entry in the sparse matrix. The
    output is a 3-dimensional matrix in COO format.
    Args:
        triple_set: A pandas DataFrame.
    Response:
        a sparse 3D COO matrix.
    """
    n = max(np.max(triple_set.subject), np.max(triple_set.object)) + 1
    k = np.max(triple_set.predicate) + 1
    return sparse.COO([triple_set.subject, triple_set.object,
        triple_set.predicate],
        np.ones_like(triple_set.subject), shape = (n, n, k)
        )

def read_adjacency_file(adjacency_path, sep = '|'):
    """Read adjacency file.
    An adjacency file is a csv file composed by three columns, subject,
    object and predicate. Each line corresponds to a link in the adjacency
    matrix. The output of this method is a sparse 3 dimensional COO matrix.
    Args:
        file_path: Path to the triple file.
        separator: character used to divide columns in csv file.
    Response:
        a sparse 3D COO matrix.
    """
    # Read file
    return triple_set_to_sparse_matrix(
            pd.read_csv(adjacency_path, sep = sep, header = None,
                names = ['subject', 'object', 'predicate'])
            )

def read_mapping_file(mapping_path, sep = '|'):
    """Read mapping file.
    A mapping file is a csv file composed by two columns: the entity id
    and the entity url. The output is a pandas' dataframe object.
    Args:
        mapping_file: Path to the mapping file.
        separator: character used to dvivde columns in csv file.
    Response:
        a DataFrame object.
    """
    return pd.read_csv(mapping_path, sep = sep, header = None,
            names = ['entity_id', 'uri'], index_col = ['entity_id'])

def read_result_file(result_path, sep = ' '):
    """Read result file.
    A result file is a csv file composed by 6 columns: query name, query
    type, entity name, position in the ranking, score and algorithm name.
    The output is a pandas' dataframe object.
    Args:
        result_file: Path to the result file.
        separator: character used to divide columns in csv file.
    Response:
        a DataFrame object
    """
    return pd.read_csv(result_path, sep = ' ', header = None,
            names = ['query','type','entity','position','score','algo'],
            index_col = ['query','type','entity'])
