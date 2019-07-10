import pandas as pd
import numpy as np
import scipy as sp
from .utilities import Parser
from .math import isin, argsort_sparse_matrix
from functools import reduce
import gensim

class ReIndex(object):
    """This class reindex the result of a random walk process, removing unwanted nodes.
    """
    def __init__(self, id_map, filters):
        """Object constructor
        Args:
            id_map: a dictionary with keys as id and values as uris
            filters: a numpy arry with node ids that would be removed from the results.
        """
        self.id_map = id_map
        self.filters = set(filters)

    def ranking_for_queries(self, diffusion, query_response_set,  max_items = 200):
        """It brings at most 'max_itmes' sorted by their relevance to the
        'query' and filtered according to 'filters'.
        Args:
            diffusion: A random walk process
            query_response_set: A query response set object.
            max_items: The maximum number of retrieved items.
        Response:
            A DataFrame with the result of the query sorted by relevance and
            the ids translated into uris
        """
        # We compute the scores for the entire set of queries
        scores = diffusion.query(query_response_set.matrix)
        # scores is a csc matrix
        # Remove unwanted entities
        if len(self.filters) > 0:
            unwanted = isin(scores.indices, self.filters)
            scores.data[unwanted] = 0
            scores.eliminate_zeros()
        # list to collect table per queries
        tables = []
        # for each query, do argsort
        args = argsort_sparse_matrix(scores, max_items)
        # for each query
        for i in range(scores.shape[1]):
            # ids and values for one query
            name = query_response_set.query_names[i]
            x = scores.indptr[i]
            y = scores.indptr[i+1]
            rank_arg = args[:,i]
            rank_arg = rank_arg[ rank_arg >= 0]
            ids = scores.indices[x:y]
            values = scores.data[x:y]
            # get top only
            ids = ids[rank_arg]
            values = values[rank_arg]
            # Create output
            rank = np.arange(1, ids.size + 1, dtype = int)
            entities = [ self.id_map[_id] for _id in ids]
            # Create table
            table = pd.DataFrame({'id':ids,'score':values,'rank':rank,'entity':entities})
            table = table.assign(query = name)
            tables.append(table)
        return pd.concat(tables)

class Mapper(object):
    """This class maps ids to uris and vice-versa
    """
    # this value was determined empirically over the experiment dataset
    uri_max_size = 150
    def __init__(self, mapping):
        """Object constructor. It creates two mapping dictionaries
        """
        self.mapping = mapping
        self.n = mapping.shape[0]
        self.id_map = mapping.to_dict()['uri']
        self.uri_map = {v: k for k, v in self.id_map.items()}

    def uri_to_id(self, uri):
        """Translate uri to id
        Args:
            uri: an uri in mapping object
        Response:
            the id of uri
        """
        return self.uri_map[uri]

    def id_to_uri(self, _id):
        """Tanslate _id to uri
        Args:
            _id: an id in mapping object
        Response:
            the uri of _id
        """
        return self.id_map[_id]

    def uris_to_ids(self, uris):
        """Translate several uris to ids
        Args:
            _uris: a list with uris
        Response:
            the ids for each uri in uris
        """
        return [self.uri_map[uri] for uri in uris]

    def ids_to_uris(self, ids):
        """Translate several ids to uris
        Args:
            ids: a list with ids
        Reponse:
            the uris for each id in ids
        """
        return [self.id_map[_id] for _id in ids]

    def match_expression(self, expression):
        """Match a string expression in mapping
        """
        return self.mapping[self.mapping.uri.str.contains(
            expression, regex=False)].index.values

    def match_expressions(self, expressions):
        """Match the string expressions included in expressions list
        """
        expr = [ self.match_expression(expression) for expression in expressions ]
        if len(expr) > 0:
            return np.unique(np.concatenate(expr))
        return np.array([], dtype = np.int32)
